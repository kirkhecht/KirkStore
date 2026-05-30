#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 5 — The Tower of Babel (Scenes 1-50)

Pipeline:
  1. ElevenLabs TTS voiceover per scene (David voice)
  2. Ken Burns motion video clip per image
  3. Fade-in / fade-out transitions
  4. Concat into final Chapter 5 MP4

Output: project/documentary/ch05_the_tower_of_babel.mp4
"""

import os, sys, subprocess, requests, argparse, time
from pathlib import Path

IMG_DIR    = Path("project/stories/ch05_babel")
AUDIO_DIR  = Path("project/documentary/ch05/audio")
CLIPS_DIR  = Path("project/documentary/ch05/clips")
OUTPUT_DIR = Path("project/documentary")
FINAL_OUT  = OUTPUT_DIR / "ch05_the_tower_of_babel.mp4"

for d in [AUDIO_DIR, CLIPS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

VOICE_ID    = "BNgbHR0DNeZixGQVzloa"  # David: Deep and Engaging Storyteller
EL_MODEL    = "eleven_multilingual_v2"
SILENCE_PAD = 0.45

FPS  = 25
W, H = 1920, 1080
FADE = 0.25

MOTION = {
    "zoom_in":        "z='min(zoom+0.0007,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    "zoom_out":       "z='if(eq(on,1),1.3,max(1.001,zoom-0.0007))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    "pan_right":      "z='1.18':x='min(iw*(1-1/zoom),0+on*0.5)':y='ih/2-(ih/zoom/2)'",
    "pan_left":       "z='1.18':x='max(0,iw*(1-1/zoom)-on*0.5)':y='ih/2-(ih/zoom/2)'",
    "pan_up":         "z='1.18':x='iw/2-(iw/zoom/2)':y='max(0,ih*(1-1/zoom)-on*0.35)'",
    "pan_down":       "z='1.18':x='iw/2-(iw/zoom/2)':y='min(ih*(1-1/zoom),0+on*0.35)'",
    "drift_right_up": "z='1.2':x='min(iw*(1-1/zoom),0+on*0.4)':y='max(0,ih*(1-1/zoom)-on*0.25)'",
    "zoom_in_up":     "z='min(zoom+0.0007,1.3)':x='iw/2-(iw/zoom/2)':y='max(0,ih/2-(ih/zoom/2)-on*0.15)'",
    "zoom_out_right": "z='if(eq(on,1),1.3,max(1.001,zoom-0.0006))':x='min(iw*(1-1/zoom),iw/2-(iw/zoom/2)+on*0.3)':y='ih/2-(ih/zoom/2)'",
}

SCENES = [
    ("001_babel_title.jpg",               "The Tower of Babel.",                                                                                                    "zoom_in"),
    ("002_rainbow_covenant.jpg",          "The promise God made to Noah was unlike any that had come before.",                                                      "zoom_out"),
    ("003_covenant_for_all_creatures.jpg","It was made not only to one man — but to every living creature.",                                                        "pan_right"),
    ("004_be_fruitful.jpg",               "He gave Noah's family a command — be fruitful. Multiply. Fill the earth.",                                               "zoom_in"),
    ("005_new_permission.jpg",            "He gave them a new permission — they could now eat the meat of animals, as well as plants.",                             "zoom_out"),
    ("006_life_is_sacred.jpg",            "He gave them a warning — life was sacred. Whoever shed the blood of a man, by man would his blood be shed.",             "zoom_in"),
    ("007_sign_in_sky.jpg",               "And then — the rainbow. The sign in the sky. The unbreakable covenant.",                                                 "pan_right"),
    ("008_world_reset.jpg",               "The world had been reset. But the human heart had not been.",                                                            "zoom_out"),
    ("009_noah_plants_vineyard.jpg",      "Not long after the waters dried, Noah planted a vineyard.",                                                              "zoom_in"),
    ("010_years_pass.jpg",                "The vineyard grew. The grapes ripened. And one day, Noah drank too much of its wine.",                                   "zoom_out"),
    ("011_noah_in_tent.jpg",              "He fell asleep — naked — in his tent.",                                                                                  "pan_right"),
    ("012_ham_mocks.jpg",                 "His son Ham saw him there and mocked him.",                                                                              "zoom_in"),
    ("013_shem_japheth_cover.jpg",        "His other two sons — Shem and Japheth — walked in backwards and covered their father without looking.",                  "zoom_out"),
    ("014_sin_remains.jpg",               "The flood had washed away the world. It had not washed away sin.",                                                       "zoom_in"),
    ("015_noahs_death.jpg",               "Noah lived nine hundred and fifty years. And then he died.",                                                             "pan_right"),
    ("016_generations_multiply.jpg",      "The sons of Noah multiplied. They had children. Their children had children.",                                           "zoom_out"),
    ("017_one_language.jpg",              "For a time, they spoke a single language. A single tongue. They could understand each other from coast to coast.",        "zoom_in"),
    ("018_traveling_eastward.jpg",        "As they traveled together — eastward — they came to a wide, flat land.",                                                 "pan_right"),
    ("019_land_of_shinar.jpg",            "A land called Shinar.",                                                                                                  "zoom_out"),
    ("020_they_settled.jpg",              "And there, they settled.",                                                                                               "zoom_in"),
    ("021_ambition_grows.jpg",            "But something had begun to grow in them. Ambition. Pride.",                                                              "zoom_out"),
    ("022_make_a_name.jpg",               "A desire to make a name for themselves.",                                                                                "pan_right"),
    ("023_plan_the_city.jpg",             "They said — come, let us build a city. And a tower. A tower whose top reaches to the heavens.",                          "zoom_in"),
    ("024_not_for_god.jpg",               "A name for themselves. Not for God. For themselves.",                                                                    "zoom_out"),
    ("025_making_bricks.jpg",             "They invented new techniques. They learned to bake bricks instead of cutting stone.",                                    "pan_right"),
    ("026_tar_as_mortar.jpg",             "They used tar instead of mortar.",                                                                                       "zoom_in"),
    ("027_tower_begins.jpg",              "And the tower began to rise.",                                                                                           "zoom_out"),
    ("028_higher_than_before.jpg",        "Higher than anything humanity had ever built.",                                                                          "zoom_in"),
    ("029_monument_to_human_will.jpg",    "A monument to human will.",                                                                                              "pan_right"),
    ("030_finger_at_the_sky.jpg",         "A finger pointing back toward the sky from which the rain had once fallen.",                                             "zoom_out"),
    ("031_god_comes_down.jpg",            "But the Lord came down to see the city and the tower the children of men had built.",                                    "zoom_in"),
    ("032_unified_in_pride.jpg",          "Unified not in worship, but in pride.",                                                                                  "zoom_out"),
    ("033_confusion_begins.jpg",          "So the Creator did something strange. He confused them.",                                                                "pan_right"),
    ("034_language_fractured.jpg",        "In a single moment — in the middle of a workday — language fractured.",                                                  "zoom_in"),
    ("035_scaffold_cannot_understand.jpg","The man on the scaffold could no longer understand the man below.",                                                      "zoom_out"),
    ("036_mason_architect.jpg",           "The mason could not understand the architect.",                                                                          "pan_right"),
    ("037_world_breaks_in_sound.jpg",     "The world broke apart in sound.",                                                                                        "zoom_in"),
    ("038_work_on_tower_stopped.jpg",     "And work on the tower stopped.",                                                                                         "zoom_out"),
    ("039_cannot_speak.jpg",              "They could not finish what they had started. They could not even speak to one another.",                                  "pan_right"),
    ("040_scattering_begins.jpg",         "So they scattered. Family by family. Tribe by tribe. Tongue by tongue.",                                                 "zoom_in"),
    ("041_across_the_plains.jpg",         "Across the plains. Across the mountains. Across the rivers. Across the world.",                                          "zoom_out"),
    ("042_place_called_babel.jpg",        "The place was called Babel — because there the Lord confused the language of all the earth.",                            "zoom_in"),
    ("043_one_people_divided.jpg",        "Humanity — once one people, one tongue, one ambition — was now divided into nations.",                                   "pan_right"),
    ("044_nations_born.jpg",              "This is where the nations of the world were born.",                                                                      "zoom_out"),
    ("045_thousand_languages.jpg",        "This is where the languages of the earth began.",                                                                        "zoom_in"),
    ("046_thousand_kings.jpg",            "From this scattering, a thousand peoples would rise. A thousand tribes. A thousand kings.",                              "zoom_out"),
    ("047_god_choosing.jpg",              "But out of all of them — God was about to choose one man. One family. One people.",                                       "zoom_in"),
    ("048_city_of_ur.jpg",                "Somewhere in the city of Ur, in the land of the Chaldeans, a man was about to hear a voice.",                           "pan_right"),
    ("049_redemption_beginning.jpg",      "Through them — He would begin to do something He had been planning since the gates of Eden.",                            "zoom_out"),
    ("050_creation_coming_back.jpg",      "He was going to bring His creation back.",                                                                               "zoom_in"),
]


def load_env():
    env = {}
    p = Path(".env")
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def generate_tts(text, out_path, key):
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": EL_MODEL,
            "voice_settings": {
                "stability": 0.60,
                "similarity_boost": 0.80,
                "style": 0.15,
                "use_speaker_boost": True,
            },
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs {resp.status_code}: {resp.text[:200]}")
    Path(out_path).write_bytes(resp.content)


def make_clip(img_path, audio_path, out_path, motion, video_dur):
    frames = max(FPS, int(video_dur * FPS))
    zp = MOTION[motion]
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
        f"zoompan={zp}:d={frames}:s={W}x{H}:fps={FPS},"
        f"fade=t=in:st=0:d={FADE},"
        f"fade=t=out:st={video_dur - FADE:.3f}:d={FADE},"
        f"format=yuv420p"
    )
    af = (
        f"apad=pad_dur={video_dur:.3f},atrim=0:{video_dur:.3f},"
        f"afade=t=in:st=0:d=0.1,afade=t=out:st={max(0, video_dur - 0.15):.3f}:d=0.1"
    )
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-i", str(audio_path),
        "-vf", vf, "-af", af,
        "-t", str(video_dur),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(out_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {r.stderr[-400:]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start",      type=int, default=1,  help="Resume from scene N")
    parser.add_argument("--end",        type=int, default=50, help="End at scene N")
    parser.add_argument("--skip-audio", action="store_true",  help="Skip TTS, reuse existing audio")
    parser.add_argument("--skip-clips", action="store_true",  help="Skip clip render, go to assembly")
    args = parser.parse_args()

    env = load_env()
    el_key = env.get("ELEVENLABS_API_KEY", "")
    if not el_key and not args.skip_audio:
        sys.exit("ELEVENLABS_API_KEY not in .env")

    scenes = SCENES[args.start - 1 : args.end]

    if not args.skip_audio:
        print(f"\n{'='*60}\n  Phase 1: TTS voiceover ({len(scenes)} lines)\n{'='*60}")
        for i, (filename, narration, motion) in enumerate(scenes):
            n = args.start + i
            audio_out = AUDIO_DIR / f"{n:03d}.mp3"
            if audio_out.exists():
                print(f"  [{n:03d}] Audio exists, skipping")
                continue
            print(f"  [{n:03d}] \"{narration[:60]}{'…' if len(narration)>60 else ''}\"")
            for attempt in range(3):
                try:
                    generate_tts(narration, audio_out, el_key)
                    print(f"         ✓ {audio_out.stat().st_size // 1024}KB")
                    break
                except Exception as e:
                    print(f"         ✗ Attempt {attempt+1}: {e}")
                    if attempt < 2:
                        time.sleep(5)

    if not args.skip_clips:
        print(f"\n{'='*60}\n  Phase 2: Rendering clips\n{'='*60}")
        for i, (filename, narration, motion) in enumerate(scenes):
            n = args.start + i
            img_path   = IMG_DIR / filename
            audio_path = AUDIO_DIR / f"{n:03d}.mp3"
            clip_path  = CLIPS_DIR / f"{n:03d}.mp4"

            if clip_path.exists():
                print(f"  [{n:03d}] Clip exists, skipping")
                continue
            if not img_path.exists():
                print(f"  [{n:03d}] ✗ Image missing: {filename}")
                continue
            if not audio_path.exists():
                print(f"  [{n:03d}] ✗ Audio missing")
                continue

            dur = get_duration(audio_path) + SILENCE_PAD
            print(f"  [{n:03d}] {filename} ({dur:.2f}s)...")
            try:
                make_clip(img_path, audio_path, clip_path, motion, dur)
                print(f"         ✓ Done")
            except Exception as e:
                print(f"         ✗ {e}")

    print(f"\n{'='*60}\n  Phase 3: Assembly\n{'='*60}")
    clips, missing = [], []
    for i in range(1, 51):
        p = CLIPS_DIR / f"{i:03d}.mp4"
        if p.exists():
            clips.append(p)
        else:
            missing.append(i)

    if missing:
        print(f"  Missing clips: {missing}")
    print(f"  Assembling {len(clips)}/50 clips...")

    list_file = OUTPUT_DIR / "ch05_concat_list.txt"
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-preset", "slow", "-crf", "16",
        "-profile:v", "baseline", "-level", "3.1", "-vsync", "cfr",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Assembly error: {r.stderr[-400:]}")
        return

    size_mb = FINAL_OUT.stat().st_size / 1_000_000
    print(f"\n✓ {FINAL_OUT} ({size_mb:.1f} MB)")

    web_out = OUTPUT_DIR / "ch05_the_tower_of_babel_720p.mp4"
    print("Encoding 720p web version...")
    cmd720 = [
        "ffmpeg", "-y", "-i", str(FINAL_OUT),
        "-vf", "scale=1280:720",
        "-c:v", "libx264", "-preset", "slow", "-crf", "22",
        "-profile:v", "baseline", "-level", "3.1", "-vsync", "cfr",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(web_out),
    ]
    r = subprocess.run(cmd720, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"✓ Web version: {web_out} ({web_out.stat().st_size / 1_000_000:.1f} MB)")
    else:
        print(f"720p encode error: {r.stderr[-200:]}")


if __name__ == "__main__":
    main()
