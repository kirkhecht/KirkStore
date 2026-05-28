#!/usr/bin/env python3
"""
KirkStore Documentary Production Pipeline
==========================================
Orchestrates all 8 phases of post-narration production.

Usage:
  python run_pipeline.py --source-dir /path/to/your/mp3s
  python run_pipeline.py --demo          # run with built-in demo data
  python run_pipeline.py --demo --ai     # demo + Claude API prompts
  python run_pipeline.py --source-dir /path/to/mp3s --whisper medium
  python run_pipeline.py --source-dir /path/to/mp3s --skip-transcription

Options:
  --source-dir PATH    Directory containing your ElevenLabs MP3 files
  --demo               Run the full pipeline on synthetic demo data
  --ot                 Enable Old Testament mode: structured sections + OT visual prompts
  --whisper MODEL      Whisper model to use (tiny|base|small|medium|large) [default: base]
  --ai                 Use Claude API for image prompt generation (requires ANTHROPIC_API_KEY)
  --skip-transcription Skip Whisper transcription (useful if transcripts already exist)
  --phases LIST        Comma-separated phases to run, e.g. 1,2,3  [default: all]
  --project-root PATH  Override project output directory [default: ./project]
"""

import argparse
import os
import sys
import time
from pathlib import Path

# ── Load .env if present ───────────────────────────────────────────────────────
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

# ── Setup project root before importing pipeline modules ──────────────────────
def _parse_project_root() -> None:
    for i, arg in enumerate(sys.argv):
        if arg == "--project-root" and i + 1 < len(sys.argv):
            os.environ["KIRKSTORE_PROJECT_ROOT"] = sys.argv[i + 1]
            break

_parse_project_root()

from pipeline import (
    phase1_organize,
    phase2_analyze,
    phase3_segment,
    phase4_prompts,
    phase5_subtitles,
    phase6_ffmpeg,
    phase7_dashboard,
    phase8_images,
)
from pipeline.config import DIRS, WHISPER_MODEL
from pipeline.utils import create_all_dirs, setup_logging

log = setup_logging("pipeline", "pipeline.log")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="KirkStore Documentary Production Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--source-dir",  type=Path, default=None,
                   help="Directory containing ElevenLabs MP3 narration files")
    p.add_argument("--demo",        action="store_true",
                   help="Run with built-in demo data (no real MP3s needed)")
    p.add_argument("--ot",          action="store_true",
                   help="Old Testament mode: load section structure + use OT visual guide")
    p.add_argument("--whisper",     default=WHISPER_MODEL,
                   choices=["tiny", "base", "small", "medium", "large"],
                   help="Whisper model size (default: base)")
    p.add_argument("--ai",          action="store_true",
                   help="Enable Claude API for image prompt generation")
    p.add_argument("--skip-transcription", action="store_true",
                   help="Skip Whisper step (use existing transcripts)")
    p.add_argument("--phases",      default="1,2,3,4,5,6,7,8",
                   help="Comma-separated phase numbers to run (default: all)")
    p.add_argument("--project-root", type=Path, default=None,
                   help="Override project output directory")
    return p.parse_args()


def banner(msg: str) -> None:
    bar = "─" * 60
    log.info(bar)
    log.info("  %s", msg)
    log.info(bar)


def main() -> None:
    args = parse_args()
    start_time = time.time()

    # Apply CLI overrides to config
    if args.whisper:
        os.environ["WHISPER_MODEL"] = args.whisper
    if args.ai and os.getenv("ANTHROPIC_API_KEY"):
        import pipeline.config as cfg
        cfg.USE_AI_PROMPTS = True
    elif args.ai:
        log.warning("--ai flag set but ANTHROPIC_API_KEY not found. Heuristic prompts will be used.")

    phases = set(int(x) for x in args.phases.split(",") if x.strip().isdigit())

    # ── Initialise directories ────────────────────────────────────────────────
    create_all_dirs()

    # ── Phase 1 — File Organisation ──────────────────────────────────────────
    chapters: list[dict] = []
    if args.demo:
        banner("DEMO MODE — using built-in synthetic chapters")
        from pipeline.demo_data import run as demo_run
        chapters = demo_run()
        log.info("Demo chapters ready: %d", len(chapters))
    elif 1 in phases:
        if not args.source_dir:
            log.error("--source-dir is required (or use --demo)")
            sys.exit(1)
        banner("Phase 1 — File Organisation")
        chapters = phase1_organize.run(args.source_dir)
        if not chapters:
            log.error("No audio files found. Exiting.")
            sys.exit(1)
    else:
        log.warning("Phase 1 skipped — chapters list will be empty if no prior run.")

    # ── Phase 2 — Audio Analysis ──────────────────────────────────────────────
    if 2 in phases and not args.skip_transcription:
        banner("Phase 2 — Audio Analysis")
        chapters = phase2_analyze.run(chapters)
    elif args.skip_transcription:
        log.info("Phase 2 skipped (--skip-transcription)")
        # Patch transcript paths for downstream phases
        for ch in chapters:
            tp = DIRS["transcripts"] / f"chapter_{ch['chapter_number']:02d}.json"
            if tp.exists():
                ch["transcript_path"] = str(tp)

    # ── OT mode: load structured chapter/section data ────────────────────────
    ot_chapters: dict = {}
    if args.ot:
        banner("OT Mode — Loading scripture structure")
        from pipeline.parse_script import run as ot_script_run
        ot_list = ot_script_run()
        ot_chapters = {c["chapter_number"]: c for c in ot_list}
        log.info("OT chapters loaded: %d chapters, %d total sections",
                 len(ot_chapters),
                 sum(len(c["sections"]) for c in ot_list))

    # ── Phase 3 — Scene Segmentation ─────────────────────────────────────────
    all_scenes: dict[int, list[dict]] = {}
    if 3 in phases:
        banner("Phase 3 — Scene Segmentation")
        all_scenes = phase3_segment.run(chapters, ot_chapters=ot_chapters or None)
    else:
        # Load saved scene JSONs so downstream phases (4–8) can run standalone
        from pipeline.utils import load_json
        import re as _re
        for p in sorted(DIRS["scene_json"].glob("chapter_*_scenes.json")):
            m = _re.search(r"chapter_(\d+)_scenes", p.name)
            if m:
                num = int(m.group(1))
                all_scenes[num] = load_json(p)
        if all_scenes:
            log.info("Loaded %d chapters of scenes from disk (%d total scenes)",
                     len(all_scenes), sum(len(s) for s in all_scenes.values()))

    # ── Phase 4 — Image Prompt Generation ────────────────────────────────────
    if 4 in phases and all_scenes:
        banner("Phase 4 — Image Prompt Generation")
        all_scenes = phase4_prompts.run(all_scenes, use_ot=args.ot)

    # ── Phase 5 — Subtitle Generation ────────────────────────────────────────
    if 5 in phases and all_scenes:
        banner("Phase 5 — Subtitle Generation")
        phase5_subtitles.run(all_scenes, chapters)

    # ── Phase 6 — FFmpeg Preparation ─────────────────────────────────────────
    if 6 in phases and all_scenes:
        banner("Phase 6 — FFmpeg Preparation")
        phase6_ffmpeg.run(chapters, all_scenes)

    # ── Phase 7 — Production Dashboard ───────────────────────────────────────
    if 7 in phases:
        banner("Phase 7 — Production Dashboard")
        phase7_dashboard.run(chapters, all_scenes)

    # ── Phase 8 — Image Generation ────────────────────────────────────────────
    if 8 in phases and all_scenes:
        banner("Phase 8 — Image Generation (Flux Dev via Replicate)")
        phase8_images.run(all_scenes)

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed = time.time() - start_time
    total_scenes = sum(len(s) for s in all_scenes.values())
    total_runtime = sum(c.get("duration_seconds", 0) for c in chapters)

    banner("Pipeline Complete")
    log.info("Chapters processed : %d", len(chapters))
    log.info("Total narration    : %.1f min", total_runtime / 60)
    log.info("Scenes segmented   : %d", total_scenes)
    log.info("Images required    : %d", total_scenes)
    log.info("Pipeline time      : %.1fs", elapsed)
    log.info("")
    log.info("Key outputs:")
    log.info("  %-40s %s", "Master index",   DIRS["production"] / "master_index.csv")
    log.info("  %-40s %s", "Scene timeline", DIRS["scene_json"]  / "scene_timeline.json")
    log.info("  %-40s %s", "Image prompts",  DIRS["image_prompts"] / "image_prompts.csv")
    log.info("  %-40s %s", "Subtitles (SRT)",DIRS["subtitles"]   / "master.srt")
    log.info("  %-40s %s", "FFmpeg plan",    DIRS["ffmpeg"]      / "ffmpeg_plan.json")
    log.info("  %-40s %s", "Assembly script",DIRS["ffmpeg"]      / "assemble_video.sh")
    log.info("  %-40s %s", "Production report", DIRS["production"] / "production_report.md")
    log.info("  %-40s %s", "Generated images",  DIRS["images"])
    log.info("")
    log.info("Next step: run:  bash project/ffmpeg/assemble_video.sh")


if __name__ == "__main__":
    main()
