"""
Phase 8 — Image Generation
Generates one cinematic image per scene using Flux Dev via Replicate.
For scenes with named characters, uses flux-kontext-dev with a canonical
portrait reference for face/identity consistency across the film.
Skips already-generated images so the run is fully resumable.
Writes images to project/images/chapter_XX/scene_XXXX.jpg
"""
import os
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .config import (DIRS, REPLICATE_API_KEY, IMAGE_MODEL, IMAGE_KONTEXT_MODEL,
                     IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_STEPS, IMAGE_GUIDANCE,
                     IMAGE_BATCH_WORKERS)
from .utils import setup_logging, load_json

log = setup_logging("phase8", "phase8.log")

# Characters that don't get reference images (non-human or collective)
_NO_REF = {"God", "Ark", "Israel", "Angel", "Angels", "Serpent", "the LORD", "The LORD"}

# Section title patterns where a character's age/appearance differs from their canonical portrait.
# Maps character name → list of section title substrings (case-insensitive) that should skip ref.
_SKIP_REF_SECTIONS: dict[str, list[str]] = {
    "Moses": ["birth of moses", "ark in the bulrushes", "baby moses", "infant moses",
              "pharaoh's daughter", "drawn from the water"],
    "Isaac": ["birth of isaac", "birth of a son"],
    "Joseph": [],  # Joseph's coat scenes are fine — he's already a teenager
    "Samuel": ["birth of samuel", "hannah"],
}


def _image_path(chapter: int, scene_number: int) -> Path:
    return DIRS["images"] / f"chapter_{chapter:02d}" / f"scene_{scene_number:04d}.jpg"


def _portrait_path(name: str) -> Path:
    safe = name.lower().replace(" ", "_").replace("/", "_")
    return DIRS["char_refs"] / f"{safe}.jpg"


def _find_reference_portrait(scene: dict) -> Path | None:
    """Return a portrait path to use as character reference, or None."""
    section = (scene.get("section_title") or scene.get("chapter_title") or "").lower()
    key_figures = scene.get("key_figures") or []

    for fig in key_figures:
        if fig in _NO_REF:
            continue
        skip_patterns = _SKIP_REF_SECTIONS.get(fig, [])
        if any(pat in section for pat in skip_patterns):
            continue
        p = _portrait_path(fig)
        if p.exists():
            return p

    return None


def _scene_prompt_for_kontext(scene: dict) -> str:
    """
    Build a scene-description prompt for flux-kontext-dev.
    Strips character appearance text — the face comes from the reference image.
    Focuses on action, environment, and emotion.
    """
    base = scene.get("image_prompt", "ancient Near Eastern cinematic scene")

    # Pull out character names to use in a short "show [Name] ..." lead-in
    figs = scene.get("key_figures") or []
    subject_names = [f for f in figs if f not in _NO_REF][:2]

    if subject_names:
        subject_str = " and ".join(subject_names)
        return f"Show {subject_str} in this scene: {base}"
    return base


def _generate_one(scene: dict) -> tuple[dict, bool, str]:
    """Generate a single image. Uses kontext model if a character portrait exists."""
    import replicate

    ch  = scene["chapter"]
    num = scene["scene_number"]
    out = _image_path(ch, num)

    if out.exists():
        return scene, True, "cached"

    out.parent.mkdir(parents=True, exist_ok=True)

    from .ot_visual_guide import OT_NEGATIVE

    ref_portrait = _find_reference_portrait(scene)

    if ref_portrait:
        return _generate_kontext(scene, ref_portrait, out, OT_NEGATIVE)
    else:
        return _generate_flux(scene, out, OT_NEGATIVE)


def _generate_flux(scene: dict, out: Path, negative: str) -> tuple[dict, bool, str]:
    """Generate with plain flux-dev (no reference)."""
    import replicate

    prompt = scene.get("image_prompt", "ancient Near Eastern cinematic scene")

    for attempt in range(5):
        try:
            output = replicate.run(
                IMAGE_MODEL,
                input={
                    "prompt":              prompt,
                    "negative_prompt":     negative,
                    "width":               IMAGE_WIDTH,
                    "height":              IMAGE_HEIGHT,
                    "num_inference_steps": IMAGE_STEPS,
                    "guidance":            IMAGE_GUIDANCE,
                    "output_format":       "jpg",
                    "output_quality":      90,
                }
            )
            url = str(output[0]) if isinstance(output, list) else str(output)
            urllib.request.urlretrieve(url, out)
            return scene, True, ""
        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "throttled" in msg.lower() or "rate limit" in msg.lower():
                wait = 15 * (2 ** attempt)
                time.sleep(wait)
                continue
            return scene, False, msg

    return scene, False, "rate limit retries exhausted"


def _generate_kontext(scene: dict, portrait: Path, out: Path,
                      negative: str) -> tuple[dict, bool, str]:
    """Generate with flux-kontext-dev using canonical character portrait as reference."""
    import replicate

    prompt = _scene_prompt_for_kontext(scene)

    for attempt in range(5):
        try:
            with open(portrait, "rb") as img_file:
                output = replicate.run(
                    IMAGE_KONTEXT_MODEL,
                    input={
                        "input_image":         img_file,
                        "prompt":              prompt,
                        "aspect_ratio":        "16:9",
                        "output_format":       "jpg",
                        "output_quality":      90,
                        "guidance_scale":      IMAGE_GUIDANCE,
                        "num_inference_steps": IMAGE_STEPS,
                        "safety_tolerance":    2,
                    }
                )
            url = str(output[0]) if isinstance(output, list) else str(output)
            urllib.request.urlretrieve(url, out)
            return scene, True, ""
        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "throttled" in msg.lower() or "rate limit" in msg.lower():
                wait = 15 * (2 ** attempt)
                time.sleep(wait)
                continue
            # If kontext model fails for any other reason, fall back to plain flux
            log.warning("kontext failed (sc%04d): %s — falling back to flux-dev",
                        scene["scene_number"], msg)
            return _generate_flux(scene, out, negative)

    return scene, False, "rate limit retries exhausted"


def run(all_scenes: dict[int, list[dict]]) -> dict[int, list[dict]]:
    """Generate images for all scenes. Fully resumable."""
    log.info("=== Phase 8: Image Generation ===")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

    flat = [s for scenes in all_scenes.values() for s in scenes]
    total   = len(flat)
    already = sum(1 for s in flat if _image_path(s["chapter"], s["scene_number"]).exists())
    needed  = total - already

    # Count how many scenes will use kontext (has a portrait)
    kontext_count = sum(
        1 for s in flat
        if not _image_path(s["chapter"], s["scene_number"]).exists()
        and _find_reference_portrait(s) is not None
    )
    log.info("Total scenes: %d | Already done: %d | Remaining: %d",
             total, already, needed)
    log.info("  Of remaining: %d with kontext (character consistency), %d with flux-dev",
             kontext_count, needed - kontext_count)

    if needed == 0:
        log.info("All images present — nothing to do.")
        return all_scenes

    todo = [s for s in flat if not _image_path(s["chapter"], s["scene_number"]).exists()]
    done = already
    errors = 0
    start = time.time()

    with ThreadPoolExecutor(max_workers=IMAGE_BATCH_WORKERS) as pool:
        futures = {pool.submit(_generate_one, s): s for s in todo}
        for future in as_completed(futures):
            scene, ok, msg = future.result()
            done += 1
            if ok:
                if msg != "cached":
                    elapsed = time.time() - start
                    generated_so_far = done - already
                    rate = generated_so_far / elapsed if elapsed > 0 else 0
                    eta_s = (needed - generated_so_far) / rate if rate > 0 else 0
                    log.info("[%d/%d] Ch%02d Sc%04d — OK  (%.1f/min, ETA %dm%02ds)",
                             done, total,
                             scene["chapter"], scene["scene_number"],
                             rate * 60,
                             int(eta_s // 60), int(eta_s % 60))
            else:
                errors += 1
                log.warning("[%d/%d] Ch%02d Sc%04d — FAIL: %s",
                            done, total, scene["chapter"], scene["scene_number"], msg)

    elapsed = time.time() - start
    log.info("Image generation complete: %d ok, %d errors in %.1fs",
             done - errors, errors, elapsed)
    log.info("Images saved to: %s", DIRS["images"])

    return all_scenes
