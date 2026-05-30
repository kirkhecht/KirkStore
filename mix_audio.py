#!/usr/bin/env python3
"""
Genesis Documentary — Background Music & Sound Effects Mixer

Mixes each story video with:
  - Background music (mood-matched, looped to video length, -22dB under voice)
  - Sound effects (scene-matched, looped, -28dB under voice)

Output: project/documentary/stories/mixed/NN_storyname.mp4
"""

import subprocess, sys
from pathlib import Path

STORIES_DIR = Path("project/documentary/stories")
MUSIC_DIR   = Path("project/audio/music")
SFX_DIR     = Path("project/audio/sfx")
OUT_DIR     = Path("project/documentary/stories/mixed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Volume levels (relative to voice at 0dB)
MUSIC_VOL = 0.10   # 10% = roughly -20dB — audible but well under voice
SFX_VOL   = 0.07   # 7%  = roughly -23dB — subtle ambience

# ── Story → music + sfx assignments ──────────────────────────────────────────
# Format: "story_filename": ("music_file", "sfx_file")
ASSIGNMENTS = {
    "01_in_the_beginning.mp4":      ("epic_cosmic.mp3",     "birds_nature.mp3"),
    "02_the_fall.mp4":              ("dark_ominous.mp3",     "wind_forest.mp3"),
    "03_cain_and_abel.mp4":         ("sorrowful.mp3",        "pastoral_animals.mp3"),
    "04_noah_and_the_flood.mp4":    ("dramatic_storm.mp3",   "rain_thunder.mp3"),
    "05_the_tower_of_babel.mp4":    ("mysterious.mp3",       "crowd_city.mp3"),
    "06_calling_of_abram.mp4":      ("journey.mp3",          "desert_wind.mp3"),
    "07_covenant_with_god.mp4":     ("epic_cosmic.mp3",      "fire_crackling.mp3"),
    "08_the_three_visitors.mp4":    ("peaceful_pastoral.mp3","birds_nature.mp3"),
    "09_sodom_and_gomorrah.mp4":    ("dark_ominous.mp3",     "crowd_city.mp3"),
    "10_birth_of_isaac.mp4":        ("joyful.mp3",           "birds_nature.mp3"),
    "11_binding_of_isaac.mp4":      ("tense_suspense.mp3",   "desert_wind.mp3"),
    "12_rebekah_wife_of_isaac.mp4": ("romantic_tender.mp3",  "river_water.mp3"),
    "13_jacob_and_esau.mp4":        ("tense_suspense.mp3",   "pastoral_animals.mp3"),
    "14_jacobs_dream_at_bethel.mp4":("mysterious.mp3",       "wind_forest.mp3"),
    "15_jacob_leah_and_rachel.mp4": ("romantic_tender.mp3",  "river_water.mp3"),
    "16_jacob_wrestles_with_god.mp4":("battle_intense.mp3",  "desert_wind.mp3"),
    "17_joseph_and_his_brothers.mp4":("sorrowful.mp3",       "pastoral_animals.mp3"),
    "18_joseph_in_egypt.mp4":       ("journey.mp3",          "crowd_city.mp3"),
    "19_pharaohs_dreams.mp4":       ("joyful.mp3",           "river_water.mp3"),
}


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def mix_story(story_file, music_file, sfx_file, out_file):
    dur = get_duration(story_file)

    # Build FFmpeg filter:
    # - Loop music & sfx to video duration, fade out last 2s
    # - Mix at low volume under voice
    music_filter = (
        f"[1:a]aloop=loop=-1:size=2e+09,atrim=0:{dur},"
        f"afade=t=out:st={max(0, dur-2):.2f}:d=2,"
        f"volume={MUSIC_VOL}[music]"
    )
    sfx_filter = (
        f"[2:a]aloop=loop=-1:size=2e+09,atrim=0:{dur},"
        f"afade=t=out:st={max(0, dur-2):.2f}:d=2,"
        f"volume={SFX_VOL}[sfx]"
    )
    mix_filter = "[0:a][music][sfx]amix=inputs=3:duration=first:dropout_transition=2[aout]"

    filter_complex = f"{music_filter};{sfx_filter};{mix_filter}"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(story_file),
        "-i", str(music_file),
        "-i", str(sfx_file),
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(out_file),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ✗ FFmpeg error: {r.stderr[-300:]}")
        return False
    return True


def main():
    missing_music = []
    missing_sfx = []

    for story_name, (music, sfx) in ASSIGNMENTS.items():
        mp = MUSIC_DIR / music
        sp = SFX_DIR / sfx
        if not mp.exists(): missing_music.append(music)
        if not sp.exists(): missing_sfx.append(sfx)

    if missing_music or missing_sfx:
        print("Missing audio files — download these first:")
        for m in set(missing_music): print(f"  MUSIC: {m}")
        for s in set(missing_sfx):   print(f"  SFX:   {s}")
        return

    for story_name, (music, sfx) in ASSIGNMENTS.items():
        story_file = STORIES_DIR / story_name
        if not story_file.exists():
            print(f"  Skip (no video): {story_name}")
            continue
        out_file = OUT_DIR / story_name
        if out_file.exists():
            print(f"  [{story_name}] Already done, skipping")
            continue
        print(f"  Mixing: {story_name}...")
        ok = mix_story(story_file, MUSIC_DIR / music, SFX_DIR / sfx, out_file)
        if ok:
            size = out_file.stat().st_size / 1_000_000
            print(f"  ✓ {story_name} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
