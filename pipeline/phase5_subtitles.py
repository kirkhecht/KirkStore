"""
Phase 5 — Subtitle Generation
Produces SRT and ASS subtitle files from scene timelines.
Falls back to word-timestamp-level subtitles when available.
"""
from pathlib import Path

from .config import DIRS, SUBTITLE_MAX_CHARS, SUBTITLE_FONT, SUBTITLE_FONTSIZE, SUBTITLE_MARGIN_V
from .utils import setup_logging, load_json, seconds_to_srt, seconds_to_ass, wrap_subtitle

log = setup_logging("phase5", "phase5.log")

# ── ASS header ─────────────────────────────────────────────────────────────────
_ASS_HEADER = """\
[Script Info]
Title: KirkStore Documentary
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,2.5,1,2,80,80,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _srt_block(index: int, start: float, end: float, text: str) -> str:
    return (
        f"{index}\n"
        f"{seconds_to_srt(start)} --> {seconds_to_srt(end)}\n"
        f"{wrap_subtitle(text, SUBTITLE_MAX_CHARS)}\n\n"
    )


def _ass_event(start: float, end: float, text: str) -> str:
    wrapped = wrap_subtitle(text, SUBTITLE_MAX_CHARS).replace("\n", "\\N")
    return f"Dialogue: 0,{seconds_to_ass(start)},{seconds_to_ass(end)},Default,,0,0,0,,{wrapped}\n"


def scenes_to_subtitles(scenes: list[dict]) -> tuple[str, str]:
    """Convert scene list to SRT and ASS strings."""
    srt_parts = []
    ass_events = []

    for i, s in enumerate(scenes, start=1):
        text  = s.get("subtitle_text", s.get("narration", ""))
        start = s["start"]
        end   = s["end"]
        if not text.strip() or text.startswith("["):
            continue
        srt_parts.append(_srt_block(i, start, end, text))
        ass_events.append(_ass_event(start, end, text))

    srt = "".join(srt_parts)
    ass = (
        _ASS_HEADER.format(
            font=SUBTITLE_FONT,
            size=SUBTITLE_FONTSIZE,
            margin=SUBTITLE_MARGIN_V,
        )
        + "".join(ass_events)
    )
    return srt, ass


def word_timestamps_to_subtitles(words: list[dict],
                                  max_chars: int = SUBTITLE_MAX_CHARS) -> tuple[str, str]:
    """Build tighter subtitles from Whisper word timestamps."""
    groups: list[tuple[float, float, str]] = []
    cur_words: list[str] = []
    group_start = words[0]["start"] if words else 0.0
    cur_len = 0

    for i, w in enumerate(words):
        word = w["word"].strip()
        if not word:
            continue
        new_len = cur_len + len(word) + (1 if cur_words else 0)
        at_sentence_end = word.endswith((".", "!", "?"))
        if new_len > max_chars or at_sentence_end:
            cur_words.append(word)
            groups.append((group_start, w["end"], " ".join(cur_words)))
            cur_words  = []
            group_start = w["end"]
            cur_len    = 0
        else:
            cur_words.append(word)
            cur_len = new_len

    if cur_words:
        groups.append((group_start, words[-1]["end"], " ".join(cur_words)))

    srt_parts = []
    ass_events = []
    for idx, (start, end, text) in enumerate(groups, start=1):
        srt_parts.append(_srt_block(idx, start, end, text))
        ass_events.append(_ass_event(start, end, text))

    srt = "".join(srt_parts)
    ass = (
        _ASS_HEADER.format(
            font=SUBTITLE_FONT,
            size=SUBTITLE_FONTSIZE,
            margin=SUBTITLE_MARGIN_V,
        )
        + "".join(ass_events)
    )
    return srt, ass


def run(all_scenes: dict[int, list[dict]], chapters: list[dict]) -> None:
    """Generate per-chapter and master subtitle files."""
    log.info("=== Phase 5: Subtitle Generation ===")
    DIRS["subtitles"].mkdir(parents=True, exist_ok=True)

    master_srt_parts  = []
    master_ass_events = []
    sub_counter = 1

    for ch in chapters:
        num    = ch["chapter_number"]
        scenes = all_scenes.get(num, [])
        if not scenes:
            continue

        transcript_path = ch.get("transcript_path", "")
        words: list[dict] = []
        if transcript_path:
            try:
                t = load_json(Path(transcript_path))
                words = t.get("words", [])
            except Exception:
                pass

        if words:
            srt, ass = word_timestamps_to_subtitles(words)
            log.info("[%02d] Word-level subtitles (%d words)", num, len(words))
        else:
            srt, ass = scenes_to_subtitles(scenes)
            log.info("[%02d] Scene-level subtitles (%d scenes)", num, len(scenes))

        # Per-chapter files
        (DIRS["subtitles"] / f"chapter_{num:02d}.srt").write_text(srt, encoding="utf-8")
        (DIRS["subtitles"] / f"chapter_{num:02d}.ass").write_text(ass, encoding="utf-8")

        # Accumulate for master (with renumbered SRT indices)
        for s in scenes:
            text = s.get("subtitle_text", s.get("narration", ""))
            if not text.strip() or text.startswith("["):
                continue
            master_srt_parts.append(
                _srt_block(sub_counter, s["start"], s["end"], text)
            )
            master_ass_events.append(
                _ass_event(s["start"], s["end"], text)
            )
            sub_counter += 1

    master_srt = "".join(master_srt_parts)
    master_ass = (
        _ASS_HEADER.format(
            font=SUBTITLE_FONT,
            size=SUBTITLE_FONTSIZE,
            margin=SUBTITLE_MARGIN_V,
        )
        + "".join(master_ass_events)
    )

    (DIRS["subtitles"] / "master.srt").write_text(master_srt, encoding="utf-8")
    (DIRS["subtitles"] / "master.ass").write_text(master_ass, encoding="utf-8")
    log.info("master.srt and master.ass written (%d subtitle blocks)", sub_counter - 1)
