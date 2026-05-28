"""
Phase 4 — Image Prompt Generation
Generates Flux/SD/GPT-ready cinematic image prompts for every scene.
Uses Claude API when ANTHROPIC_API_KEY is set, otherwise uses heuristic templates.
Writes image_prompts.csv.
"""
import csv
import json
from pathlib import Path

from .config import DIRS, IMAGE_BASE_STYLE, USE_AI_PROMPTS, ANTHROPIC_API_KEY, CLAUDE_MODEL
from .utils import setup_logging, save_json, load_json

log = setup_logging("phase4", "phase4.log")

# ── Optional OT visual guide ───────────────────────────────────────────────────
try:
    from .ot_visual_guide import (build_prompt as _ot_build_prompt,
                                   get_negative_prompt as _ot_get_negative)
    _OT_GUIDE = True
except ImportError:
    _OT_GUIDE = False

# ── Style modifiers by emotion ─────────────────────────────────────────────────
_STYLE_MODS: dict[str, str] = {
    "dark_and_tense":  "dark and brooding, storm-lit, shadows dominate, chiaroscuro",
    "triumphant":      "golden hour light, epic scope, triumphant atmosphere, warm tones",
    "mysterious":      "atmospheric fog, flickering torchlight, deep shadows, textured stone",
    "solemn":          "muted palette, single light source, gravitas, still composition",
    "epic_grandeur":   "sweeping vista, monumental scale, wide-angle, awe-inspiring",
    "hopeful":         "warm sunrise light, open sky, fresh colours, optimistic framing",
    "dramatic":        "high contrast, shallow depth of field, intense focal point",
    "neutral":         "neutral natural lighting, balanced composition, period-accurate",
}

_NEGATIVE_PROMPT = (
    "cartoon, anime, illustration, painting, text, watermark, logo, "
    "floating objects, distorted anatomy, modern elements, low quality, "
    "blurry, overexposed, plastic look"
)


def _ot_prompt(scene: dict) -> str:
    """Build an OT-specific prompt using the visual guide."""
    section_title = scene.get("section_title") or scene.get("chapter_title", "")
    chapter_num   = scene.get("chapter", 0)
    emotion       = scene.get("emotion", "solemn")
    setting       = scene.get("visual_description")
    key_figures   = scene.get("key_figures")
    return _ot_build_prompt(section_title, chapter_num, emotion, setting, key_figures)


def _heuristic_prompt(scene: dict) -> str:
    emotion  = scene.get("emotion", "neutral")
    visual   = scene.get("visual_description", "historical documentary scene")
    title    = scene.get("chapter_title", "documentary")
    mod      = _STYLE_MODS.get(emotion, _STYLE_MODS["neutral"])

    return (
        f"{visual}, {mod}, {IMAGE_BASE_STYLE}, "
        f"{title.lower()} historical setting, "
        f"cinematic color grading, film grain, anamorphic lens"
    )


def _ai_batch_prompts(scenes: list[dict]) -> list[str]:
    """Use Claude to generate richer prompts for a batch of scenes."""
    try:
        import anthropic
    except ImportError:
        log.warning("anthropic library not installed — falling back to heuristics.")
        return [_heuristic_prompt(s) for s in scenes]

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    scenes_text = json.dumps(
        [{"scene": s["scene_number"],
          "narration": s["narration"],
          "emotion": s["emotion"],
          "visual_description": s["visual_description"]}
         for s in scenes],
        indent=2
    )

    prompt = f"""You are a cinematic art director generating image generation prompts for a documentary film.

For each scene below, write ONE ultra-detailed image prompt optimized for Flux/Stable Diffusion/DALL-E.

Requirements:
- Ultra realistic, cinematic film still
- Dramatic lighting, high contrast
- Emotionally immersive, historically grounded
- 16:9 composition, no text, no watermarks
- Avoid cartoon, anime, illustration styles
- Include: subject, environment, lighting, mood, camera angle, film aesthetic

Return ONLY a JSON array of strings — one prompt per scene, same order as input.

Scenes:
{scenes_text}"""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()
    # Strip markdown fences if present
    raw = raw.strip("```json").strip("```").strip()
    try:
        prompts = json.loads(raw)
        if isinstance(prompts, list) and len(prompts) == len(scenes):
            return [str(p) for p in prompts]
    except Exception as exc:
        log.warning("Could not parse Claude response: %s — using heuristics.", exc)

    return [_heuristic_prompt(s) for s in scenes]


def enrich_scenes(scenes: list[dict], use_ai: bool = USE_AI_PROMPTS,
                  use_ot: bool = False) -> list[dict]:
    """Add enriched image_prompt field to each scene."""
    if use_ai and scenes:
        log.info("  Generating prompts with Claude API (%d scenes)…", len(scenes))
        batch_size = 20
        ai_prompts = []
        for i in range(0, len(scenes), batch_size):
            batch = scenes[i:i + batch_size]
            log.info("  Batch %d/%d…", i // batch_size + 1,
                     (len(scenes) - 1) // batch_size + 1)
            ai_prompts.extend(_ai_batch_prompts(batch))
        for scene, prompt in zip(scenes, ai_prompts):
            scene["image_prompt"] = prompt
    elif use_ot and _OT_GUIDE:
        log.info("  Generating OT visual guide prompts (%d scenes)…", len(scenes))
        for scene in scenes:
            scene["image_prompt"] = _ot_prompt(scene)
    else:
        log.info("  Generating prompts with heuristic templates (%d scenes)…", len(scenes))
        for scene in scenes:
            scene["image_prompt"] = _heuristic_prompt(scene)

    return scenes


def run(all_scenes: dict[int, list[dict]],
        use_ot: bool = False) -> dict[int, list[dict]]:
    """Enrich all scenes with finalised image prompts. Writes image_prompts.csv."""
    log.info("=== Phase 4: Image Prompt Generation ===")
    mode = "Claude API" if USE_AI_PROMPTS else ("OT visual guide" if use_ot else "heuristic")
    log.info("Prompt mode: %s", mode)

    negative = _ot_get_negative() if (use_ot and _OT_GUIDE) else _NEGATIVE_PROMPT

    DIRS["image_prompts"].mkdir(parents=True, exist_ok=True)

    csv_rows = []
    enriched: dict[int, list[dict]] = {}

    for ch_num, scenes in all_scenes.items():
        log.info("[%02d] %d scenes", ch_num, len(scenes))
        scenes = enrich_scenes(list(scenes), use_ot=use_ot)
        enriched[ch_num] = scenes

        for s in scenes:
            csv_rows.append({
                "scene_number": s["scene_number"],
                "chapter":      s["chapter"],
                "chapter_title": s["chapter_title"],
                "section_title": s.get("section_title", ""),
                "emotion":      s["emotion"],
                "motion":       s["motion_recommendation"],
                "prompt":       s["image_prompt"],
                "negative_prompt": negative,
                "start":        s["start"],
                "end":          s["end"],
                "duration":     s["duration"],
                "narration":    s["narration"][:120],
            })

        # Save enriched scene JSON back to disk so phase 8 picks up updated prompts
        out_json = DIRS["scene_json"] / f"chapter_{ch_num:02d}_scenes.json"
        save_json(scenes, out_json)

        # Per-chapter CSV
        out_csv = DIRS["image_prompts"] / f"chapter_{ch_num:02d}_prompts.csv"
        _write_csv(
            [r for r in csv_rows if r["chapter"] == ch_num],
            out_csv
        )

    # Master CSV
    master_csv = DIRS["image_prompts"] / "image_prompts.csv"
    _write_csv(csv_rows, master_csv)
    log.info("image_prompts.csv: %d rows → %s", len(csv_rows), master_csv)

    return enriched


def _write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
