"""
Phase 8 — Image Generation
Generates one cinematic image per scene using Google Gemini (gemini-2.5-flash-image)
directly via the Google AI Studio API, falling back to Nano Banana on rate limits.
Fully resumable — skips already-generated images.
Writes images to project/images/chapter_XX/scene_XXXX.jpg
"""
import base64
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

from .config import DIRS, GOOGLE_AI_STUDIO_KEY, IMAGE_BATCH_WORKERS
from .utils import setup_logging

log = setup_logging("phase8", "phase8.log")

_IMAGEN_MODEL    = "imagen-4.0-ultra-generate-001"
_FLASH_IMAGE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-image:generateContent"
)
_IMAGEN_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{_IMAGEN_MODEL}:predict"
)

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


def _find_reference_portrait(scene: dict) -> tuple[Path | None, str | None]:
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
    base = scene.get("image_prompt", "ancient Near Eastern cinematic scene")
    if primary_char:
        return f"The reference image shows {primary_char}. {base}"
    return base


def _call_nano_banana(prompt: str, key: str, timeout: int = 90) -> bytes:
    resp = requests.post(
        f"{_FLASH_IMAGE_URL}?key={key}",
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["image"]},
        },
        timeout=timeout,
    )
    if resp.status_code == 429:
        raise RuntimeError("RATE_LIMIT")
    if resp.status_code != 200:
        raise RuntimeError(resp.json().get("error", {}).get("message", resp.text[:200]))
    parts = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"])
    raise RuntimeError("EMPTY")


def _call_imagen(prompt: str, key: str, timeout: int = 120) -> bytes:
    resp = requests.post(
        f"{_IMAGEN_URL}?key={key}",
        json={
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1, "aspectRatio": "16:9"},
        },
        timeout=timeout,
    )
    if resp.status_code == 429:
        raise RuntimeError("RATE_LIMIT")
    if resp.status_code != 200:
        raise RuntimeError(resp.json().get("error", {}).get("message", resp.text[:200]))
    preds = resp.json().get("predictions", [])
    if not preds:
        raise RuntimeError("EMPTY")
    return base64.b64decode(preds[0]["bytesBase64Encoded"])


def _generate_one(scene: dict, key: str) -> tuple[dict, bool, str]:
    """Generate a single image using Google AI Studio directly."""
    ch  = scene["chapter"]
    num = scene["scene_number"]
    out = _image_path(ch, num)

    if out.exists():
        return scene, True, "cached"

    out.parent.mkdir(parents=True, exist_ok=True)

    portrait, char_name = _find_reference_portrait(scene)
    prompt = _build_scene_prompt(scene, char_name)

    # Try Imagen 4 Ultra first (30 RPD limit), fall back to Nano Banana
    try:
        data = _call_imagen(prompt, key)
        out.write_bytes(data)
        return scene, True, "imagen"
    except RuntimeError as e:
        if "RATE_LIMIT" not in str(e):
            log.debug("sc%04d: Imagen failed (%s), falling back to Nano Banana",
                      num, str(e)[:80])

    for attempt in range(5):
        try:
            data = _call_nano_banana(prompt, key)
            out.write_bytes(data)
            return scene, True, "nano_banana"
        except RuntimeError as e:
            msg = str(e)
            if "RATE_LIMIT" in msg:
                wait = min(60, 15 * (attempt + 1))
                time.sleep(wait)
                continue
            return scene, False, msg

    return scene, False, "rate limit retries exhausted"


def run(all_scenes: dict[int, list[dict]]) -> dict[int, list[dict]]:
    """Generate images for all scenes. Fully resumable."""
    log.info("=== Phase 8: Image Generation (Google AI Studio) ===")

    key = GOOGLE_AI_STUDIO_KEY
    if not key:
        log.error("GOOGLE_AI_STUDIO_KEY not set — cannot generate images")
        return all_scenes

    flat = [s for scenes in all_scenes.values() for s in scenes]
    total   = len(flat)
    already = sum(1 for s in flat if _image_path(s["chapter"], s["scene_number"]).exists())
    needed  = total - already

    log.info("Total: %d | Done: %d | Remaining: %d", total, already, needed)

    if needed == 0:
        log.info("All images present — nothing to do.")
        return all_scenes

    todo = [s for s in flat if not _image_path(s["chapter"], s["scene_number"]).exists()]
    done = already
    errors = 0
    start = time.time()

    with ThreadPoolExecutor(max_workers=IMAGE_BATCH_WORKERS) as pool:
        futures = {pool.submit(_generate_one, s, key): s for s in todo}
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
