"""
Phase 1 — File Organization
Scans source directory, renames audio files consistently, copies to project/audio,
copies scripts/guides to project/scripts, and generates master_index.csv.
"""
import csv
import re
import shutil
from pathlib import Path

from .config import DIRS, DEFAULT_WPM, SCENE_IDEAL_DURATION
from .utils import setup_logging, create_all_dirs, slugify

log = setup_logging("phase1", "phase1.log")

AUDIO_EXTENSIONS  = {".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg"}
SCRIPT_EXTENSIONS = {".txt", ".md", ".docx", ".rtf", ".fountain"}

# Keywords that hint at chapter ordering if the filename has no number
_ORDER_HINTS = [
    "intro", "introduction", "prologue",
    "chapter", "part", "episode",
    "outro", "epilogue", "conclusion", "credits",
]


def _extract_number(name: str) -> int | None:
    """Return leading integer from filename stem, or None."""
    m = re.match(r"^(\d+)", name.strip())
    return int(m.group(1)) if m else None


def _clean_title(stem: str) -> str:
    """Strip leading numbers/separators and return a human title."""
    stem = re.sub(r"^[\d_\-\.]+", "", stem)
    stem = re.sub(r"[_\-]+", " ", stem)
    return stem.strip().title() or stem


def discover_files(source_dir: Path) -> tuple[list[Path], list[Path]]:
    """Recursively find audio and script files under source_dir."""
    audio, scripts = [], []
    for p in sorted(source_dir.rglob("*")):
        if p.is_file():
            if p.suffix.lower() in AUDIO_EXTENSIONS:
                audio.append(p)
            elif p.suffix.lower() in SCRIPT_EXTENSIONS:
                scripts.append(p)
    return audio, scripts


def sort_audio_files(files: list[Path]) -> list[Path]:
    """Sort: numbered first (by number), then alphabetical."""
    numbered   = [(f, _extract_number(f.stem)) for f in files if _extract_number(f.stem) is not None]
    unnumbered = [f for f in files if _extract_number(f.stem) is None]
    numbered.sort(key=lambda x: x[1])
    return [f for f, _ in numbered] + sorted(unnumbered)


def get_audio_duration(path: Path) -> float:
    """Return duration in seconds using mutagen, or 0 if unavailable."""
    try:
        from mutagen import File as MutagenFile
        af = MutagenFile(str(path))
        if af and hasattr(af, "info"):
            return float(af.info.length)
    except Exception:
        pass
    return 0.0


def copy_to_project(source: Path, dest_dir: Path, new_name: str) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / new_name
    if not dest.exists():
        shutil.copy2(source, dest)
        log.info("  Copied %s → %s", source.name, new_name)
    else:
        log.info("  Already exists, skipped: %s", new_name)
    return dest


def run(source_dir: Path) -> list[dict]:
    """
    Main entry point.
    Returns list of chapter dicts used by downstream phases.
    """
    create_all_dirs()
    log.info("=== Phase 1: File Organization ===")
    log.info("Source directory: %s", source_dir)

    audio_files, script_files = discover_files(source_dir)
    log.info("Found %d audio file(s), %d script file(s)", len(audio_files), len(script_files))

    if not audio_files:
        log.warning("No audio files found in %s", source_dir)
        log.warning("Add your ElevenLabs MP3s to that directory and re-run.")
        return []

    audio_files = sort_audio_files(audio_files)

    chapters = []
    for idx, src in enumerate(audio_files, start=1):
        title   = _clean_title(src.stem)
        slug    = slugify(title) or f"chapter_{idx:02d}"
        new_name = f"{idx:02d}_{slug}{src.suffix.lower()}"

        dest = copy_to_project(src, DIRS["audio"], new_name)
        duration = get_audio_duration(dest)

        est_words  = int(duration / 60 * DEFAULT_WPM)
        est_scenes = max(1, int(duration / SCENE_IDEAL_DURATION))

        chapters.append({
            "chapter_number":      idx,
            "chapter_title":       title,
            "filename":            new_name,
            "source_path":         str(src),
            "dest_path":           str(dest),
            "duration_seconds":    round(duration, 2),
            "estimated_word_count": est_words,
            "estimated_scene_count": est_scenes,
        })
        log.info("  [%02d] %s  (%.1fs, ~%d words, ~%d scenes)",
                 idx, new_name, duration, est_words, est_scenes)

    # Copy scripts
    for s in script_files:
        copy_to_project(s, DIRS["scripts"], s.name)

    # Write master_index.csv
    csv_path = DIRS["production"] / "master_index.csv"
    fieldnames = [
        "chapter_number", "chapter_title", "filename",
        "duration_seconds", "estimated_word_count", "estimated_scene_count",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for ch in chapters:
            writer.writerow({k: ch[k] for k in fieldnames})

    log.info("master_index.csv written → %s", csv_path)

    total = sum(c["duration_seconds"] for c in chapters)
    log.info("Total runtime: %.1f seconds (%.1f minutes)", total, total / 60)

    return chapters
