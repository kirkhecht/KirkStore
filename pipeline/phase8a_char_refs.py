"""
Phase 8a — Character Reference Portrait Generation
Generates one canonical portrait per named character using Nano Banana 2 (Google).
Portraits are used by Phase 8 for character consistency.
Fully resumable — skips already-generated portraits.
"""
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from .config import DIRS, REPLICATE_API_KEY
from .ot_visual_guide import CHARACTER_APPEARANCE
from .utils import setup_logging

log = setup_logging("phase8a", "phase8a.log")

# Non-human / collective entities — no portrait needed
_NON_HUMAN = {"God", "Ark", "Israel", "Angel", "Angels", "Serpent", "the LORD", "The LORD"}


def portrait_path(name: str) -> Path:
    safe = name.lower().replace(" ", "_").replace("/", "_")
    return DIRS["char_refs"] / f"{safe}.jpg"


def _generate_portrait(name: str, description: str) -> tuple[str, bool, str]:
    import replicate

    out = portrait_path(name)
    if out.exists():
        return name, True, "cached"

    out.parent.mkdir(parents=True, exist_ok=True)

    # Clean description — nano-banana-2 handles photorealism naturally
    base = description.replace(", photorealistic", "").replace("photorealistic", "").strip().rstrip(",")
    prompt = (
        f"{base}. "
        f"Close-up portrait, face fully visible, looking directly at camera, neutral expression. "
        f"Plain rocky limestone background. Ultra photorealistic, 8K, shot on cinema camera, "
        f"authentic Middle Eastern features, natural daylight."
    )

    for attempt in range(5):
        try:
            output = replicate.run(
                "google/nano-banana-2",
                input={
                    "prompt":        prompt,
                    "aspect_ratio":  "9:16",
                    "output_format": "jpg",
                }
            )
            url = str(output[0]) if isinstance(output, list) else str(output)
            urllib.request.urlretrieve(url, out)
            return name, True, ""
        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "throttled" in msg.lower() or "rate limit" in msg.lower():
                wait = 15 * (2 ** attempt)
                log.info("Rate-limited on %s attempt %d — sleeping %ds", name, attempt + 1, wait)
                time.sleep(wait)
                continue
            return name, False, msg

    return name, False, "rate limit retries exhausted"


def run(all_scenes: dict[int, list[dict]]) -> None:
    """Generate canonical portrait for every named character that appears in scenes."""
    log.info("=== Phase 8a: Character Reference Portrait Generation (Nano Banana 2) ===")

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_KEY
    DIRS["char_refs"].mkdir(parents=True, exist_ok=True)

    scene_chars: set[str] = set()
    for scenes in all_scenes.values():
        for s in scenes:
            for fig in (s.get("key_figures") or []):
                scene_chars.add(fig)

    to_generate = {
        name: desc
        for name, desc in CHARACTER_APPEARANCE.items()
        if name in scene_chars and name not in _NON_HUMAN
    }

    already = sum(1 for n in to_generate if portrait_path(n).exists())
    needed = len(to_generate) - already
    log.info("Characters: %d | Already done: %d | Remaining: %d",
             len(to_generate), already, needed)

    if needed == 0:
        log.info("All character portraits present — skipping generation.")
        return

    todo = {n: d for n, d in to_generate.items() if not portrait_path(n).exists()}
    done_count = already

    with ThreadPoolExecutor(max_workers=1) as pool:
        futures = {pool.submit(_generate_portrait, n, d): n for n, d in todo.items()}
        for future in as_completed(futures):
            name, ok, msg = future.result()
            done_count += 1
            if ok and msg != "cached":
                log.info("[%d/%d] %s — OK", done_count, len(to_generate), name)
            elif not ok:
                log.warning("[%d/%d] %s — FAIL: %s", done_count, len(to_generate), name, msg)

    total_done = sum(1 for n in to_generate if portrait_path(n).exists())
    log.info("Portraits complete: %d/%d → %s", total_done, len(to_generate), DIRS["char_refs"])
