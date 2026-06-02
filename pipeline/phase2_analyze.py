"""
Phase 2 — Audio Analysis
For each chapter: extract duration/waveform metadata, run Whisper transcription
(if available), detect silence gaps, and write chapter_summary.json.
"""
from pathlib import Path

from .config import DIRS, DEFAULT_WPM, WHISPER_MODEL, SCENE_IDEAL_DURATION, SILENCE_THRESHOLD
from .utils import setup_logging, load_json, save_json, format_duration

log = setup_logging("phase2", "phase2.log")

# ── Optional dependency guards ─────────────────────────────────────────────────
try:
    from mutagen import File as MutagenFile
    _MUTAGEN = True
except ImportError:
    _MUTAGEN = False
    log.warning("mutagen not installed — duration may be 0.  pip install mutagen")

try:
    import whisper as _whisper
    _WHISPER = True
except ImportError:
    _WHISPER = False
    log.warning("openai-whisper not installed — transcription skipped.  pip install openai-whisper")

_whisper_model_cache: dict = {}


def get_duration(path: Path) -> float:
    if not _MUTAGEN:
        return 0.0
    try:
        af = MutagenFile(str(path))
        return float(af.info.length) if af and hasattr(af, "info") else 0.0
    except Exception as exc:
        log.warning("Could not read duration for %s: %s", path.name, exc)
        return 0.0


def _load_whisper_model():
    if WHISPER_MODEL not in _whisper_model_cache:
        log.info("  Loading Whisper model '%s'…", WHISPER_MODEL)
        _whisper_model_cache[WHISPER_MODEL] = _whisper.load_model(WHISPER_MODEL)
    return _whisper_model_cache[WHISPER_MODEL]


def transcribe(audio_path: Path, chapter_num: int) -> dict:
    """Run Whisper and return a transcript dict with word-level timestamps."""
    out = DIRS["transcripts"] / f"chapter_{chapter_num:02d}.json"

    if out.exists():
        log.info("  Transcript cache hit: %s", out.name)
        return load_json(out)

    if not _WHISPER:
        log.warning("  Whisper unavailable — generating stub transcript.")
        stub = _stub_transcript(audio_path, chapter_num)
        save_json(stub, out)
        return stub

    log.info("  Transcribing %s with Whisper (%s)…", audio_path.name, WHISPER_MODEL)
    model = _load_whisper_model()
    result = model.transcribe(str(audio_path), word_timestamps=True)

    words = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "word":  w["word"].strip(),
                "start": round(w["start"], 3),
                "end":   round(w["end"],   3),
            })

    transcript = {
        "chapter":    chapter_num,
        "file":       audio_path.name,
        "full_text":  result["text"].strip(),
        "language":   result.get("language", "en"),
        "words":      words,
        "transcribed": True,
    }
    save_json(transcript, out)
    log.info("  Saved transcript: %s (%d words)", out.name, len(words))
    return transcript


def _stub_transcript(audio_path: Path, chapter_num: int) -> dict:
    dur = get_duration(audio_path)
    return {
        "chapter":    chapter_num,
        "file":       audio_path.name,
        "full_text":  "[Transcription pending — install openai-whisper]",
        "language":   "en",
        "words":      [],
        "duration":   dur,
        "estimated_word_count": int(dur / 60 * DEFAULT_WPM),
        "transcribed": False,
    }


def detect_silences(words: list[dict]) -> list[dict]:
    """Return silence gaps between consecutive words."""
    gaps = []
    for i in range(1, len(words)):
        gap = words[i]["start"] - words[i - 1]["end"]
        if gap >= SILENCE_THRESHOLD:
            gaps.append({
                "after_word": words[i - 1]["word"],
                "start": round(words[i - 1]["end"], 3),
                "end":   round(words[i]["start"],   3),
                "duration": round(gap, 3),
            })
    return gaps


def pacing_profile(words: list[dict], duration: float) -> dict:
    wpm = len(words) / (duration / 60) if (words and duration) else DEFAULT_WPM
    if   wpm < 100: pace, desc = "very_slow",  "Deliberate, contemplative"
    elif wpm < 130: pace, desc = "slow",        "Measured, authoritative"
    elif wpm < 160: pace, desc = "moderate",    "Clear, engaging"
    elif wpm < 190: pace, desc = "fast",        "Energetic, intense"
    else:           pace, desc = "very_fast",   "Rapid-fire, high tension"
    return {"wpm": round(wpm, 1), "pace": pace, "description": desc}


def emotional_intensity(pace: str, silences: list) -> tuple[str, str]:
    long_silences = [s for s in silences if s["duration"] > 1.0]
    if pace in ("very_slow", "slow") or len(long_silences) > 3:
        return "low", "slow_cinematic"
    if pace == "moderate":
        return "medium", "steady_cinematic"
    return "high", "dynamic_cutting"


def chapter_summary(audio_path: Path, chapter_num: int, transcript: dict,
                    fallback_duration: float = 0.0) -> dict:
    dur = get_duration(audio_path) or transcript.get("duration", 0.0) or fallback_duration
    words  = transcript.get("words", [])
    w_count = len(words) or transcript.get("estimated_word_count", 0)

    pacing   = pacing_profile(words, dur)
    silences = detect_silences(words)
    intensity, vis_pace = emotional_intensity(pacing["pace"], silences)

    n_scenes = max(1, int(dur / SCENE_IDEAL_DURATION))

    summary = {
        "chapter":                chapter_num,
        "file":                   audio_path.name,
        "runtime_seconds":        round(dur, 2),
        "runtime_formatted":      format_duration(dur),
        "word_count":             w_count,
        "pacing_profile":         pacing,
        "silence_gaps":           silences,
        "emotional_intensity":    intensity,
        "recommended_visual_pacing": vis_pace,
        "estimated_scene_count":  n_scenes,
        "avg_scene_duration":     round(dur / n_scenes, 2) if n_scenes else 0,
        "transcription_available": transcript.get("transcribed", False),
    }

    out = DIRS["transcripts"] / f"chapter_{chapter_num:02d}_summary.json"
    save_json(summary, out)
    return summary


def run(chapters: list[dict]) -> list[dict]:
    """Analyze every chapter. Returns enriched chapter list with summaries."""
    log.info("=== Phase 2: Audio Analysis ===")
    DIRS["transcripts"].mkdir(parents=True, exist_ok=True)

    enriched = []
    for ch in chapters:
        path = Path(ch["dest_path"])
        num  = ch["chapter_number"]
        log.info("[%02d] %s", num, path.name)

        transcript = transcribe(path, num)
        summary    = chapter_summary(path, num, transcript,
                                     fallback_duration=ch.get("duration_seconds", 0.0))

        ch = dict(ch)
        ch["duration_seconds"] = summary["runtime_seconds"]
        ch["summary"]          = summary
        ch["transcript_path"]  = str(DIRS["transcripts"] / f"chapter_{num:02d}.json")
        enriched.append(ch)

        log.info("  %s | WPM: %.0f | Intensity: %s | Scenes: ~%d",
                 summary["runtime_formatted"],
                 summary["pacing_profile"]["wpm"],
                 summary["emotional_intensity"],
                 summary["estimated_scene_count"])

    return enriched
