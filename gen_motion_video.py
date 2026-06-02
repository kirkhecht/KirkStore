"""
Motion Picture Assembler — Ken Burns effect + crossfade dissolve transitions.

Turns the story still images into a cinematic video by applying:
  - Slow pan / zoom / drift per scene (chosen to match the visual content)
  - 0.8s crossfade dissolve between every scene
  - 25fps, 1920x1080, H.264

Usage:
    python gen_motion_video.py                          # preview: Cold Open + Creation
    python gen_motion_video.py --section cold_open      # Cold Open only
    python gen_motion_video.py --section creation       # The Creation only
    python gen_motion_video.py --fps 25 --crf 18        # higher quality final render
    python gen_motion_video.py --preview                # fast draft (crf 28, ultrafast)
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path

# ── Directories ────────────────────────────────────────────────────────────────
COLD_OPEN_DIR = Path("project/stories/ch01_cold_open")
CREATION_DIR  = Path("project/stories/ch01_the_creation")
OUTPUT_DIR    = Path("project/stories/video")
CLIPS_DIR     = Path("project/stories/clips")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CLIPS_DIR.mkdir(parents=True, exist_ok=True)

FPS = 25
CROSSFADE = 0.8      # seconds of dissolve between scenes
DEFAULT_DUR = 5.0    # seconds per image (for preview — real runs use audio timing)

# ── Motion types ───────────────────────────────────────────────────────────────
# Each type is a zoompan expression.  z=zoom, x/y=position, on=frame number.
# All motions start from z=1.0 or z=1.25 and drift slowly over the clip duration.
# The 'd' (duration in frames) is inserted at render time based on actual clip length.

MOTION_EXPRS = {
    # Slow zoom IN toward center — building tension, intimacy, focus
    "zoom_in": (
        "z='min(zoom+0.0007,1.3)':"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    # Slow zoom OUT from center — revelation, scale, the universe expanding
    "zoom_out": (
        "z='if(eq(on,1),1.3,max(1.001,zoom-0.0007))':"
        "x='iw/2-(iw/zoom/2)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    # Pan slowly LEFT to RIGHT — narrative progression, reading, time passing
    "pan_right": (
        "z='1.18':"
        "x='min(iw*(1-1/zoom),0+on*0.5)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    # Pan slowly RIGHT to LEFT — reversal, looking back, mourning
    "pan_left": (
        "z='1.18':"
        "x='max(0,iw*(1-1/zoom)-on*0.5)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
    # Pan slowly UPWARD — ascension, hope, heaven, mountains rising
    "pan_up": (
        "z='1.18':"
        "x='iw/2-(iw/zoom/2)':"
        "y='max(0,ih*(1-1/zoom)-on*0.35)'"
    ),
    # Pan slowly DOWNWARD — descent, fall, weight, gravity
    "pan_down": (
        "z='1.18':"
        "x='iw/2-(iw/zoom/2)':"
        "y='min(ih*(1-1/zoom),0+on*0.35)'"
    ),
    # Drift diagonally — wandering, searching, lost
    "drift_right_up": (
        "z='1.2':"
        "x='min(iw*(1-1/zoom),0+on*0.4)':"
        "y='max(0,ih*(1-1/zoom)-on*0.25)'"
    ),
    "drift_right_down": (
        "z='1.2':"
        "x='min(iw*(1-1/zoom),0+on*0.4)':"
        "y='min(ih*(1-1/zoom),0+on*0.25)'"
    ),
    # Zoom in + slight upward — soaring, divine presence descending
    "zoom_in_up": (
        "z='min(zoom+0.0007,1.3)':"
        "x='iw/2-(iw/zoom/2)':"
        "y='max(0,ih/2-(ih/zoom/2)-on*0.15)'"
    ),
    # Zoom out + slight pan right — wide reveal sweeping across landscape
    "zoom_out_right": (
        "z='if(eq(on,1),1.3,max(1.001,zoom-0.0006))':"
        "x='min(iw*(1-1/zoom),iw/2-(iw/zoom/2)+on*0.3)':"
        "y='ih/2-(ih/zoom/2)'"
    ),
}

# ── Scene manifest — (filename, dir_key, motion_type, subtitle) ────────────────
# Motion choice is based on the visual content and emotional intent of each line.

SCENES = [
    # COLD OPEN
    ("001_title_ot_documentary.jpg", "cold_open", "zoom_in",       "The Old Testament. A cinematic documentary."),
    ("002_part_1.jpg",               "cold_open", "zoom_out",      "Part 1."),
    ("003_book_of_genesis.jpg",      "cold_open", "pan_right",     "The Book of Genesis. Creation to Babel."),
    ("004_cold_open_title.jpg",      "cold_open", "zoom_in",       "Cold Open."),
    ("005_before_kingdoms.jpg",      "cold_open", "pan_right",     "Before kingdoms,"),
    ("006_before_nations.jpg",       "cold_open", "zoom_out",      "before nations, before the first whisper of human breath,"),
    ("007_before_egypt.jpg",         "cold_open", "pan_right",     "before the rise of Egypt,"),
    ("008_before_mesopotamia.jpg",   "cold_open", "pan_left",      "before the cities of Mesopotamia,"),
    ("009_before_stars_had_names.jpg","cold_open","zoom_out",      "before the stars had names,"),
    ("010_the_deep.jpg",             "cold_open", "zoom_in",       "there was only the deep,"),
    ("011_vast_silent.jpg",          "cold_open", "zoom_out",      "vast, silent,"),
    ("012_formless_silence.jpg",     "cold_open", "zoom_in",       "formless, and into that silence,"),
    ("013_came_a_voice.jpg",         "cold_open", "zoom_in",       "came a voice. This is the story of how everything began,"),
    ("014_first_light_first_betrayal.jpg","cold_open","pan_right", "of the first light, the first betrayal,"),
    ("015_first_murder_first_flood.jpg","cold_open","pan_down",    "the first murder, the first flood,"),
    ("016_world_born_perfect.jpg",   "cold_open", "zoom_out",      "of a world that was born perfect and broken almost as quickly,"),
    ("017_fall_and_rise.jpg",        "cold_open", "pan_up",        "of a family that would fall and rise and fall again,"),
    ("018_creator_who.jpg",          "cold_open", "zoom_in_up",    "and of a creator who,"),
    ("019_world_turned_against.jpg", "cold_open", "pan_right",     "even when his world turned against him,"),
    ("020_refused_to_walk_away.jpg", "cold_open", "zoom_out",      "refused to walk away. This is the Book of Genesis,"),
    ("021_this_is_where_it_begins.jpg","cold_open","zoom_in",      "and this is where it all begins."),
    ("022_book_of_genesis_header.jpg","cold_open","zoom_in",       "Book of Genesis."),
    ("023_genesis_1.jpg",            "cold_open", "zoom_out",      "Genesis 1."),
    ("024_creation_of_the_world.jpg","cold_open", "zoom_in",       "The Creation of the World."),
    ("025_before_recorded_history.jpg","cold_open","zoom_out",     "Approximately before recorded history."),
    ("026_in_the_beginning_nothing.jpg","cold_open","zoom_in",     "In the beginning, there was nothing."),
    ("027_no_earth_no_sun.jpg",      "cold_open", "zoom_out",      "No earth, no sun,"),
    ("028_no_sky_no_time.jpg",       "cold_open", "zoom_in",       "no sky, no measure of time, because time itself had not yet begun."),
    ("029_only_god_and_then.jpg",    "cold_open", "zoom_in",       "Only God. And then,"),
    ("030_a_word_first_sound.jpg",   "cold_open", "zoom_out",      "a word. The first sound the universe had ever known,"),
    ("031_voice_over_darkness.jpg",  "cold_open", "zoom_in",       "a voice moving over the darkness,"),
    ("032_breath_stirring_deep.jpg", "cold_open", "pan_right",     "a breath stirring across the deep,"),
    ("033_first_command.jpg",        "cold_open", "zoom_in",       "and from that voice came the first command,"),
    ("034_let_there_be_light.jpg",   "cold_open", "zoom_in",       "let there be light,"),
    ("035_darkness_obeyed.jpg",      "cold_open", "pan_right",     "and the darkness obeyed."),
    ("036_light_tore_through.jpg",   "cold_open", "zoom_out",      "Light tore through the emptiness,"),
    ("037_not_from_a_star.jpg",      "cold_open", "zoom_in",       "not from a star, not from a sun,"),
    ("038_from_the_will.jpg",        "cold_open", "zoom_in",       "because neither yet existed, but from the will of the one who spoke."),
    ("039_light_spread.jpg",         "cold_open", "zoom_out_right","And as the light spread,"),
    ("040_universe_took_shape.jpg",  "cold_open", "zoom_out",      "the universe began to take shape."),
    ("041_second_day.jpg",           "cold_open", "pan_up",        "On the second day,"),
    ("042_heavens_opened.jpg",       "cold_open", "zoom_out",      "the heavens opened. The sky stretched out like a vast canopy above the waters."),
    ("043_dry_land_rose.jpg",        "cold_open", "pan_up",        "On the third, dry land rose from the seas."),
    ("044_mountains_pushed_upward.jpg","cold_open","pan_up",       "Mountains pushed upward."),
    ("045_valleys_carved.jpg",       "cold_open", "pan_down",      "Valleys carved themselves into the earth."),
    ("046_forests_bloomed.jpg",      "cold_open", "pan_right",     "Forests bloomed where there had only been silence."),
    ("047_fourth_day_sun.jpg",       "cold_open", "zoom_in",       "On the fourth day, the sun was set to blaze in the heavens."),
    ("048_moon_took_her_place.jpg",  "cold_open", "pan_up",        "The moon took her place in the night,"),
    ("049_stars_glittering_eternal.jpg","cold_open","zoom_out",    "and the stars, countless glittering, eternal,"),
    ("050_scattered_across_dark.jpg","cold_open", "drift_right_up","were scattered across the dark,"),
    ("051_pages_of_story.jpg",       "cold_open", "zoom_in",       "like the pages of a story not yet written."),
    ("052_fifth_day.jpg",            "cold_open", "zoom_in",       "On the fifth day,"),
    ("053_life_began_to_move.jpg",   "cold_open", "zoom_in",       "life began to move."),
    ("054_oceans_creatures_stirred.jpg","cold_open","pan_right",   "In the oceans, creatures stirred,"),
    ("055_fish_leviathans.jpg",      "cold_open", "zoom_out",      "schools of fish, Leviathans of the deep,"),

    # THE CREATION
    ("056_things_never_seen.jpg",    "creation",  "zoom_out",      "things that had never been seen before, because they had never existed before."),
    ("057_wings_unfurled.jpg",       "creation",  "pan_up",        "In the skies, wings unfurled."),
    ("058_birds_rose.jpg",           "creation",  "pan_up",        "Birds rose into the air,"),
    ("059_calling_across_new_world.jpg","creation","zoom_out",     "calling to one another across the new world."),
    ("060_sixth_day_land_alive.jpg", "creation",  "zoom_out",      "And on the sixth day, the land itself came alive."),
    ("061_cattle_on_hills.jpg",      "creation",  "pan_right",     "Cattle on the hills,"),
    ("062_wild_beasts_forests.jpg",  "creation",  "zoom_in",       "wild beasts in the forests,"),
    ("063_creeping_things.jpg",      "creation",  "zoom_in",       "creeping things in the grass."),
    ("064_shaped_with_intention.jpg","creation",  "zoom_in",       "Every creature shaped with intention,"),
    ("065_every_detail.jpg",         "creation",  "zoom_in",       "every detail considered,"),

    # Remaining scenes (66–110) — will generate once quota resets
    ("066_reflection_of_maker.jpg",  "creation",  "zoom_out",      "every form or reflection of the one who made them."),
    ("067_at_the_very_end.jpg",      "creation",  "pan_right",     "And then, at the very end,"),
    ("068_god_paused.jpg",           "creation",  "zoom_in",       "God paused. Because he was about to do something different."),
    ("069_reached_into_dust.jpg",    "creation",  "zoom_in",       "He reached down into the dust of the earth he had just made."),
    ("070_gathered_in_hands.jpg",    "creation",  "zoom_in",       "He gathered it in his hands."),
    ("071_shaped_not_animal.jpg",    "creation",  "zoom_in",       "And he shaped it, not into another animal,"),
    ("072_carry_his_own_image.jpg",  "creation",  "zoom_out",      "not into another beast, but into something that would carry his own image."),
    ("073_breathed_into_it.jpg",     "creation",  "zoom_in_up",    "He breathed into it,"),
    ("074_dust_became_man.jpg",      "creation",  "zoom_in",       "and dust became man."),
    ("075_first_time_universe.jpg",  "creation",  "zoom_out",      "For the first time in the history of the universe,"),
    ("076_stood_upright_face_of_maker.jpg","creation","zoom_in_up","a creature stood upright and looked into the face of his maker."),
    ("077_his_name_was_adam.jpg",    "creation",  "zoom_in",       "His name was Adam,"),
    ("078_seventh_day.jpg",          "creation",  "zoom_out",      "and on the seventh day,"),
    ("079_creator_rested.jpg",       "creation",  "pan_right",     "the creator rested. Not because he was tired, but because the work was"),
    ("080_finished_perfect.jpg",     "creation",  "zoom_out",      "finished, the world was perfect."),
    ("081_would_not_stay.jpg",       "creation",  "zoom_in",       "It would not stay that way for long."),
    ("082_genesis_2_3.jpg",          "creation",  "zoom_in",       "Genesis 2-3."),
    ("083_adam.jpg",                 "creation",  "pan_right",     "Adam,"),
    ("084_eve_fall_of_man.jpg",      "creation",  "zoom_in",       "Eve, and the fall of man."),
    ("085_dawn_of_humanity.jpg",     "creation",  "zoom_out",      "The dawn of humanity,"),
    ("086_god_planted_a_garden.jpg", "creation",  "zoom_out",      "in the east, God planted a garden,"),
    ("087_place_called_eden.jpg",    "creation",  "zoom_out",      "a place called Eden, a paradise unlike anything the earth would ever see again."),
    ("088_rivers_flowed.jpg",        "creation",  "pan_right",     "Rivers flowed through it,"),
    ("089_trees_heavy_fruit.jpg",    "creation",  "pan_right",     "trees heavy with fruit lined its paths,"),
    ("090_animals_no_fear.jpg",      "creation",  "pan_right",     "animals roamed without fear."),
    ("091_no_death.jpg",             "creation",  "zoom_out",      "There was no death here,"),
    ("092_no_sickness_sorrow.jpg",   "creation",  "zoom_in",       "no sickness, no sorrow,"),
    ("093_no_hunger_no_shame.jpg",   "creation",  "zoom_in",       "no hunger, no shame,"),
    ("094_center_two_trees.jpg",     "creation",  "zoom_in",       "and in the center of the garden stood two trees,"),
    ("095_tree_of_life.jpg",         "creation",  "zoom_in",       "the tree of life,"),
    ("096_tree_of_knowledge.jpg",    "creation",  "zoom_in",       "and the tree of the knowledge of good and evil."),
    ("097_placed_adam_one_rule.jpg", "creation",  "zoom_in",       "God placed Adam in the garden and gave him only one rule."),
    ("098_eat_from_any_tree.jpg",    "creation",  "zoom_out",      "He could eat from any tree."),
    ("099_any_tree_at_all.jpg",      "creation",  "zoom_in",       "Any tree at all,"),
    ("100_except_one.jpg",           "creation",  "zoom_in",       "except one. Do not eat from the tree of the knowledge of good and evil."),
    ("101_in_the_day_you_eat.jpg",   "creation",  "zoom_in",       "For in the day you eat of it,"),
    ("102_surely_die.jpg",           "creation",  "zoom_out",      "you will surely die. It was a single command,"),
    ("103_single_boundary.jpg",      "creation",  "zoom_out",      "a single boundary, in a world overflowing with abundance."),
    ("104_adam_was_alone.jpg",       "creation",  "zoom_in",       "But Adam was alone,"),
    ("105_not_good_to_be_alone.jpg", "creation",  "zoom_out",      "and God said it was not good for man to be alone."),
    ("106_adam_slept.jpg",           "creation",  "zoom_in",       "So as Adam slept, God formed a companion for him,"),
    ("107_bone_of_his_bone.jpg",     "creation",  "zoom_in",       "bone of his bone,"),
    ("108_flesh_of_his_flesh.jpg",   "creation",  "zoom_in",       "flesh of his flesh."),
    ("109_her_name_was_eve.jpg",     "creation",  "zoom_in",       "Her name was Eve."),
    ("110_for_a_time.jpg",           "creation",  "pan_right",     "And for a time, for how long we do not know,"),
]

DIRS = {"cold_open": COLD_OPEN_DIR, "creation": CREATION_DIR}


# ── FFmpeg helpers ─────────────────────────────────────────────────────────────

def make_ken_burns_clip(img_path: Path, out_path: Path, motion: str,
                        duration: float, fps: int = FPS, crf: int = 18,
                        preset: str = "fast") -> bool:
    """Render a single Ken Burns clip from a still image."""
    frames = int(duration * fps)
    zp_expr = MOTION_EXPRS[motion]

    # Scale image to 1920x1080 preserving aspect, pad black if needed, then zoompan
    vf = (
        f"scale=1920:1080:force_original_aspect_ratio=decrease,"
        f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,"
        f"zoompan={zp_expr}:d={frames}:s=1920x1080:fps={fps},"
        f"format=yuv420p"
    )

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-vf", vf,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", preset,
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        str(out_path)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[-200:]}")
        return False
    return True


def concat_with_xfade(clips: list, durations: list, output: Path,
                      crossfade: float = CROSSFADE, fps: int = FPS) -> bool:
    """Concatenate clips with crossfade dissolve transitions."""
    n = len(clips)
    if n == 1:
        import shutil
        shutil.copy(clips[0], output)
        return True

    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]

    # Build xfade filter chain
    # Each clip offset = sum of previous clip durations minus accumulated crossfade time
    filter_parts = []
    cumulative_offset = 0.0
    prev_label = "[0:v]"

    for i in range(n - 1):
        cumulative_offset += durations[i] - crossfade
        next_label = f"[xf{i}]" if i < n - 2 else ""
        src_label = f"[{i+1}:v]"
        filter_parts.append(
            f"{prev_label}{src_label}xfade=transition=dissolve:"
            f"duration={crossfade}:offset={cumulative_offset:.3f}{next_label}"
        )
        prev_label = f"[xf{i}]"

    filter_str = ";".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_str,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        str(output)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  XFADE ERROR: {result.stderr[-300:]}")
        return False
    return True


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", choices=["cold_open", "creation", "all"], default="all")
    parser.add_argument("--duration", type=float, default=DEFAULT_DUR,
                        help="Seconds per image (default 5.0)")
    parser.add_argument("--crossfade", type=float, default=CROSSFADE)
    parser.add_argument("--fps", type=int, default=FPS)
    parser.add_argument("--crf", type=int, default=20)
    parser.add_argument("--preview", action="store_true",
                        help="Fast draft: crf 26, ultrafast preset")
    parser.add_argument("--skip-clips", action="store_true",
                        help="Skip clip generation, go straight to assembly")
    args = parser.parse_args()

    preset = "ultrafast" if args.preview else "fast"
    crf    = 26 if args.preview else args.crf
    dur    = args.duration
    xfade  = args.crossfade

    # Filter to available images only
    available = []
    for filename, dir_key, motion, subtitle in SCENES:
        img = DIRS[dir_key] / filename
        if not img.exists():
            continue
        if args.section != "all" and dir_key != args.section:
            continue
        available.append((filename, dir_key, motion, subtitle, img))

    if not available:
        print("No images found. Run gen_cold_open_creation.py first.")
        sys.exit(1)

    total = len(available)
    print(f"\nMotion Picture Assembler")
    print(f"  {total} scenes | {dur}s each | {xfade}s crossfade | {args.fps}fps | CRF {crf}")
    print(f"  Total runtime: ~{total * dur / 60:.1f} min\n")

    # ── Step 1: Ken Burns clips ────────────────────────────────────────────────
    clip_paths = []
    durations  = []

    for i, (filename, dir_key, motion, subtitle, img) in enumerate(available, 1):
        clip_name = filename.replace(".jpg", ".mp4")
        clip_path = CLIPS_DIR / clip_name

        if args.skip_clips and clip_path.exists():
            size_mb = clip_path.stat().st_size / 1_048_576
            print(f"  [{i:03d}/{total}] {filename} — clip cached ({size_mb:.1f}MB)")
        else:
            print(f"  [{i:03d}/{total}] {filename}")
            print(f"    \"{subtitle}\"")
            print(f"    motion: {motion} | {dur}s")
            ok = make_ken_burns_clip(img, clip_path, motion, dur, args.fps, crf, preset)
            if not ok:
                print(f"    SKIPPED due to error")
                continue
            size_mb = clip_path.stat().st_size / 1_048_576
            print(f"    → {size_mb:.1f}MB")

        clip_paths.append(clip_path)
        durations.append(dur)

    if not clip_paths:
        print("No clips generated.")
        sys.exit(1)

    # ── Step 2: Assemble with crossfade ───────────────────────────────────────
    section_label = args.section if args.section != "all" else "cold_open_creation"
    quality_label = "preview" if args.preview else "cinematic"
    output = OUTPUT_DIR / f"ot_part1_{section_label}_{quality_label}.mp4"

    print(f"\nAssembling {len(clip_paths)} clips with {xfade}s crossfade dissolves...")
    print(f"Output: {output}")

    # FFmpeg xfade can only handle ~50 clips at once in a single filter graph.
    # For larger sets, split into batches then concat.
    BATCH = 40
    if len(clip_paths) <= BATCH:
        ok = concat_with_xfade(clip_paths, durations, output, xfade, args.fps)
    else:
        # Split into batches, assemble each, then concat batches
        batch_files = []
        for b_start in range(0, len(clip_paths), BATCH):
            b_clips = clip_paths[b_start:b_start + BATCH]
            b_durs  = durations[b_start:b_start + BATCH]
            b_out   = OUTPUT_DIR / f"batch_{b_start:03d}.mp4"
            print(f"  Batch {b_start//BATCH + 1}: {len(b_clips)} clips → {b_out.name}")
            concat_with_xfade(b_clips, b_durs, b_out, xfade, args.fps)
            batch_files.append(b_out)

        # Final concat of batches (simple cut — crossfade already done within batches)
        concat_txt = OUTPUT_DIR / "concat_batches.txt"
        concat_txt.write_text("\n".join(f"file '{f.resolve()}'" for f in batch_files))
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy", str(output)
        ]
        ok = subprocess.run(cmd, capture_output=True).returncode == 0

    if ok:
        size_mb = output.stat().st_size / 1_048_576
        runtime = total * dur
        print(f"\nDone: {output}")
        print(f"  Size: {size_mb:.0f}MB | Runtime: {runtime/60:.1f} min ({runtime:.0f}s)")
    else:
        print(f"\nAssembly failed — check FFmpeg output above.")


if __name__ == "__main__":
    main()
