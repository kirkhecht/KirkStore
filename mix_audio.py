#!/usr/bin/env python3
"""
Genesis Documentary — Background Music & Sound Effects Mixer v2

Changes from v1:
- SFX volume 7% → 12%
- Dynamic multi-segment music for 10 stories (emotional arcs)
- Upgraded tracks: Dreamlike (mysterious), Serpentine Trek (journey),
  Eternal Hope (joyful), Five Armies (battle)
- Story 01 video re-encoded at 380k to be openable (<22MB)
- Audio bitrate 128k → 96k (matches reference quality, saves ~1MB/story)
"""

import subprocess, sys
from pathlib import Path

STORIES_DIR = Path("project/documentary/stories")
MUSIC_DIR   = Path("project/audio/music")
SFX_DIR     = Path("project/audio/sfx")
OUT_DIR     = Path("project/documentary/stories/mixed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

MUSIC_VOL = 0.205
SFX_VOL   = 0.15   # raised from 0.07

# Assignments:
#   tuple  → ("music.mp3", "sfx.mp3")  single track, stream-copy video
#   dict   → {
#               "music": [(start, end_or_None, "track.mp3"), ...],
#               "sfx": "sfx.mp3",
#               "video_bitrate": "380k"   # optional, triggers video re-encode
#            }
ASSIGNMENTS = {
    "01_in_the_beginning.mp4": {
        "music": [
            (0,   160, "peaceful_pastoral.mp3"),  # Void → first days of creation
            (160, None,"epic_cosmic.mp3"),          # Mankind breathed into life
        ],
        "sfx": "birds_nature.mp3",
        "video_bitrate": "380k",
    },
    "02_the_fall.mp4": {
        "music": [
            (0,   65,  "peaceful_pastoral.mp3"),  # Garden of Eden, beauty
            (65,  135, "mysterious.mp3"),           # Serpent arrives, temptation
            (135, None,"sorrowful.mp3"),            # Fall, curse, expulsion
        ],
        "sfx": "wind_forest.mp3",
    },
    "03_cain_and_abel.mp4": {
        "music": [
            (0,   75,  "peaceful_pastoral.mp3"),  # Brothers, offerings to God
            (75,  None,"sorrowful.mp3"),            # Jealousy, murder, exile
        ],
        "sfx": "pastoral_animals.mp3",
    },
    "04_noah_and_the_flood.mp4": {
        "music": [
            (0,   55,  "dark_ominous.mp3"),        # Wickedness, God grieves
            (55,  175, "dramatic_storm.mp3"),       # Ark, flood, forty days
            (175, None,"epic_cosmic.mp3"),           # Dove, rainbow, covenant
        ],
        "sfx": "rain_thunder.mp3",
    },
    "05_the_tower_of_babel.mp4": {
        "music": [
            (0,   100, "mysterious.mp3"),           # One language, proud builders
            (100, None,"dark_ominous.mp3"),          # God confuses, scatters
        ],
        "sfx": "crowd_city.mp3",
    },
    "06_calling_of_abram.mp4":      ("journey.mp3",           "desert_wind.mp3"),
    "07_covenant_with_god.mp4": {
        "music": [
            (0,   45,  "journey.mp3"),              # Abram waits, God speaks
            (45,  None,"epic_cosmic.mp3"),           # Stars, covenant, circumcision
        ],
        "sfx": "fire_crackling.mp3",
    },
    "08_the_three_visitors.mp4":    ("peaceful_pastoral.mp3", "birds_nature.mp3"),
    "09_sodom_and_gomorrah.mp4": {
        "music": [
            (0,   40,  "mysterious.mp3"),           # Angels arrive, Lot's hospitality
            (40,  None,"dark_ominous.mp3"),          # Mob violence, fire and brimstone
        ],
        "sfx": "crowd_city.mp3",
    },
    "10_birth_of_isaac.mp4":        ("joyful.mp3",            "birds_nature.mp3"),
    "11_binding_of_isaac.mp4": {
        "music": [
            (0,   50,  "tense_suspense.mp3"),       # God's command, three-day journey
            (50,  None,"epic_cosmic.mp3"),           # Binding, angel intervenes, ram
        ],
        "sfx": "desert_wind.mp3",
    },
    "12_rebekah_wife_of_isaac.mp4": ("romantic_tender.mp3",   "river_water.mp3"),
    "13_jacob_and_esau.mp4": {
        "music": [
            (0,   55,  "peaceful_pastoral.mp3"),    # Birth, twins, childhood
            (55,  None,"tense_suspense.mp3"),        # Birthright sold, stolen blessing
        ],
        "sfx": "pastoral_animals.mp3",
    },
    "14_jacobs_dream_at_bethel.mp4": ("mysterious.mp3",       "wind_forest.mp3"),
    "15_jacob_leah_and_rachel.mp4":  ("romantic_tender.mp3",  "river_water.mp3"),
    "16_jacob_wrestles_with_god.mp4": {
        "music": [
            (0,   30,  "mysterious.mp3"),           # Night, alone at the ford
            (30,  None,"battle_intense.mp3"),        # Wrestling until dawn
        ],
        "sfx": "desert_wind.mp3",
    },
    "17_joseph_and_his_brothers.mp4": {
        "music": [
            (0,   55,  "romantic_tender.mp3"),      # Beloved son, coat of colors
            (55,  None,"sorrowful.mp3"),             # Betrayal, pit, sold into slavery
        ],
        "sfx": "pastoral_animals.mp3",
    },
    "18_joseph_in_egypt.mp4":       ("journey.mp3",           "crowd_city.mp3"),
    "19_pharaohs_dreams.mp4": {
        "music": [
            (0,   70,  "mysterious.mp3"),           # Prison, troubled dreams
            (70,  None,"joyful.mp3"),               # Joseph interprets, exalted
        ],
        "sfx": "river_water.mp3",
    },
}


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True)
    return float(r.stdout.strip())


def mix_story(story_file, music_assign, sfx_name, out_file, video_bitrate=None):
    dur = get_duration(story_file)
    FADE = 2.5

    if isinstance(music_assign, list):
        inputs = ["-i", str(story_file)]
        filter_parts = []

        for i, (seg_start, seg_end, music_file) in enumerate(music_assign):
            seg_dur = max(0.5, (seg_end if seg_end is not None else dur) - seg_start)
            inputs += ["-i", str(MUSIC_DIR / music_file)]

            f = (
                f"[{i+1}:a]aloop=loop=-1:size=2e+09,"
                f"atrim=0:{seg_dur:.3f},"
                f"asetpts=PTS-STARTPTS,"
                f"aformat=sample_rates=44100:channel_layouts=stereo"
            )
            if i > 0:
                f += f",afade=t=in:st=0:d={FADE:.2f}"
            f += f",afade=t=out:st={max(0, seg_dur - FADE):.3f}:d={FADE:.2f}"
            f += f"[ms{i}]"
            filter_parts.append(f)

        n = len(music_assign)
        sfx_idx = n + 1
        refs = "".join(f"[ms{i}]" for i in range(n))
        filter_parts.append(f"{refs}concat=n={n}:v=0:a=1[mconcat]")
        filter_parts.append(
            f"[mconcat]afade=t=out:st={max(0,dur-2):.2f}:d=2,"
            f"volume={MUSIC_VOL}[music]"
        )
    else:
        inputs = ["-i", str(story_file), "-i", str(MUSIC_DIR / music_assign)]
        sfx_idx = 2
        filter_parts = [
            f"[1:a]aloop=loop=-1:size=2e+09,"
            f"atrim=0:{dur:.3f},"
            f"asetpts=PTS-STARTPTS,"
            f"afade=t=out:st={max(0,dur-2):.2f}:d=2,"
            f"volume={MUSIC_VOL}[music]"
        ]

    inputs += ["-i", str(SFX_DIR / sfx_name)]
    filter_parts.append(
        f"[{sfx_idx}:a]aloop=loop=-1:size=2e+09,"
        f"atrim=0:{dur:.3f},"
        f"asetpts=PTS-STARTPTS,"
        f"afade=t=out:st={max(0,dur-2):.2f}:d=2,"
        f"volume={SFX_VOL}[sfx]"
    )
    filter_parts.append(
        "[0:a][music][sfx]amix=inputs=3:duration=first:dropout_transition=2[aout]"
    )

    filter_complex = ";".join(filter_parts)
    v_opts = (["-c:v", "libx264", "-b:v", video_bitrate, "-preset", "fast"]
              if video_bitrate else ["-c:v", "copy"])

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[aout]",
        *v_opts,
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        str(out_file),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ✗ FFmpeg error:\n{r.stderr[-500:]}")
        return False
    return True


def main():
    all_music, all_sfx = set(), set()
    for assignment in ASSIGNMENTS.values():
        if isinstance(assignment, tuple):
            all_music.add(assignment[0])
            all_sfx.add(assignment[1])
        else:
            all_sfx.add(assignment["sfx"])
            m = assignment["music"]
            if isinstance(m, list):
                for _, _, t in m: all_music.add(t)
            else:
                all_music.add(m)

    missing = []
    for f in all_music:
        if not (MUSIC_DIR / f).exists(): missing.append(f"MUSIC: {f}")
    for f in all_sfx:
        if not (SFX_DIR / f).exists():   missing.append(f"SFX:   {f}")
    if missing:
        print("Missing files:\n  " + "\n  ".join(sorted(missing)))
        return

    for story_name, assignment in ASSIGNMENTS.items():
        story_file = STORIES_DIR / story_name
        if not story_file.exists():
            print(f"  Skip (no video): {story_name}")
            continue

        out_file = OUT_DIR / story_name
        if out_file.exists():
            print(f"  [skip] {story_name}")
            continue

        if isinstance(assignment, tuple):
            music_assign, sfx_name = assignment
            video_bitrate = None
        else:
            music_assign  = assignment["music"]
            sfx_name      = assignment["sfx"]
            video_bitrate = assignment.get("video_bitrate")

        print(f"  Mixing: {story_name}...")
        ok = mix_story(story_file, music_assign, sfx_name, out_file, video_bitrate)
        if ok:
            size = out_file.stat().st_size / 1_000_000
            print(f"  ✓ {story_name} ({size:.1f} MB)")


if __name__ == "__main__":
    main()
