"""
Phase 3 — Scene Segmentation
Splits each chapter's narration into cinematic 2–6 second scenes.
Cuts align with sentence boundaries and silence gaps.
Outputs scene_timeline.json per chapter.
"""
import re
from pathlib import Path

from .config import (DIRS, SCENE_MIN_DURATION, SCENE_MAX_DURATION,
                     SCENE_IDEAL_DURATION, SILENCE_THRESHOLD)
from .utils import setup_logging, load_json, save_json, format_duration

log = setup_logging("phase3", "phase3.log")

SENTENCE_END = re.compile(r'[.!?]["\'»]?\s*$')

# ── Emotion keyword map ────────────────────────────────────────────────────────
_EMOTION_WORDS: dict[str, list[str]] = {
    "dark_and_tense":   ["death", "fall", "chaos", "blood", "shadow", "ruin",
                         "despair", "tragedy", "collapse", "destruction", "war",
                         "battle", "plague", "famine", "massacre"],
    "triumphant":       ["victory", "triumph", "glory", "conquer", "rise",
                         "achieve", "empire", "power", "rule", "dominion",
                         "crown", "sovereign", "champion"],
    "mysterious":       ["secret", "hidden", "ancient", "unknown", "legend",
                         "myth", "forbidden", "cursed", "ritual", "prophecy",
                         "oracle", "whisper", "shadow"],
    "solemn":           ["ceremony", "sacred", "ritual", "honor", "grave",
                         "mourn", "remember", "silence", "prayer", "eternal"],
    "epic_grandeur":    ["empire", "dynasty", "civilization", "thousand",
                         "centuries", "vast", "great", "monumental", "colossal",
                         "kingdom", "realm", "age"],
    "hopeful":          ["hope", "light", "future", "dream", "dawn", "new",
                         "begin", "rise", "free", "peace", "rebuild", "restore"],
    "dramatic":         ["reveal", "shock", "discover", "suddenly", "moment",
                         "turn", "crisis", "fate", "destiny", "crucial"],
}

_MOTION_FOR_EMOTION: dict[str, str] = {
    "dark_and_tense":  "slow_zoom_in",
    "triumphant":      "slow_zoom_out",
    "mysterious":      "slow_pan_left",
    "solemn":          "static_with_subtle_zoom",
    "epic_grandeur":   "wide_slow_pan",
    "hopeful":         "slow_zoom_out_with_tilt_up",
    "dramatic":        "push_in_fast",
    "neutral":         "slow_zoom_in",
}

_VISUAL_TEMPLATES: dict[str, str] = {
    "dark_and_tense":  "dramatic wide shot, dark atmosphere, storm clouds, ruins",
    "triumphant":      "heroic wide shot, golden light, raised standards, gathered crowds",
    "mysterious":      "misty ancient location, torchlight, shadowed archways",
    "solemn":          "solitary figure, long shadows, stone architecture, candlelight",
    "epic_grandeur":   "aerial establishing shot, vast landscape, monumental architecture",
    "hopeful":         "sunrise over landscape, open horizon, warm golden light",
    "dramatic":        "extreme close-up, high contrast lighting, cinematic depth of field",
    "neutral":         "mid-shot, natural lighting, period-accurate environment",
}


def detect_emotion(text: str) -> str:
    text_lower = text.lower()
    scores = {emo: 0 for emo in _EMOTION_WORDS}
    for emo, keywords in _EMOTION_WORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[emo] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "neutral"


def is_sentence_end(word: str) -> bool:
    return bool(SENTENCE_END.search(word))


def build_scenes_from_words(words: list[dict], chapter_num: int,
                             chapter_title: str) -> list[dict]:
    """
    Walk word timestamps and create scenes respecting:
      - min 2s, max 6s duration
      - prefer cutting at sentence ends
      - also cut on silence gaps >= SILENCE_THRESHOLD
    """
    scenes = []
    scene_start = words[0]["start"] if words else 0.0
    current_words: list[dict] = []
    scene_idx = 1

    def flush(end_time: float) -> None:
        nonlocal scene_start, current_words, scene_idx
        if not current_words:
            return
        text    = " ".join(w["word"] for w in current_words).strip()
        emotion = detect_emotion(text)
        visual  = _VISUAL_TEMPLATES.get(emotion, _VISUAL_TEMPLATES["neutral"])
        motion  = _MOTION_FOR_EMOTION.get(emotion, "slow_zoom_in")
        prompt  = (
            f"{visual}, {chapter_title.lower()} era, "
            f"cinematic lighting, ultra realistic film still, 16:9"
        )
        scenes.append({
            "scene_number":          scene_idx,
            "chapter":               chapter_num,
            "chapter_title":         chapter_title,
            "start":                 round(scene_start, 3),
            "end":                   round(end_time, 3),
            "duration":              round(end_time - scene_start, 3),
            "narration":             text,
            "emotion":               emotion,
            "visual_description":    visual,
            "image_prompt":          prompt,
            "motion_recommendation": motion,
            "subtitle_text":         text,
        })
        scene_start  = end_time
        current_words = []
        scene_idx   += 1

    for i, w in enumerate(words):
        current_words.append(w)
        elapsed = w["end"] - scene_start

        # Check gap to next word
        gap_to_next = 0.0
        if i + 1 < len(words):
            gap_to_next = words[i + 1]["start"] - w["end"]

        force_cut = elapsed >= SCENE_MAX_DURATION
        good_cut  = (elapsed >= SCENE_MIN_DURATION and
                     (is_sentence_end(w["word"]) or gap_to_next >= SILENCE_THRESHOLD))

        if force_cut or good_cut:
            flush(w["end"])

    # Flush any remaining words
    if current_words:
        flush(current_words[-1]["end"])

    return scenes


def estimate_scenes_from_duration(duration: float, chapter_num: int,
                                   chapter_title: str) -> list[dict]:
    """Fallback: create uniformly-spaced scenes when no word timestamps exist."""
    scenes = []
    t = 0.0
    idx = 1
    while t < duration:
        end = min(t + SCENE_IDEAL_DURATION, duration)
        emotion = "neutral"
        visual  = _VISUAL_TEMPLATES["neutral"]
        motion  = _MOTION_FOR_EMOTION["neutral"]
        prompt  = (
            f"{visual}, {chapter_title.lower()} documentary scene, "
            f"cinematic lighting, ultra realistic film still, 16:9"
        )
        scenes.append({
            "scene_number":          idx,
            "chapter":               chapter_num,
            "chapter_title":         chapter_title,
            "start":                 round(t, 3),
            "end":                   round(end, 3),
            "duration":              round(end - t, 3),
            "narration":             f"[Scene {idx} — transcription pending]",
            "emotion":               emotion,
            "visual_description":    visual,
            "image_prompt":          prompt,
            "motion_recommendation": motion,
            "subtitle_text":         f"[Scene {idx}]",
        })
        t = end
        idx += 1
    return scenes


def _annotate_sections(scenes: list[dict], sections: list[dict]) -> None:
    """Proportionally assign section_title and key_figures to scenes."""
    n, k = len(scenes), len(sections)
    if not n or not k:
        return
    for i, scene in enumerate(scenes):
        sec = sections[min(int(i / n * k), k - 1)]
        scene["section_title"] = sec["title"]
        scene["key_figures"]   = sec.get("key_figures", [])


def run(chapters: list[dict],
        ot_chapters: dict | None = None) -> dict[int, list[dict]]:
    """Segment all chapters. Returns {chapter_num: [scene, ...]}."""
    log.info("=== Phase 3: Scene Segmentation ===")
    all_scenes: dict[int, list[dict]] = {}

    for ch in chapters:
        num   = ch["chapter_number"]
        title = ch["chapter_title"]
        log.info("[%02d] %s", num, title)

        transcript_path = ch.get("transcript_path", "")
        transcript = {}
        if transcript_path:
            try:
                transcript = load_json(Path(transcript_path))
            except Exception:
                pass

        words    = transcript.get("words", [])
        duration = ch.get("duration_seconds", 0.0)

        if words:
            scenes = build_scenes_from_words(words, num, title)
            log.info("  %d scenes from word timestamps", len(scenes))
        else:
            scenes = estimate_scenes_from_duration(duration, num, title)
            log.info("  %d scenes estimated (no timestamps)", len(scenes))

        if ot_chapters and num in ot_chapters:
            sections = ot_chapters[num].get("sections", [])
            if sections:
                _annotate_sections(scenes, sections)
                log.info("  Annotated with %d OT sections", len(sections))

        out = DIRS["scene_json"] / f"chapter_{num:02d}_scenes.json"
        save_json(scenes, out)

        all_scenes[num] = scenes
        log.info("  Wrote %s", out.name)

    # Master scene timeline
    flat = [s for scenes in all_scenes.values() for s in scenes]
    save_json(flat, DIRS["scene_json"] / "scene_timeline.json")
    log.info("scene_timeline.json: %d total scenes across %d chapters",
             len(flat), len(chapters))

    return all_scenes
