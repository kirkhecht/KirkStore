#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 1 — Full Documentary Pipeline (Scenes 1-110)

Pipeline:
  1. ElevenLabs TTS voiceover per scene narration line
  2. Ken Burns motion video clip per image, timed to audio duration
  3. Fade-in / fade-out transitions per clip
  4. Concat all 110 audio+video clips into final documentary MP4

Output: project/documentary/ch01_cold_open_creation.mp4

Usage:
    python gen_documentary.py              # full run
    python gen_documentary.py --test 5     # first 5 scenes as a quick test
    python gen_documentary.py --start 20   # resume from scene 20
    python gen_documentary.py --skip-audio # re-render video only (keep existing audio)
"""

import os, sys, json, time, subprocess, requests, argparse
from pathlib import Path

# ── Paths ───────────────────────────────────────────────────────────────────────
COLD_OPEN_DIR = Path("project/stories/ch01_cold_open")
CREATION_DIR  = Path("project/stories/ch01_the_creation")
AUDIO_DIR     = Path("project/documentary/audio")
CLIPS_DIR     = Path("project/documentary/clips")
OUTPUT_DIR    = Path("project/documentary")
FINAL_OUT     = OUTPUT_DIR / "ch01_cold_open_creation.mp4"

for d in [AUDIO_DIR, CLIPS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

IMAGE_DIRS = {"cold_open": COLD_OPEN_DIR, "creation": CREATION_DIR}

# ── ElevenLabs config ───────────────────────────────────────────────────────────
# George: British storyteller voice — warm, captivating, perfect for documentary
VOICE_ID  = "JBFqnCBsd6RMkjVDRZzb"
EL_MODEL  = "eleven_multilingual_v2"
SILENCE_PAD = 0.45   # seconds of silence added after each narration clip

# ── Video config ────────────────────────────────────────────────────────────────
FPS    = 25
W, H   = 1920, 1080
FADE   = 0.25   # fade-in and fade-out seconds per clip

# ── Motion expressions (zoompan) ────────────────────────────────────────────────
# on = current frame number, zoom = current zoom, iw/ih = input width/height
MOTION = {
    "zoom_in": (
        "z='min(zoom+0.0007,1.3)':"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    "zoom_out": (
        "z='if(eq(on,1),1.3,max(1.001,zoom-0.0007))':"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    "pan_right": (
        "z='1.18':"
        "x='min(iw*(1-1/zoom),0+on*0.5)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    "pan_left": (
        "z='1.18':"
        "x='max(0,iw*(1-1/zoom)-on*0.5)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    "pan_up": (
        "z='1.18':"
        "x='iw/2-(iw/zoom/2)':"
        "y='max(0,ih*(1-1/zoom)-on*0.35)'"
    ),
    "pan_down": (
        "z='1.18':"
        "x='iw/2-(iw/zoom/2)':"
        "y='min(ih*(1-1/zoom),0+on*0.35)'"
    ),
    "drift_right_up": (
        "z='1.2':"
        "x='min(iw*(1-1/zoom),0+on*0.4)':"
        "y='max(0,ih*(1-1/zoom)-on*0.25)'"
    ),
    "zoom_in_up": (
        "z='min(zoom+0.0007,1.3)':"
        "x='iw/2-(iw/zoom/2)':"
        "y='max(0,ih/2-(ih/zoom/2)-on*0.15)'"
    ),
    "zoom_out_right": (
        "z='if(eq(on,1),1.3,max(1.001,zoom-0.0006))':"
        "x='min(iw*(1-1/zoom),iw/2-(iw/zoom/2)+on*0.3)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
}

# ── Scene manifest ──────────────────────────────────────────────────────────────
# (dir_key, filename, narration_text, motion_type)
SCENES = [
    # ── COLD OPEN ────────────────────────────────────────────────────────────────
    ("cold_open", "001_title_ot_documentary.jpg",    "The Old Testament. A cinematic documentary.",                                           "zoom_in"),
    ("cold_open", "002_part_1.jpg",                   "Part 1.",                                                                               "zoom_out"),
    ("cold_open", "003_book_of_genesis.jpg",          "The Book of Genesis. Creation to Babel.",                                               "pan_right"),
    ("cold_open", "004_cold_open_title.jpg",          "Cold Open.",                                                                            "zoom_in"),
    ("cold_open", "005_before_kingdoms.jpg",          "Before kingdoms,",                                                                      "pan_right"),
    ("cold_open", "006_before_nations.jpg",           "before nations, before the first whisper of human breath,",                             "zoom_out"),
    ("cold_open", "007_before_egypt.jpg",             "before the rise of Egypt,",                                                             "pan_right"),
    ("cold_open", "008_before_mesopotamia.jpg",       "before the cities of Mesopotamia,",                                                     "pan_left"),
    ("cold_open", "009_before_stars_had_names.jpg",   "before the stars had names,",                                                           "zoom_out"),
    ("cold_open", "010_the_deep.jpg",                 "there was only the deep,",                                                              "zoom_in"),
    ("cold_open", "011_vast_silent.jpg",              "vast, silent,",                                                                         "zoom_out"),
    ("cold_open", "012_formless_silence.jpg",         "formless, and into that silence,",                                                      "zoom_in"),
    ("cold_open", "013_came_a_voice.jpg",             "came a voice. This is the story of how everything began,",                              "zoom_in"),
    ("cold_open", "014_first_light_first_betrayal.jpg","of the first light, the first betrayal,",                                              "pan_right"),
    ("cold_open", "015_first_murder_first_flood.jpg", "the first murder, the first flood,",                                                    "pan_down"),
    ("cold_open", "016_world_born_perfect.jpg",       "of a world that was born perfect and broken almost as quickly, of a family",            "zoom_out"),
    ("cold_open", "017_fall_and_rise.jpg",            "that would fall and rise and fall again,",                                              "pan_up"),
    ("cold_open", "018_creator_who.jpg",              "and of a creator who,",                                                                 "zoom_in_up"),
    ("cold_open", "019_world_turned_against.jpg",     "even when his world turned against him,",                                               "pan_right"),
    ("cold_open", "020_refused_to_walk_away.jpg",     "refused to walk away. This is the Book of Genesis,",                                   "zoom_out"),
    ("cold_open", "021_this_is_where_it_begins.jpg",  "and this is where it all begins.",                                                      "zoom_in"),
    ("cold_open", "022_book_of_genesis_header.jpg",   "Book of Genesis.",                                                                      "zoom_in"),
    ("cold_open", "023_genesis_1.jpg",                "Genesis 1.",                                                                            "zoom_out"),
    ("cold_open", "024_creation_of_the_world.jpg",    "The Creation of the World.",                                                            "zoom_in"),
    ("cold_open", "025_before_recorded_history.jpg",  "Approximately before recorded history.",                                                "zoom_out"),
    ("cold_open", "026_in_the_beginning_nothing.jpg", "In the beginning, there was nothing.",                                                  "zoom_in"),
    ("cold_open", "027_no_earth_no_sun.jpg",          "No earth, no sun,",                                                                     "zoom_out"),
    ("cold_open", "028_no_sky_no_time.jpg",           "no sky, no measure of time, because time itself had not yet begun.",                    "zoom_in"),
    ("cold_open", "029_only_god_and_then.jpg",        "Only God. And then,",                                                                   "zoom_in"),
    ("cold_open", "030_a_word_first_sound.jpg",       "a word. The first sound the universe had ever known,",                                  "zoom_out"),
    ("cold_open", "031_voice_over_darkness.jpg",      "a voice moving over the darkness,",                                                     "zoom_in"),
    ("cold_open", "032_breath_stirring_deep.jpg",     "a breath stirring across the deep,",                                                    "pan_right"),
    ("cold_open", "033_first_command.jpg",            "and from that voice came the first command,",                                           "zoom_in"),
    ("cold_open", "034_let_there_be_light.jpg",       "let there be light,",                                                                   "zoom_in"),
    ("cold_open", "035_darkness_obeyed.jpg",          "and the darkness obeyed.",                                                              "pan_right"),
    ("cold_open", "036_light_tore_through.jpg",       "Light tore through the emptiness,",                                                     "zoom_out"),
    ("cold_open", "037_not_from_a_star.jpg",          "not from a star, not from a sun,",                                                      "zoom_in"),
    ("cold_open", "038_from_the_will.jpg",            "because neither yet existed, but from the will of the one who spoke.",                  "zoom_in"),
    ("cold_open", "039_light_spread.jpg",             "And as the light spread,",                                                              "zoom_out_right"),
    ("cold_open", "040_universe_took_shape.jpg",      "the universe began to take shape.",                                                     "zoom_out"),
    ("cold_open", "041_second_day.jpg",               "On the second day,",                                                                    "pan_up"),
    ("cold_open", "042_heavens_opened.jpg",           "the heavens opened. The sky stretched out like a vast canopy above the waters.",        "zoom_out"),
    ("cold_open", "043_dry_land_rose.jpg",            "On the third, dry land rose from the seas.",                                            "pan_up"),
    ("cold_open", "044_mountains_pushed_upward.jpg",  "Mountains pushed upward.",                                                              "pan_up"),
    ("cold_open", "045_valleys_carved.jpg",           "Valleys carved themselves into the earth.",                                             "pan_down"),
    ("cold_open", "046_forests_bloomed.jpg",          "Forests bloomed where there had only been silence.",                                    "pan_right"),
    ("cold_open", "047_fourth_day_sun.jpg",           "On the fourth day, the sun was set to blaze in the heavens.",                          "zoom_in"),
    ("cold_open", "048_moon_took_her_place.jpg",      "The moon took her place in the night,",                                                 "pan_up"),
    ("cold_open", "049_stars_glittering_eternal.jpg", "and the stars, countless, glittering, eternal,",                                       "zoom_out"),
    ("cold_open", "050_scattered_across_dark.jpg",    "were scattered across the dark,",                                                       "drift_right_up"),
    ("cold_open", "051_pages_of_story.jpg",           "like the pages of a story not yet written.",                                            "zoom_in"),
    ("cold_open", "052_fifth_day.jpg",                "On the fifth day,",                                                                     "zoom_in"),
    ("cold_open", "053_life_began_to_move.jpg",       "life began to move.",                                                                   "zoom_in"),
    ("cold_open", "054_oceans_creatures_stirred.jpg", "In the oceans, creatures stirred,",                                                     "pan_right"),
    ("cold_open", "055_fish_leviathans.jpg",          "schools of fish, Leviathans of the deep,",                                              "zoom_out"),

    # ── THE CREATION ─────────────────────────────────────────────────────────────
    ("creation",  "056_things_never_seen.jpg",        "things that had never been seen before, because they had never existed before.",        "zoom_out"),
    ("creation",  "057_wings_unfurled.jpg",           "In the skies, wings unfurled.",                                                         "pan_up"),
    ("creation",  "058_birds_rose.jpg",               "Birds rose into the air,",                                                              "pan_up"),
    ("creation",  "059_calling_across_new_world.jpg", "calling to one another across the new world.",                                          "zoom_out"),
    ("creation",  "060_sixth_day_land_alive.jpg",     "And on the sixth day, the land itself came alive.",                                     "zoom_out"),
    ("creation",  "061_cattle_on_hills.jpg",          "Cattle on the hills,",                                                                  "pan_right"),
    ("creation",  "062_wild_beasts_forests.jpg",      "wild beasts in the forests,",                                                           "zoom_in"),
    ("creation",  "063_creeping_things.jpg",          "creeping things in the grass.",                                                         "zoom_in"),
    ("creation",  "064_shaped_with_intention.jpg",    "Every creature shaped with intention,",                                                 "zoom_in"),
    ("creation",  "065_every_detail.jpg",             "every detail considered,",                                                              "zoom_in"),
    ("creation",  "066_reflection_of_maker.jpg",      "every form a reflection of the one who made them.",                                    "zoom_out"),
    ("creation",  "067_at_the_very_end.jpg",          "And then, at the very end,",                                                            "pan_right"),
    ("creation",  "068_god_paused.jpg",               "God paused. Because he was about to do something different.",                           "zoom_in"),
    ("creation",  "069_reached_into_dust.jpg",        "He reached down into the dust of the earth he had just made.",                          "zoom_in"),
    ("creation",  "070_gathered_in_hands.jpg",        "He gathered it in his hands.",                                                          "zoom_in"),
    ("creation",  "071_shaped_not_animal.jpg",        "And he shaped it, not into another animal,",                                            "zoom_in"),
    ("creation",  "072_carry_his_own_image.jpg",      "not into another beast, but into something that would carry his own image.",            "zoom_out"),
    ("creation",  "073_breathed_into_it.jpg",         "He breathed into it,",                                                                  "zoom_in_up"),
    ("creation",  "074_dust_became_man.jpg",          "and dust became man.",                                                                  "zoom_in"),
    ("creation",  "075_first_time_universe.jpg",      "For the first time in the history of the universe,",                                   "zoom_out"),
    ("creation",  "076_stood_upright_face_of_maker.jpg","a creature stood upright and looked into the face of his maker.",                    "zoom_in_up"),
    ("creation",  "077_his_name_was_adam.jpg",        "His name was Adam,",                                                                    "zoom_in"),
    ("creation",  "078_seventh_day.jpg",              "and on the seventh day,",                                                               "zoom_out"),
    ("creation",  "079_creator_rested.jpg",           "the creator rested. Not because he was tired, but because the work was",               "pan_right"),
    ("creation",  "080_finished_perfect.jpg",         "finished. The world was perfect.",                                                      "zoom_out"),
    ("creation",  "081_would_not_stay.jpg",           "It would not stay that way for long.",                                                  "zoom_in"),
    ("creation",  "082_genesis_2_3.jpg",              "Genesis 2 and 3.",                                                                      "zoom_in"),
    ("creation",  "083_adam.jpg",                     "Adam,",                                                                                 "pan_right"),
    ("creation",  "084_eve_fall_of_man.jpg",          "Eve, and the fall of man.",                                                             "zoom_in"),
    ("creation",  "085_dawn_of_humanity.jpg",         "The dawn of humanity,",                                                                 "zoom_out"),
    ("creation",  "086_god_planted_a_garden.jpg",     "in the east, God planted a garden,",                                                   "zoom_out"),
    ("creation",  "087_place_called_eden.jpg",        "a place called Eden, a paradise unlike anything the earth would ever see again.",       "pan_right"),
    ("creation",  "088_rivers_flowed.jpg",            "Rivers flowed through it,",                                                             "pan_right"),
    ("creation",  "089_trees_heavy_fruit.jpg",        "trees heavy with fruit lined its paths,",                                               "pan_right"),
    ("creation",  "090_animals_no_fear.jpg",          "animals roamed without fear.",                                                          "pan_right"),
    ("creation",  "091_no_death.jpg",                 "There was no death here,",                                                              "zoom_out"),
    ("creation",  "092_no_sickness_no_sorrow.jpg",    "no sickness, no sorrow,",                                                               "zoom_in"),
    ("creation",  "093_no_hunger_no_shame.jpg",       "no hunger, no shame,",                                                                  "zoom_in"),
    ("creation",  "094_two_trees.jpg",                "and in the center of the garden stood two trees,",                                      "zoom_out"),
    ("creation",  "095_tree_of_life.jpg",             "the tree of life,",                                                                     "zoom_in"),
    ("creation",  "096_tree_of_knowledge.jpg",        "and the tree of the knowledge of good and evil.",                                       "zoom_in"),
    ("creation",  "097_adam_receiving_rule.jpg",      "God placed Adam in the garden and gave him only one rule.",                             "zoom_in"),
    ("creation",  "098_all_trees_permitted.jpg",      "He could eat from any tree.",                                                           "zoom_out"),
    ("creation",  "099_adam_picking_fruit.jpg",       "Any tree at all,",                                                                      "zoom_in"),
    ("creation",  "100_forbidden_fruit.jpg",          "except one. Do not eat from the tree of the knowledge of good and evil.",               "zoom_in"),
    ("creation",  "101_adam_warning.jpg",             "For in the day you eat of it,",                                                         "zoom_in"),
    ("creation",  "102_single_command.jpg",           "you will surely die. It was a single command,",                                        "zoom_out"),
    ("creation",  "103_one_boundary.jpg",             "a single boundary, in a world overflowing with abundance.",                            "zoom_out"),
    ("creation",  "104_adam_alone_eden.jpg",          "But Adam was alone,",                                                                   "zoom_out"),
    ("creation",  "105_adam_alone_sunset.jpg",        "and God said it was not good for man to be alone.",                                     "zoom_out"),
    ("creation",  "106_adam_deep_sleep.jpg",          "So as Adam slept, God formed a companion for him,",                                    "zoom_in"),
    ("creation",  "107_rib_drawn_out.jpg",            "bone of his bone,",                                                                     "zoom_in"),
    ("creation",  "108_eve_forming.jpg",              "flesh of his flesh.",                                                                   "zoom_out"),
    ("creation",  "109_eve_portrait.jpg",             "Her name was Eve.",                                                                     "zoom_in"),
    ("creation",  "110_adam_eve_together.jpg",        "And for a time, for how long we do not know,",                                         "pan_right"),
]


# ── Helpers ─────────────────────────────────────────────────────────────────────

def load_env():
    env = {}
    p = Path(".env")
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def get_audio_duration(path):
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


def make_scene_clip(img_path, audio_path, out_path, motion, video_dur):
    """Create a single scene clip: motion video + narration audio, with fade in/out."""
    frames = max(FPS, int(video_dur * FPS))
    zp = MOTION[motion]

    fade_frames_in  = int(FADE * FPS)
    fade_frames_out = max(1, frames - int(FADE * FPS))

    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
        f"zoompan={zp}:d={frames}:s={W}x{H}:fps={FPS},"
        f"fade=t=in:st=0:d={FADE},"
        f"fade=t=out:st={video_dur - FADE:.3f}:d={FADE},"
        f"format=yuv420p"
    )

    # Audio: narration padded with silence to match video_dur
    af = f"apad=pad_dur={video_dur:.3f},atrim=0:{video_dur:.3f},afade=t=in:st=0:d=0.1,afade=t=out:st={video_dur - 0.15:.3f}:d=0.1"

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-i", str(audio_path),
        "-vf", vf,
        "-af", af,
        "-t", str(video_dur),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(out_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg error for {out_path.name}:\n{r.stderr[-400:]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",       type=int, default=0,   help="Only render first N scenes")
    parser.add_argument("--start",      type=int, default=1,   help="Start at scene N (1-indexed)")
    parser.add_argument("--end",        type=int, default=110, help="End at scene N")
    parser.add_argument("--skip-audio", action="store_true",   help="Skip TTS generation, reuse existing audio")
    parser.add_argument("--skip-clips", action="store_true",   help="Skip clip render, go straight to assembly")
    args = parser.parse_args()

    env = load_env()
    el_key = env.get("ELEVENLABS_API_KEY", "")
    if not el_key and not args.skip_audio:
        sys.exit("ELEVENLABS_API_KEY not in .env")

    scenes = SCENES
    if args.test:
        scenes = SCENES[:args.test]
    else:
        scenes = SCENES[args.start - 1 : args.end]

    # ── Phase 1: ElevenLabs TTS ────────────────────────────────────────────────
    if not args.skip_audio:
        print(f"\n{'='*60}")
        print(f"  Phase 1: Generating voiceover ({len(scenes)} lines)")
        print(f"{'='*60}")
        for i, (dir_key, filename, narration, motion) in enumerate(scenes):
            scene_num = args.start + i if not args.test else i + 1
            audio_out = AUDIO_DIR / f"{scene_num:03d}.mp3"
            if audio_out.exists():
                print(f"  [{scene_num:03d}] Audio OK (exists)")
                continue
            print(f"  [{scene_num:03d}] TTS → \"{narration[:55]}{'…' if len(narration)>55 else ''}\"")
            generate_tts(narration, audio_out, el_key)
            time.sleep(0.4)

    # ── Phase 2: Render motion clips ───────────────────────────────────────────
    if not args.skip_clips:
        print(f"\n{'='*60}")
        print(f"  Phase 2: Rendering motion clips ({len(scenes)} clips)")
        print(f"{'='*60}")
        for i, (dir_key, filename, narration, motion) in enumerate(scenes):
            scene_num = args.start + i if not args.test else i + 1
            img_path   = IMAGE_DIRS[dir_key] / filename
            audio_path = AUDIO_DIR / f"{scene_num:03d}.mp3"
            clip_out   = CLIPS_DIR / f"{scene_num:03d}.mp4"

            if clip_out.exists():
                print(f"  [{scene_num:03d}] Clip OK (exists)")
                continue

            if not img_path.exists():
                print(f"  [{scene_num:03d}] WARNING: missing image {img_path.name}, skipping")
                continue
            if not audio_path.exists():
                print(f"  [{scene_num:03d}] WARNING: missing audio, skipping")
                continue

            audio_dur  = get_audio_duration(audio_path)
            video_dur  = audio_dur + SILENCE_PAD
            print(f"  [{scene_num:03d}] {motion:16s} {video_dur:.1f}s  {filename}")
            make_scene_clip(img_path, audio_path, clip_out, motion, video_dur)

    # ── Phase 3: Assemble final documentary ───────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Phase 3: Assembling documentary")
    print(f"{'='*60}")

    concat_file = OUTPUT_DIR / "concat.txt"
    clip_list = []
    for i, (dir_key, filename, narration, motion) in enumerate(scenes):
        scene_num = args.start + i if not args.test else i + 1
        clip = CLIPS_DIR / f"{scene_num:03d}.mp4"
        if clip.exists():
            clip_list.append(clip)

    if not clip_list:
        sys.exit("No clips found to assemble.")

    with open(concat_file, "w") as f:
        for c in clip_list:
            f.write(f"file '{c.resolve()}'\n")

    output_file = FINAL_OUT if not args.test else OUTPUT_DIR / f"test_{args.test}_scenes.mp4"

    print(f"  Concatenating {len(clip_list)} clips → {output_file.name}")
    r = subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_file),
    ], capture_output=True, text=True)

    if r.returncode != 0:
        print(f"  Assembly error: {r.stderr[-400:]}")
        sys.exit(1)

    size_mb = output_file.stat().st_size / 1_048_576
    print(f"\n  ✓ Done: {output_file}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
