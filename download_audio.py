#!/usr/bin/env python3
"""
Download royalty-free music and sound effects for mix_audio.py

Music: Kevin MacLeod (CC-BY) from archive.org
SFX:   Various public domain collections from archive.org
       + FFmpeg synthesis for gaps
"""

import subprocess, urllib.parse
from pathlib import Path

MUSIC_DIR = Path("project/audio/music")
SFX_DIR   = Path("project/audio/sfx")
MUSIC_DIR.mkdir(parents=True, exist_ok=True)
SFX_DIR.mkdir(parents=True, exist_ok=True)

BASE_KM = "https://archive.org/download/KevinMacLeod/Soundtrack"

MUSIC_TRACKS = {
    "epic_cosmic.mp3":      f"{BASE_KM}/Procession%20of%20the%20King.mp3",
    "dark_ominous.mp3":     f"{BASE_KM}/Dark%20Times.mp3",
    "sorrowful.mp3":        f"{BASE_KM}/Lamentation.mp3",
    "dramatic_storm.mp3":   f"{BASE_KM}/Tectonic.mp3",
    "mysterious.mp3":       f"{BASE_KM}/Investigations.mp3",
    "journey.mp3":          f"{BASE_KM}/Long%20Road%20Ahead.mp3",
    "peaceful_pastoral.mp3":f"{BASE_KM}/Serene.mp3",
    "joyful.mp3":           f"{BASE_KM}/Willow%20and%20the%20Light.mp3",
    "tense_suspense.mp3":   f"{BASE_KM}/Crisis.mp3",
    "romantic_tender.mp3":  f"{BASE_KM}/Love%20Song.mp3",
    "battle_intense.mp3":   f"{BASE_KM}/Stoneworld%20Battle.mp3",
}

BASE_PS   = "https://archive.org/download/PureSoundscapes"
BASE_BIRD = "https://archive.org/download/birdsounds_202001"
BASE_FIRE = "https://archive.org/download/fire-sound-effects-crackle-burn-flames-free-cc-0-sfx"

SFX_TRACKS = {
    "birds_nature.mp3": f"{BASE_BIRD}/bird%20sounds%20.mp3",
    "wind_forest.mp3":  f"{BASE_PS}/forrest_walk2_wwind.mp3",
    "rain_thunder.mp3": f"{BASE_PS}/0709_noise_rain_wthunder.mp3",
    "crowd_city.mp3":   f"{BASE_PS}/0709_park_w_people_traffic.mp3",
    "river_water.mp3":  f"{BASE_PS}/forrest_walk_stream.mp3",
    "fire_crackling.mp3": f"{BASE_FIRE}/api%201.mp3",
    # pastoral_animals and desert_wind will be synthesized
}

SYNTH_SFX = {
    "desert_wind.mp3":    "wind",
    "pastoral_animals.mp3": "pastoral",
}


def download(url, dest, timeout=120):
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  ✓ Already have {dest.name} ({dest.stat().st_size//1024}KB)")
        return True
    print(f"  ↓ Downloading {dest.name}...")
    r = subprocess.run(
        ["curl", "-sL", "--max-time", str(timeout),
         "--retry", "3", "--retry-delay", "2",
         "-o", str(dest), url],
        capture_output=True
    )
    if r.returncode != 0 or not dest.exists() or dest.stat().st_size < 5000:
        print(f"  ✗ Failed: {url}")
        if dest.exists():
            dest.unlink()
        return False
    size = dest.stat().st_size // 1024
    print(f"  ✓ {dest.name} ({size}KB)")
    return True


def synth_desert_wind(dest, duration=120):
    """Synthesize desert wind using FFmpeg pink noise + low-pass filter."""
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  ✓ Already have {dest.name}")
        return
    print(f"  ♪ Synthesizing {dest.name}...")
    # Pink noise filtered to sound like distant wind
    filter_str = (
        "anoisesrc=color=pink:amplitude=0.4,"
        "lowpass=f=800,"
        "lowpass=f=600,"
        "highpass=f=80,"
        "volume=0.6"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", filter_str,
        "-t", str(duration),
        "-c:a", "libmp3lame", "-q:a", "4",
        str(dest)
    ], capture_output=True)
    print(f"  ✓ {dest.name} ({dest.stat().st_size//1024}KB)")


def synth_pastoral_animals(dest, duration=120):
    """Synthesize pastoral ambience (outdoor field sounds)."""
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"  ✓ Already have {dest.name}")
        return
    print(f"  ♪ Synthesizing {dest.name}...")
    # Gentle outdoor ambience: light wind + subtle high-frequency nature
    filter_str = (
        "anoisesrc=color=brown:amplitude=0.15,"
        "highpass=f=200,"
        "lowpass=f=3000,"
        "volume=0.5"
    )
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", filter_str,
        "-t", str(duration),
        "-c:a", "libmp3lame", "-q:a", "4",
        str(dest)
    ], capture_output=True)
    print(f"  ✓ {dest.name} ({dest.stat().st_size//1024}KB)")


def verify_audio(path):
    """Quick check that an audio file is valid."""
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True
    )
    try:
        dur = float(r.stdout.strip())
        return dur > 1.0
    except:
        return False


def main():
    print("=== Downloading Music (Kevin MacLeod, CC-BY) ===")
    music_ok = 0
    for name, url in MUSIC_TRACKS.items():
        dest = MUSIC_DIR / name
        if download(url, dest):
            if verify_audio(dest):
                music_ok += 1
            else:
                print(f"  ✗ {name} is not valid audio, removing")
                dest.unlink()

    print(f"\n  Music: {music_ok}/{len(MUSIC_TRACKS)} tracks downloaded")

    print("\n=== Downloading Sound Effects (Public Domain) ===")
    sfx_ok = 0
    for name, url in SFX_TRACKS.items():
        dest = SFX_DIR / name
        if download(url, dest):
            if verify_audio(dest):
                sfx_ok += 1
            else:
                print(f"  ✗ {name} is not valid audio, removing")
                dest.unlink()

    print("\n=== Synthesizing Missing SFX ===")
    synth_desert_wind(SFX_DIR / "desert_wind.mp3")
    synth_pastoral_animals(SFX_DIR / "pastoral_animals.mp3")

    print("\n=== Summary ===")
    print(f"Music:  {len(list(MUSIC_DIR.glob('*.mp3')))} files")
    print(f"SFX:    {len(list(SFX_DIR.glob('*.mp3')))} files")

    # Check what's still missing
    needed_music = set(MUSIC_TRACKS.keys())
    needed_sfx   = set(SFX_TRACKS.keys()) | set(SYNTH_SFX.keys())
    have_music   = {f.name for f in MUSIC_DIR.glob("*.mp3")}
    have_sfx     = {f.name for f in SFX_DIR.glob("*.mp3")}

    missing_m = needed_music - have_music
    missing_s = needed_sfx   - have_sfx
    if missing_m:
        print(f"\nStill missing music: {missing_m}")
    if missing_s:
        print(f"Still missing SFX:   {missing_s}")
    if not missing_m and not missing_s:
        print("\n✓ All audio files ready — run: python mix_audio.py")


if __name__ == "__main__":
    main()
