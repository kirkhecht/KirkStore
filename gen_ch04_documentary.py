#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 4 — Noah and the Flood (Scenes 1-55)

Pipeline:
  1. ElevenLabs TTS voiceover per scene (David voice)
  2. Ken Burns motion video clip per image
  3. Fade-in / fade-out transitions
  4. Concat into final Chapter 4 MP4

Output: project/documentary/ch04_noah_and_the_flood.mp4

Usage:
    python gen_ch04_documentary.py              # full run
    python gen_ch04_documentary.py --skip-audio # re-render video only
    python gen_ch04_documentary.py --start 20   # resume from scene 20
"""

import os, sys, subprocess, requests, argparse, time
from pathlib import Path

IMG_DIR    = Path("project/stories/ch04_noah")
AUDIO_DIR  = Path("project/documentary/ch04/audio")
CLIPS_DIR  = Path("project/documentary/ch04/clips")
OUTPUT_DIR = Path("project/documentary")
FINAL_OUT  = OUTPUT_DIR / "ch04_noah_and_the_flood.mp4"

for d in [AUDIO_DIR, CLIPS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

VOICE_ID    = "kmjgtnoB3DMXA9wZpudu"  # David: Deep and Engaging Storyteller
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
    ("001_noah_title.jpg",                  "Noah.",                                                                                                                                     "zoom_in"),
    ("002_world_became_wicked.jpg",          "The world God had made became corrupted.",                                                                                                  "zoom_out"),
    ("003_wickedness_of_man.jpg",            "The wickedness of man was great upon the earth.",                                                                                           "zoom_in"),
    ("004_every_intention_evil.jpg",         "And every intention of man's heart was only evil, continually.",                                                                            "pan_right"),
    ("005_lord_saw_and_grieved.jpg",         "The Lord saw this. And his heart was deeply troubled.",                                                                                     "zoom_out"),
    ("006_will_wipe_from_earth.jpg",         "I will wipe from the face of the earth the human race I have created.",                                                                    "zoom_in"),
    ("007_but_noah_was_different.jpg",       "But Noah was different.",                                                                                                                   "zoom_out"),
    ("008_noah_found_favor.jpg",             "Noah found favor in the eyes of the Lord.",                                                                                                 "zoom_in"),
    ("009_noah_was_righteous.jpg",           "He was a righteous man, blameless among the people of his time.",                                                                          "pan_right"),
    ("010_noah_walked_with_god.jpg",         "And Noah walked with God.",                                                                                                                 "zoom_out"),
    ("011_god_spoke_to_noah.jpg",            "God said to Noah: I am going to put an end to all people.",                                                                                "zoom_in"),
    ("012_build_an_ark.jpg",                 "So make yourself an ark of cypress wood.",                                                                                                  "zoom_out"),
    ("013_ark_dimensions.jpg",               "Make it three hundred cubits long, fifty wide, and thirty high.",                                                                          "pan_right"),
    ("014_noah_obeyed.jpg",                  "Noah did everything just as God commanded him.",                                                                                            "zoom_in"),
    ("015_noah_building_ark.jpg",            "He built the ark with his sons, beam by beam, plank by plank.",                                                                            "pan_right"),
    ("016_animals_coming.jpg",               "Then God said: bring two of every living creature into the ark.",                                                                          "zoom_out"),
    ("017_two_by_two.jpg",                   "Two by two they came — every creature of the earth.",                                                                                      "pan_right"),
    ("018_male_and_female.jpg",              "Male and female, every kind.",                                                                                                              "zoom_in"),
    ("019_enter_the_ark.jpg",                "Then the Lord said: Go into the ark, you and your whole family.",                                                                          "zoom_out"),
    ("020_noahs_family_entered.jpg",         "Noah entered the ark, and his sons, his wife, and his sons' wives.",                                                                       "pan_right"),
    ("021_god_shut_the_door.jpg",            "Then the Lord shut them in.",                                                                                                               "zoom_in"),
    ("022_seven_days_waiting.jpg",           "For seven days, nothing happened.",                                                                                                         "zoom_out"),
    ("023_the_rain_began.jpg",               "And then the rain began.",                                                                                                                  "zoom_in"),
    ("024_forty_days_nights.jpg",            "For forty days and forty nights, the rain fell.",                                                                                          "zoom_out"),
    ("025_waters_rose.jpg",                  "The waters rose and increased greatly on the earth.",                                                                                       "pan_right"),
    ("026_mountains_covered.jpg",            "They rose and covered the mountains to a depth of more than fifteen cubits.",                                                              "zoom_out"),
    ("027_everything_perished.jpg",          "Every living thing that moved on land perished.",                                                                                           "zoom_in"),
    ("028_ark_floated.jpg",                  "But the ark floated on the surface of the water.",                                                                                         "pan_right"),
    ("029_god_remembered_noah.jpg",          "But God remembered Noah.",                                                                                                                  "zoom_in"),
    ("030_wind_sent_over_earth.jpg",         "And God sent a wind over the earth, and the waters receded.",                                                                              "zoom_out"),
    ("031_waters_receded.jpg",               "The waters receded steadily from the earth.",                                                                                               "pan_right"),
    ("032_ark_rested_on_ararat.jpg",         "And on the seventeenth day, the ark came to rest on the mountains of Ararat.",                                                             "zoom_out"),
    ("033_mountaintops_appeared.jpg",        "The tops of the mountains became visible.",                                                                                                 "zoom_in"),
    ("034_noah_opened_window.jpg",           "After forty more days, Noah opened the window of the ark.",                                                                                "zoom_in"),
    ("035_sent_out_raven.jpg",               "He sent out a raven, and it kept flying back and forth.",                                                                                  "pan_right"),
    ("036_sent_out_dove.jpg",                "Then he sent out a dove to see if the water had receded.",                                                                                 "zoom_out"),
    ("037_dove_returned.jpg",                "But the dove could find no place to set its feet. It returned.",                                                                           "zoom_in"),
    ("038_noah_reached_out.jpg",             "Noah reached out his hand and brought it back inside the ark.",                                                                            "zoom_in"),
    ("039_second_dove.jpg",                  "He waited seven days and sent the dove out again.",                                                                                        "zoom_out"),
    ("040_dove_with_olive_branch.jpg",       "This time, the dove returned with a fresh olive leaf in its beak.",                                                                        "zoom_in"),
    ("041_noah_knew.jpg",                    "Then Noah knew that the water had receded from the earth.",                                                                                "zoom_in"),
    ("042_third_dove_sent.jpg",              "He waited seven more days and sent the dove again.",                                                                                       "zoom_out"),
    ("043_dove_did_not_return.jpg",          "This time it did not return.",                                                                                                              "pan_right"),
    ("044_god_said_come_out.jpg",            "Then God said to Noah: Come out of the ark.",                                                                                              "zoom_out"),
    ("045_noah_emerged.jpg",                 "So Noah came out, together with his sons and his wife and his sons' wives.",                                                               "pan_right"),
    ("046_animals_came_out.jpg",             "And all the animals and creatures came out of the ark.",                                                                                   "zoom_out"),
    ("047_noah_built_altar.jpg",             "Then Noah built an altar to the Lord.",                                                                                                    "zoom_in"),
    ("048_burnt_offering.jpg",               "And taking some of all the clean animals and birds, he sacrificed burnt offerings.",                                                       "zoom_out"),
    ("049_pleasing_aroma.jpg",               "The Lord smelled the pleasing aroma.",                                                                                                     "zoom_in"),
    ("050_never_again_curse_ground.jpg",     "Never again will I curse the ground because of humans.",                                                                                   "pan_right"),
    ("051_as_long_as_earth_endures.jpg",     "As long as the earth endures, seedtime and harvest, cold and heat, summer and winter, day and night will never cease.",                   "zoom_out"),
    ("052_rainbow_in_clouds.jpg",            "I have set my rainbow in the clouds.",                                                                                                     "zoom_in"),
    ("053_sign_of_covenant.jpg",             "It will be a sign of the covenant between me and the earth.",                                                                              "zoom_out"),
    ("054_whenever_rainbow_appears.jpg",     "Whenever I bring clouds over the earth and the rainbow appears, I will remember my covenant.",                                             "zoom_in"),
    ("055_never_again_flood.jpg",            "And the waters will never again become a flood to destroy all life. The promise was made. And the earth began again.",                    "zoom_out"),
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
                "stability": 0.55,
                "similarity_boost": 0.80,
                "style": 0.35,
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
    parser.add_argument("--end",        type=int, default=55, help="End at scene N")
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
    for i in range(1, 56):
        p = CLIPS_DIR / f"{i:03d}.mp4"
        if p.exists():
            clips.append(p)
        else:
            missing.append(i)

    if missing:
        print(f"  Missing clips: {missing}")
    print(f"  Assembling {len(clips)}/55 clips...")

    list_file = OUTPUT_DIR / "ch04_concat_list.txt"
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in clips))

    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"Assembly error: {r.stderr[-400:]}")
        return

    size_mb = FINAL_OUT.stat().st_size / 1024 / 1024
    print(f"\n✓ {FINAL_OUT} ({size_mb:.1f} MB)")

    web_out = OUTPUT_DIR / "ch04_noah_and_the_flood_720p.mp4"
    print("Encoding 720p web version...")
    r2 = subprocess.run([
        "ffmpeg", "-y", "-i", str(FINAL_OUT),
        "-vf", "scale=1280:720", "-c:v", "libx264", "-profile:v", "baseline",
        "-level", "3.1", "-crf", "28", "-preset", "fast",
        "-c:a", "aac", "-b:a", "96k", "-ar", "44100",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(web_out),
    ], capture_output=True, text=True)
    if r2.returncode == 0:
        print(f"✓ Web version: {web_out} ({web_out.stat().st_size/1024/1024:.1f} MB)")

    story_out = Path("project/documentary/stories/04_noah_and_the_flood.mp4")
    story_out.parent.mkdir(parents=True, exist_ok=True)
    print(f"Encoding story file (04_noah_and_the_flood.mp4)...")
    r3 = subprocess.run([
        "ffmpeg", "-y", "-i", str(FINAL_OUT),
        "-c:v", "libx264", "-b:v", "600k", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(story_out),
    ], capture_output=True, text=True)
    if r3.returncode == 0:
        print(f"✓ {story_out} ({story_out.stat().st_size/1_000_000:.1f} MB)")
    else:
        print(f"✗ Story encode failed: {r3.stderr[-200:]}")


if __name__ == "__main__":
    main()
