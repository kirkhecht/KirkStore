"""
Demo data generator — creates synthetic chapter data so you can run the full
pipeline and see all outputs without having real MP3 files.
"""
import random
import shutil
from pathlib import Path

from .config import DIRS
from .utils import setup_logging, save_json

log = setup_logging("demo")

_CHAPTERS = [
    {
        "title": "The Ancient World",
        "duration": 387.4,
        "text": (
            "Long before the empires of the modern world rose to power, ancient civilizations "
            "carved their legacies into stone and sky. The rivers Tigris and Euphrates cradled "
            "the first cities. Farmers learned to tame the wild earth. Priests read the heavens "
            "for signs of divine will. Out of this fertile chaos, the first great kingdoms were born. "
            "They built monuments that would outlast their own memories. And in doing so, they set "
            "the foundation for every civilization that followed."
        ),
    },
    {
        "title": "Rise of Empire",
        "duration": 523.8,
        "text": (
            "War was the crucible in which empires were forged. Armies swept across the ancient world "
            "like storms across a dry plain. Generals became gods. Kings became legends. The clash of "
            "iron and the cry of battle echoed from the Mediterranean coast to the mountains of Persia. "
            "Every victory added territory. Every defeat reshaped borders. The map of the known world "
            "was redrawn with blood and ambition. And yet, from this violence came order. Laws were "
            "written. Roads were built. Trade flourished under the shadow of military power."
        ),
    },
    {
        "title": "The Golden Age",
        "duration": 445.2,
        "text": (
            "There are moments in history when a civilization reaches its peak. Art flourishes. "
            "Philosophy deepens. Science begins to explain the mysteries that once required myth. "
            "The golden age was such a moment. Scholars gathered in great libraries. Architects "
            "conceived buildings that seemed to defy gravity. Poets wrote verses that still move "
            "us today. It was a time of extraordinary human achievement. But golden ages are never "
            "permanent. They exist in the brief window between the struggles that create them and "
            "the forces that eventually bring them down."
        ),
    },
    {
        "title": "Conflict and Collapse",
        "duration": 498.6,
        "text": (
            "The signs of collapse are rarely visible until it is too late. Internal division, "
            "foreign pressure, economic failure — these forces gathered like clouds before a storm. "
            "The empire that had seemed invincible began to fracture. Provinces declared independence. "
            "The army stretched thin across too many borders. Famine gripped the cities. In the "
            "corridors of power, conspiracies replaced governance. The final blow, when it came, "
            "was almost anticlimactic. An empire that had taken centuries to build was undone in a "
            "generation. Its ruins became the foundation for whatever came next."
        ),
    },
    {
        "title": "The Enduring Legacy",
        "duration": 312.9,
        "text": (
            "Civilizations may fall, but their legacies endure. In the languages we speak, the laws "
            "we follow, the architecture that shapes our cities, the ideas that fuel our politics — "
            "the ancient world lives on. Every generation inherits this vast accumulation of human "
            "effort and struggle. We are the sum of everything that came before us. And perhaps that "
            "is the most profound lesson history offers. No civilization truly dies as long as its "
            "ideas continue to shape the living. The past is never past. It is always present."
        ),
    },
]


def _make_word_timestamps(text: str, duration: float) -> list[dict]:
    """Generate realistic synthetic word timestamps."""
    rng = random.Random(42)
    words = text.split()
    # Use ~145 wpm base with slight randomness
    base_gap = 60.0 / 145
    timestamps = []
    t = 0.2  # small intro silence

    for i, word in enumerate(words):
        word_dur = base_gap * (0.6 + rng.random() * 0.8)
        timestamps.append({"word": word, "start": round(t, 3), "end": round(t + word_dur, 3)})
        t += word_dur

        # Gap between words
        t += 0.04 + rng.random() * 0.08

        # Sentence-ending pause
        if word.rstrip("\"'").endswith((".", "!", "?")):
            t += 0.35 + rng.random() * 0.55

    # Scale to fit actual duration
    if timestamps and t > 0:
        scale = (duration - 0.4) / t
        for w in timestamps:
            w["start"] = round(w["start"] * scale, 3)
            w["end"]   = round(w["end"]   * scale, 3)

    return timestamps


def _create_dummy_mp3(path: Path, duration: float) -> None:
    """Create a minimal valid MP3-like placeholder (silence marker)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write a small stub file — not playable but present for path resolution
    path.write_bytes(b"ID3" + b"\x00" * 10 + f"[DEMO:{duration:.1f}s]".encode())


def run() -> list[dict]:
    """Create demo chapters and return chapter list."""
    log.info("Generating demo data for %d chapters…", len(_CHAPTERS))
    DIRS["audio"].mkdir(parents=True, exist_ok=True)
    DIRS["transcripts"].mkdir(parents=True, exist_ok=True)

    chapters = []
    for idx, ch in enumerate(_CHAPTERS, start=1):
        slug     = ch["title"].lower().replace(" ", "_")
        filename = f"{idx:02d}_{slug}.mp3"
        dest     = DIRS["audio"] / filename

        _create_dummy_mp3(dest, ch["duration"])

        words = _make_word_timestamps(ch["text"], ch["duration"])

        transcript = {
            "chapter":    idx,
            "file":       filename,
            "full_text":  ch["text"],
            "language":   "en",
            "duration":   ch["duration"],
            "words":      words,
            "transcribed": True,
            "demo":       True,
        }
        save_json(transcript, DIRS["transcripts"] / f"chapter_{idx:02d}.json")

        chapters.append({
            "chapter_number":       idx,
            "chapter_title":        ch["title"],
            "filename":             filename,
            "source_path":          str(dest),
            "dest_path":            str(dest),
            "duration_seconds":     ch["duration"],
            "estimated_word_count": len(ch["text"].split()),
            "estimated_scene_count": max(1, int(ch["duration"] / 4)),
            "transcript_path":      str(DIRS["transcripts"] / f"chapter_{idx:02d}.json"),
        })
        log.info("  [%02d] %s — %.1fs, %d words",
                 idx, ch["title"], ch["duration"], len(ch["text"].split()))

    return chapters
