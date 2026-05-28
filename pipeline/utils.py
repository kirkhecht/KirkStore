"""Shared utility functions for the KirkStore pipeline."""
import json
import logging
import re
import sys
from pathlib import Path

from .config import DIRS


def setup_logging(name: str, log_file: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                            datefmt="%H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    if log_file:
        DIRS["logs"].mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(DIRS["logs"] / log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
    return logger


def create_all_dirs() -> None:
    for d in DIRS.values():
        d.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict | list:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: Path, indent: int = 2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def format_duration(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:06.3f}"
    return f"{m:02d}:{s:06.3f}"


def seconds_to_srt(s: float) -> str:
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int(round((s % 1) * 1000))
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def seconds_to_ass(s: float) -> str:
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = s % 60
    return f"{h}:{m:02d}:{sec:05.2f}"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "_", text)
    return text


def wrap_subtitle(text: str, max_chars: int = 42) -> str:
    words = text.split()
    lines, current = [], []
    count = 0
    for w in words:
        if count + len(w) + (1 if current else 0) > max_chars:
            lines.append(" ".join(current))
            current = [w]
            count = len(w)
        else:
            current.append(w)
            count += len(w) + (1 if len(current) > 1 else 0)
    if current:
        lines.append(" ".join(current))
    return "\n".join(lines[:2])  # cap at 2 lines
