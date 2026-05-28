"""
Phase 8 — Image Generation
Generates one cinematic image per scene using Flux Dev via Replicate.
Skips already-generated images so the run is fully resumable.
Writes images to project/images/chapter_XX/scene_XXXX.jpg
"""
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .config import (DIRS, REPLICATE_API_KEY, IMAGE_MODEL,
                     IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_STEPS,
                     IMAGE_GUIDANCE, IMAGE_BATCH_WORKERS)
from .utils import setup_logging, load_json

log = setup_logging("phase8", "phase8.log")


def _image_path(chapter: int, scene_number: int) -> Path:
    return DIRS["images"] / f"chapter_{chapter:02d}" / f"scene_{scene_number:04d}.jpg"


def _generate_one(scene: dict) -> tuple[dict, bool, str]:
    """Generate a single image with retry/backoff. Returns (scene, success, error_msg)."""
    import replicate

    ch  = scene["chapter"]
    num = scene["scene_number"]
    out = _image_path(ch, num)

    if out.exists():
        return scene, True, "cached"

    out.parent.mkdir(parents=True, exist_ok=True)
    prompt = scene.get("image_prompt", "ancient Near Eastern cinematic scene")

    for attempt in range(5):
        try:
            from .ot_visual_guide import OT_NEGATIVE
            output = replicate.run(
                IMAGE_MODEL,
                input={
                    "prompt":              prompt,
                    "negative_prompt":     OT_NEGATIVE,
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
            if "429" in msg or "throttled" in msg or "rate limit" in msg.lower():
                wait = 15 * (2 ** attempt)   # 15s, 30s, 60s, 120s, 240s
                time.sleep(wait)
                continue
            return scene, False, msg

    return scene, False, "rate limit retries exhausted"


def run(all_scenes: dict[int, list[dict]]) -> dict[int, list[dict]]:
    """Generate images for all scenes. Fully resumable."""
    log.info("=== Phase 8: Image Generation ===")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY

    flat = [s for scenes in all_scenes.values() for s in scenes]
    total   = len(flat)
    already = sum(1 for s in flat if _image_path(s["chapter"], s["scene_number"]).exists())
    needed  = total - already

    log.info("Total scenes: %d | Already generated: %d | Remaining: %d",
             total, already, needed)

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
                    rate    = (done - already) / elapsed if elapsed > 0 else 0
                    eta_s   = (needed - (done - already)) / rate if rate > 0 else 0
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
