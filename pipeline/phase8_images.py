"""
Phase 8 — Image Generation
Generates one cinematic image per scene using Nano Banana 2 (Google) via Replicate.
For scenes with named characters, passes the canonical portrait as a reference image
so the model maintains face and identity consistency across all scenes.
Fully resumable — skips already-generated images.
Writes images to project/images/chapter_XX/scene_XXXX.jpg
"""
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .config import (DIRS, REPLICATE_API_KEY, IMAGE_BATCH_WORKERS)
from .utils import setup_logging

log = setup_logging("phase8", "phase8.log")

_MODEL = "google/nano-banana-2"

# Non-human / collective — no portrait reference
_NO_REF = {"God", "Ark", "Israel", "Angel", "Angels", "Serpent", "the LORD", "The LORD"}

# Section title substrings where a character's appearance is age-mismatched vs their portrait
_SKIP_REF_SECTIONS: dict[str, list[str]] = {
    "Moses":  ["birth of moses", "ark in the bulrushes", "baby moses", "infant moses",
               "pharaoh's daughter", "drawn from the water"],
    "Isaac":  ["birth of isaac", "birth of a son"],
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
    for fig in (scene.get("key_figures") or []):
        if fig in _NO_REF:
            continue
        if any(pat in section for pat in _SKIP_REF_SECTIONS.get(fig, [])):
            continue
        p = _portrait_path(fig)
        if p.exists():
            return p, fig
    return None, None


def _build_scene_prompt(scene: dict, primary_char: str | None) -> str:
    """Build the scene prompt, prepending a character label if using a reference image."""
    base = scene.get("image_prompt", "ancient Near Eastern cinematic scene")

    if primary_char:
        # Tell the model who the reference image shows so it can apply consistency
        return f"The reference image shows {primary_char}. {base}"
    return base


def _generate_one(scene: dict) -> tuple[dict, bool, str]:
    """Generate a single image. Uses portrait reference when available."""
    import replicate

    ch  = scene["chapter"]
    num = scene["scene_number"]
    out = _image_path(ch, num)

    if out.exists():
        return scene, True, "cached"

    out.parent.mkdir(parents=True, exist_ok=True)

    portrait, char_name = _find_reference_portrait(scene)

    for attempt in range(5):
        fh = None
        try:
            prompt = _build_scene_prompt(scene, char_name)
            inp = {
                "prompt":        prompt,
                "aspect_ratio":  "16:9",
                "output_format": "jpg",
            }
            if portrait:
                fh = open(portrait, "rb")
                inp["image"] = fh

            output = replicate.run(_MODEL, input=inp)
            url = str(output[0]) if isinstance(output, list) else str(output)
            urllib.request.urlretrieve(url, out)
            return scene, True, ""

        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "throttled" in msg.lower() or "rate limit" in msg.lower():
                wait = 15 * (2 ** attempt)
                time.sleep(wait)
                continue
            if portrait and attempt == 0:
                log.warning("sc%04d: image-ref call failed (%s) — retrying without reference",
                            scene["scene_number"], msg[:80])
                portrait = None
                char_name = None
                continue
            return scene, False, msg
        finally:
            if fh:
                fh.close()

    return scene, False, "rate limit retries exhausted"


def run(all_scenes: dict[int, list[dict]]) -> dict[int, list[dict]]:
    """Generate images for all scenes. Fully resumable."""
    log.info("=== Phase 8: Image Generation (Nano Banana 2) ===")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

    flat = [s for scenes in all_scenes.values() for s in scenes]
    total   = len(flat)
    already = sum(1 for s in flat if _image_path(s["chapter"], s["scene_number"]).exists())
    needed  = total - already

    with_ref = sum(
        1 for s in flat
        if not _image_path(s["chapter"], s["scene_number"]).exists()
        and _find_reference_portrait(s)[0] is not None
    )
    log.info("Total: %d | Done: %d | Remaining: %d  (%d with character reference, %d text-only)",
             total, already, needed, with_ref, needed - with_ref)

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
                    gen_count = done - already
                    rate = gen_count / elapsed if elapsed > 0 else 0
                    eta_s = (needed - gen_count) / rate if rate > 0 else 0
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
