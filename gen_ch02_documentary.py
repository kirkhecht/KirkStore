#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 2 — The Fall (Scenes 1-55)

Pipeline:
  1. ElevenLabs TTS voiceover per scene (David voice)
  2. Ken Burns motion video clip per image
  3. Fade-in / fade-out transitions
  4. Concat into final Chapter 2 MP4

Output: project/documentary/ch02_the_fall.mp4

Usage:
    python gen_ch02_documentary.py              # full run
    python gen_ch02_documentary.py --skip-audio # re-render video only
    python gen_ch02_documentary.py --start 20   # resume from scene 20
"""

import os, sys, subprocess, requests, argparse, time
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
IMG_DIR   = Path("project/stories/ch02_the_fall")
AUDIO_DIR = Path("project/documentary/ch02/audio")
CLIPS_DIR = Path("project/documentary/ch02/clips")
OUTPUT_DIR = Path("project/documentary")
FINAL_OUT  = OUTPUT_DIR / "ch02_the_fall.mp4"

for d in [AUDIO_DIR, CLIPS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── ElevenLabs config ──────────────────────────────────────────────────────────
VOICE_ID = "kmjgtnoB3DMXA9wZpudu"  # David: Deep and Engaging Storyteller
EL_MODEL = "eleven_multilingual_v2"
SILENCE_PAD = 0.45

# ── Video config ───────────────────────────────────────────────────────────────
FPS  = 25
W, H = 1920, 1080
FADE = 0.25

MOTION = {
    "zoom_in":       "z='min(zoom+0.0007,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    "zoom_out":      "z='if(eq(on,1),1.3,max(1.001,zoom-0.0007))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    "pan_right":     "z='1.18':x='min(iw*(1-1/zoom),0+on*0.5)':y='ih/2-(ih/zoom/2)'",
    "pan_left":      "z='1.18':x='max(0,iw*(1-1/zoom)-on*0.5)':y='ih/2-(ih/zoom/2)'",
    "pan_up":        "z='1.18':x='iw/2-(iw/zoom/2)':y='max(0,ih*(1-1/zoom)-on*0.35)'",
    "pan_down":      "z='1.18':x='iw/2-(iw/zoom/2)':y='min(ih*(1-1/zoom),0+on*0.35)'",
    "drift_right_up":"z='1.2':x='min(iw*(1-1/zoom),0+on*0.4)':y='max(0,ih*(1-1/zoom)-on*0.25)'",
    "zoom_in_up":    "z='min(zoom+0.0007,1.3)':x='iw/2-(iw/zoom/2)':y='max(0,ih/2-(ih/zoom/2)-on*0.15)'",
    "zoom_out_right":"z='if(eq(on,1),1.3,max(1.001,zoom-0.0006))':x='min(iw*(1-1/zoom),iw/2-(iw/zoom/2)+on*0.3)':y='ih/2-(ih/zoom/2)'",
}

# ── Scene manifest: (filename, narration, motion) ─────────────────────────────
SCENES = [
    ("001_the_fall_title.jpg",           "The Fall.",                                                                        "zoom_in"),
    ("002_they_had_everything.jpg",       "They had everything.",                                                             "zoom_out"),
    ("003_garden_without_end.jpg",        "A garden without end,",                                                            "pan_right"),
    ("004_rivers_of_clear_water.jpg",     "rivers of clear water,",                                                           "pan_right"),
    ("005_fruit_heavy_on_branches.jpg",   "fruit heavy on every branch,",                                                     "zoom_in"),
    ("006_animals_that_came_when_called.jpg", "animals that came when called,",                                               "pan_right"),
    ("007_god_walked_cool_of_day.jpg",    "and a God who walked with them in the cool of the day.",                           "zoom_out"),
    ("008_one_thing_not_to_touch.jpg",    "But there was one thing in the garden they had been told not to touch.",           "zoom_in"),
    ("009_one_tree.jpg",                  "One tree.",                                                                        "zoom_in"),
    ("010_that_was_enough.jpg",           "And that was enough.",                                                             "zoom_out"),
    ("011_serpent_most_cunning.jpg",      "The serpent was the most cunning of all the creatures God had made.",              "zoom_in"),
    ("012_serpent_came_to_eve.jpg",       "He came to Eve, not with a threat, but with a question.",                          "pan_right"),
    ("013_did_god_really_say.jpg",        "Did God really say you must not eat from any tree in the garden?",                 "zoom_in"),
    ("014_eve_answered.jpg",              "Eve answered carefully.",                                                           "zoom_out"),
    ("015_may_eat_from_trees.jpg",        "We may eat from the trees of the garden,",                                         "pan_right"),
    ("016_not_from_center_tree.jpg",      "but not from the tree in the center. God said, do not eat from it, or you will die.", "zoom_in"),
    ("017_serpent_smiled.jpg",            "And the serpent smiled.",                                                           "zoom_in"),
    ("018_you_will_not_die.jpg",          "You will not die, he said.",                                                       "zoom_out"),
    ("019_eyes_will_be_opened.jpg",       "God knows that when you eat from it, your eyes will be opened.",                   "zoom_in"),
    ("020_like_god_knowing.jpg",          "And you will be like God, knowing good and evil.",                                 "pan_right"),
    ("021_eve_looked_at_tree.jpg",        "Eve looked at the tree.",                                                          "zoom_in"),
    ("022_fruit_good_for_food.jpg",       "She saw that its fruit was good for food.",                                        "zoom_in"),
    ("023_beautiful_to_the_eye.jpg",      "That it was beautiful to the eye.",                                                "zoom_in"),
    ("024_desirable_for_wisdom.jpg",      "That it was desirable for making one wise.",                                       "zoom_in"),
    ("025_she_reached_out.jpg",           "And she reached out and took it.",                                                 "zoom_in"),
    ("026_she_ate.jpg",                   "She ate.",                                                                         "zoom_in"),
    ("027_gave_some_to_adam.jpg",         "And she gave some to Adam, who was with her.",                                     "pan_right"),
    ("028_and_he_ate.jpg",                "And he ate.",                                                                      "zoom_in"),
    ("029_in_that_instant.jpg",           "In that instant, everything changed.",                                             "zoom_out"),
    ("030_eyes_were_opened.jpg",          "Their eyes were opened.",                                                          "zoom_in"),
    ("031_knew_they_were_naked.jpg",      "And for the first time, they knew they were naked.",                               "zoom_out"),
    ("032_they_were_ashamed.jpg",         "And they were ashamed.",                                                           "zoom_out"),
    ("033_sewed_fig_leaves.jpg",          "They sewed fig leaves together and covered themselves.",                           "zoom_in"),
    ("034_then_they_heard_it.jpg",        "Then they heard it.",                                                              "zoom_in"),
    ("035_sound_of_god_walking.jpg",      "The sound of God walking in the garden in the cool of the evening.",              "zoom_out"),
    ("036_they_hid.jpg",                  "And they hid.",                                                                    "zoom_in"),
    ("037_first_time_hid_from_god.jpg",   "For the first time in their lives, they hid from God.",                           "zoom_out"),
    ("038_where_are_you.jpg",             "Where are you? God called.",                                                       "zoom_in"),
    ("039_adam_i_was_afraid.jpg",         "I heard you in the garden, Adam said. And I was afraid. And I hid.",               "pan_right"),
    ("040_who_told_you_naked.jpg",        "Who told you that you were naked? Have you eaten from the tree?",                  "zoom_in"),
    ("041_woman_you_gave_me.jpg",         "The woman you put here with me — she gave me some fruit from the tree.",          "pan_right"),
    ("042_serpent_deceived_me.jpg",       "The serpent deceived me, Eve said.",                                               "zoom_in"),
    ("043_god_turned_to_serpent.jpg",     "And God turned to the serpent.",                                                   "zoom_in"),
    ("044_cursed_above_all.jpg",          "Cursed are you above all livestock. You will crawl on your belly all the days of your life.", "zoom_out"),
    ("045_enmity_between_you.jpg",        "And I will put enmity between you and the woman, between your offspring and hers.", "pan_right"),
    ("046_greatly_increase_pain.jpg",     "To Eve, God said: I will greatly increase your pain in childbearing.",            "zoom_in"),
    ("047_cursed_is_the_ground.jpg",      "To Adam: Cursed is the ground because of you. Through painful toil you will eat of it.", "zoom_out"),
    ("048_sweat_of_your_brow.jpg",        "By the sweat of your brow you will eat your food,",                               "pan_right"),
    ("049_dust_you_shall_return.jpg",     "For dust you are, and to dust you shall return.",                                  "zoom_in"),
    ("050_garments_of_skin.jpg",          "God made garments of skin for Adam and Eve and clothed them.",                    "zoom_out"),
    ("051_become_like_one_of_us.jpg",     "The man has now become like one of us, knowing good and evil.",                   "zoom_in"),
    ("052_banished_from_eden.jpg",        "So God banished them from the Garden of Eden.",                                   "zoom_out"),
    ("053_adam_looked_back.jpg",          "Adam looked back at the garden for the last time.",                               "pan_left"),
    ("054_cherubim_and_sword.jpg",        "Behind them, God placed cherubim, and a flaming sword flashing back and forth.",  "zoom_out"),
    ("055_they_would_never_return.jpg",   "The gate was closed. They would never return.",                                   "zoom_out"),
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
        capture_output=True, text=True, check=True
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

    # ── Phase 1: TTS ────────────────────────────────────────────────────────────
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

    # ── Phase 2: Clips ──────────────────────────────────────────────────────────
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
                print(f"  [{n:03d}] ✗ Image missing")
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

    # ── Phase 3: Assembly ───────────────────────────────────────────────────────
    print(f"\n{'='*60}\n  Phase 3: Assembly\n{'='*60}")
    clips = []
    missing = []
    for i in range(1, 56):
        p = CLIPS_DIR / f"{i:03d}.mp4"
        if p.exists():
            clips.append(p)
        else:
            missing.append(i)

    if missing:
        print(f"  Missing clips: {missing}")
    print(f"  Assembling {len(clips)}/55 clips...")

    list_file = OUTPUT_DIR / "ch02_concat_list.txt"
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

    web_out = OUTPUT_DIR / "ch02_the_fall_720p.mp4"
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


if __name__ == "__main__":
    main()
