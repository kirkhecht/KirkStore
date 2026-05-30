#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 3 — Cain and Abel (Scenes 1-55)

Pipeline:
  1. ElevenLabs TTS voiceover per scene (David voice)
  2. Ken Burns motion video clip per image
  3. Fade-in / fade-out transitions
  4. Concat into final Chapter 3 MP4

Output: project/documentary/ch03_cain_and_abel.mp4

Usage:
    python gen_ch03_documentary.py              # full run
    python gen_ch03_documentary.py --skip-audio # re-render video only
    python gen_ch03_documentary.py --start 20   # resume from scene 20
"""

import os, sys, subprocess, requests, argparse, time
from pathlib import Path

IMG_DIR    = Path("project/stories/ch03_cain_abel")
AUDIO_DIR  = Path("project/documentary/ch03/audio")
CLIPS_DIR  = Path("project/documentary/ch03/clips")
OUTPUT_DIR = Path("project/documentary")
FINAL_OUT  = OUTPUT_DIR / "ch03_cain_and_abel.mp4"

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

# ── Scene manifest: (filename, narration, motion) ─────────────────────────────
SCENES = [
    ("001_cain_abel_title.jpg",           "Cain and Abel.",                                                                                  "zoom_in"),
    ("002_outside_eden_hard.jpg",          "Outside the garden, life was hard.",                                                              "zoom_out"),
    ("003_ground_demands_everything.jpg",  "The ground that had once given freely now demanded everything.",                                   "zoom_in"),
    ("004_adam_works_soil.jpg",            "Adam worked the soil with sweat and pain, just as God had said.",                                  "pan_right"),
    ("005_eve_bears_children.jpg",         "Eve bore children into this new and broken world.",                                                "zoom_in"),
    ("006_first_son_named_cain.jpg",       "Her first son, she named Cain.",                                                                  "zoom_in"),
    ("007_with_help_of_lord.jpg",          "With the help of the Lord, she said. I have brought forth a man.",                                 "zoom_out"),
    ("008_then_bore_abel.jpg",             "Then she bore another son.",                                                                      "pan_right"),
    ("009_named_him_abel.jpg",             "She named him Abel.",                                                                             "zoom_in"),
    ("010_two_brothers_two_paths.jpg",     "Two brothers. Two paths.",                                                                        "zoom_out"),
    ("011_abel_became_shepherd.jpg",       "Abel became a shepherd, tending his flocks under the open sky.",                                   "pan_right"),
    ("012_cain_became_farmer.jpg",         "Cain became a farmer, working the cursed earth with his hands.",                                   "pan_left"),
    ("013_both_brought_offerings.jpg",     "In time, both brothers brought an offering to God.",                                               "zoom_out"),
    ("014_cains_offering_grain.jpg",       "Cain brought the fruits of the soil — a harvest offering.",                                        "zoom_in"),
    ("015_abels_offering_flock.jpg",       "Abel brought fat portions from the firstborn of his flock.",                                       "zoom_in"),
    ("016_god_accepted_abel.jpg",          "And the Lord looked with favor on Abel and his offering.",                                         "zoom_out"),
    ("017_god_rejected_cain.jpg",          "But on Cain and his offering, the Lord did not look with favor.",                                  "zoom_in"),
    ("018_cain_was_angry.jpg",             "And Cain was very angry.",                                                                        "zoom_in"),
    ("019_cains_face_fell.jpg",            "His face fell.",                                                                                  "zoom_in"),
    ("020_why_are_you_angry.jpg",          "Why are you angry? God asked. Why is your face downcast?",                                         "zoom_out"),
    ("021_if_you_do_right.jpg",            "If you do what is right, will you not be accepted?",                                              "pan_right"),
    ("022_sin_crouching_at_door.jpg",      "But if you do not do what is right, sin is crouching at your door.",                              "zoom_in"),
    ("023_sin_desires_to_have_you.jpg",    "It desires to have you.",                                                                         "zoom_in"),
    ("024_you_must_rule_over_it.jpg",      "But you must rule over it.",                                                                      "zoom_out"),
    ("025_cain_did_not_listen.jpg",        "Cain did not listen.",                                                                            "zoom_in"),
    ("026_lets_go_to_field.jpg",           "He said to his brother Abel: let's go out to the field.",                                          "pan_right"),
    ("027_while_in_the_field.jpg",         "And while they were out in the field...",                                                          "zoom_out"),
    ("028_cain_rose_against_abel.jpg",     "Cain rose up against his brother Abel.",                                                           "zoom_in"),
    ("029_and_he_killed_him.jpg",          "And he killed him.",                                                                               "zoom_out"),
    ("030_first_death_first_murder.jpg",   "The first death. The first murder.",                                                               "zoom_in"),
    ("031_abels_blood_cried_out.jpg",      "Abel's blood cried out from the ground.",                                                          "zoom_in"),
    ("032_where_is_your_brother.jpg",      "Then the Lord said to Cain: Where is your brother Abel?",                                          "zoom_out"),
    ("033_am_i_my_brothers_keeper.jpg",    "I don't know, Cain said. Am I my brother's keeper?",                                               "zoom_in"),
    ("034_what_have_you_done.jpg",         "What have you done? the Lord said.",                                                               "zoom_in"),
    ("035_blood_cries_from_ground.jpg",    "Your brother's blood cries out to me from the ground.",                                            "pan_right"),
    ("036_cursed_from_ground.jpg",         "You are now cursed from the ground.",                                                              "zoom_out"),
    ("037_ground_yields_no_crops.jpg",     "When you work the soil, it will no longer yield its crops for you.",                               "zoom_in"),
    ("038_restless_wanderer.jpg",          "You will be a restless wanderer on the earth.",                                                    "pan_right"),
    ("039_punishment_too_great.jpg",       "Cain said to the Lord: my punishment is more than I can bear.",                                    "zoom_in"),
    ("040_driving_me_from_land.jpg",       "Today you are driving me from the land.",                                                          "pan_left"),
    ("041_hidden_from_presence.jpg",       "I will be hidden from your presence.",                                                             "zoom_out"),
    ("042_whoever_finds_me.jpg",           "I will be a restless wanderer — and whoever finds me will kill me.",                               "zoom_in"),
    ("043_vengeance_seven_times.jpg",      "But the Lord said: anyone who kills Cain will suffer vengeance seven times over.",                 "zoom_out"),
    ("044_lord_put_mark_on_cain.jpg",      "And the Lord put a mark on Cain.",                                                                 "zoom_in"),
    ("045_none_would_kill_him.jpg",        "So that no one who found him would kill him.",                                                     "zoom_out"),
    ("046_cain_left_lords_presence.jpg",   "So Cain left the Lord's presence.",                                                                "pan_left"),
    ("047_land_of_nod.jpg",               "And settled in the land of Nod, east of Eden.",                                                    "pan_right"),
    ("048_abel_was_gone.jpg",             "Abel was gone.",                                                                                   "zoom_in"),
    ("049_flock_without_shepherd.jpg",    "His flock grazed without a shepherd.",                                                             "pan_right"),
    ("050_altar_stood_silent.jpg",        "His altar stood cold and silent.",                                                                 "zoom_out"),
    ("051_adam_eve_grieved.jpg",          "Adam and Eve grieved deeply.",                                                                     "zoom_out"),
    ("052_eve_conceived_again.jpg",       "And in time, Eve conceived again.",                                                                "zoom_in"),
    ("053_gave_birth_to_son.jpg",         "She gave birth to a son.",                                                                        "zoom_in"),
    ("054_named_him_seth.jpg",            "And she named him Seth.",                                                                          "zoom_in"),
    ("055_another_child_for_abel.jpg",    "God has granted me another child in place of Abel, she said. The line of Adam continued. But something in the world would never be the same.", "zoom_out"),
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

    list_file = OUTPUT_DIR / "ch03_concat_list.txt"
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

    web_out = OUTPUT_DIR / "ch03_cain_and_abel_720p.mp4"
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
