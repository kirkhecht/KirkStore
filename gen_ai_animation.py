#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
AI Animation Pipeline — Chapter 1 (Scenes 1-110)

Replaces Ken Burns static motion with real AI-generated in-frame animation
using minimax/video-01-live on Replicate.

Pipeline per scene:
  1. Load existing still image
  2. Call minimax/video-01-live with scene-specific motion prompt
  3. Download raw animated clip (~6s)
  4. Loop/trim animated clip to match audio duration
  5. Apply fade-in/fade-out
  6. Mux with existing David-voice audio (no regen — saves credits)
  7. Save final animated clip

Final step: concat all 110 animated clips into documentary MP4.

Usage:
    python gen_ai_animation.py                    # full run
    python gen_ai_animation.py --start 1 --end 10 # first 10 scenes
    python gen_ai_animation.py --skip-replicate   # re-render clips only (keep raw videos)
    python gen_ai_animation.py --assemble-only    # only run final concat
    python gen_ai_animation.py --test 3           # test first 3 scenes
"""

import os, sys, time, base64, subprocess, argparse, urllib.request, requests
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────
COLD_OPEN_DIR = Path("project/stories/ch01_cold_open")
CREATION_DIR  = Path("project/stories/ch01_the_creation")
AUDIO_DIR     = Path("project/documentary/audio")
RAW_AI_DIR    = Path("project/documentary/ai_raw")      # raw minimax output
AI_CLIPS_DIR  = Path("project/documentary/ai_clips")    # final muxed clips
OUTPUT_DIR    = Path("project/documentary")
FINAL_OUT     = OUTPUT_DIR / "ch01_ai_animated.mp4"

for d in [RAW_AI_DIR, AI_CLIPS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

IMAGE_DIRS = {"cold_open": COLD_OPEN_DIR, "creation": CREATION_DIR}

# ── Video config ──────────────────────────────────────────────────────────────
FPS  = 25
W, H = 1920, 1080
FADE = 0.25

# ── Scene manifest: (dir_key, filename, narration, motion_prompt) ─────────────
# Motion prompts describe the actual in-frame movement for minimax to generate.
SCENES = [
    # COLD OPEN ─────────────────────────────────────────────────────────────────
    ("cold_open", "001_title_ot_documentary.jpg",
     "The Old Testament. A cinematic documentary.",
     "cosmic nebula slowly swirling, golden light particles drifting through deep space, subtle ethereal movement"),

    ("cold_open", "002_part_1.jpg",
     "Part 1.",
     "faint cosmic dust motes floating slowly through infinite darkness, gentle light wisps shifting"),

    ("cold_open", "003_book_of_genesis.jpg",
     "The Book of Genesis. Creation to Babel.",
     "ancient stone tablet with faint glowing golden text, desert sand grains drifting slowly across surface"),

    ("cold_open", "004_cold_open_title.jpg",
     "Cold Open.",
     "single water droplet rippling outward in slow motion on still dark water surface, concentric rings expanding"),

    ("cold_open", "005_before_kingdoms.jpg",
     "Before kingdoms,",
     "wind slowly moving across vast ancient barren landscape, dust particles drifting, clouds shifting overhead"),

    ("cold_open", "006_before_nations.jpg",
     "before nations, before the first whisper of human breath,",
     "ancient forest canopy swaying gently in breeze, leaves rustling, morning mist drifting between trees"),

    ("cold_open", "007_before_egypt.jpg",
     "before the rise of Egypt,",
     "gentle desert wind rippling across Nile river surface, sand grains shifting along ancient riverbank"),

    ("cold_open", "008_before_mesopotamia.jpg",
     "before the cities of Mesopotamia,",
     "slow river current flowing through ancient landscape, reeds swaying at riverbank, water glinting"),

    ("cold_open", "009_before_stars_had_names.jpg",
     "before the stars had names,",
     "stars slowly twinkling across night sky, subtle nebula wisps shifting, cosmic atmosphere breathing"),

    ("cold_open", "010_the_deep.jpg",
     "there was only the deep,",
     "dark primordial water surface moving in slow gentle swells, mysterious ripples spreading from center"),

    ("cold_open", "011_vast_silent.jpg",
     "vast, silent,",
     "vast dark ocean gently undulating, slow deep swells rolling across the primordial waters"),

    ("cold_open", "012_formless_silence.jpg",
     "formless, and into that silence,",
     "formless void slowly shifting, dark water stirring very gently, atmosphere of profound stillness moving"),

    ("cold_open", "013_came_a_voice.jpg",
     "came a voice. This is the story of how everything began,",
     "divine golden light slowly pulsing and expanding, radiant beams shifting through the darkness"),

    ("cold_open", "014_first_light_first_betrayal.jpg",
     "of the first light, the first betrayal,",
     "golden light rays slowly sweeping across ancient landscape, dramatic light and shadow shifting"),

    ("cold_open", "015_first_murder_first_flood.jpg",
     "the first murder, the first flood,",
     "dark storm clouds slowly building on horizon, ominous sky shifting, distant lightning flicker"),

    ("cold_open", "016_world_born_perfect.jpg",
     "of a world that was born perfect and broken almost as quickly, of a family",
     "perfect world landscape with wind moving through trees and grass, peaceful motion"),

    ("cold_open", "017_fall_and_rise.jpg",
     "that would fall and rise and fall again,",
     "dramatic light shifting across landscape, clouds casting moving shadows, wind through tall grass"),

    ("cold_open", "018_creator_who.jpg",
     "and of a creator who,",
     "divine radiant light slowly pulsing from above, golden rays expanding outward, sacred atmosphere"),

    ("cold_open", "019_world_turned_against.jpg",
     "even when his world turned against him,",
     "turbulent clouds slowly moving across stormy sky, wind through ancient trees, dramatic atmosphere"),

    ("cold_open", "020_refused_to_walk_away.jpg",
     "refused to walk away. This is the Book of Genesis,",
     "warm divine golden light breaking through clouds, rays sweeping across landscape, hopeful atmosphere"),

    ("cold_open", "021_this_is_where_it_begins.jpg",
     "and this is where it all begins.",
     "dawn light slowly rising over ancient landscape, golden glow expanding across the horizon"),

    ("cold_open", "022_book_of_genesis_header.jpg",
     "Book of Genesis.",
     "ancient text glowing with soft golden light, dust motes floating slowly in sacred atmosphere"),

    ("cold_open", "023_genesis_1.jpg",
     "Genesis 1.",
     "ancient scroll or stone surface with soft ambient light slowly shifting, sacred atmosphere"),

    ("cold_open", "024_creation_of_the_world.jpg",
     "The Creation of the World.",
     "swirling cosmic energy forming slowly, golden light particles coalescing, universe taking shape"),

    ("cold_open", "025_before_recorded_history.jpg",
     "Approximately before recorded history.",
     "ancient untouched landscape with wind moving through grass, clouds drifting slowly overhead"),

    ("cold_open", "026_in_the_beginning_nothing.jpg",
     "In the beginning, there was nothing.",
     "absolute cosmic void with the very faintest light particles drifting, profound emptiness slowly breathing"),

    ("cold_open", "027_no_earth_no_sun.jpg",
     "No earth, no sun,",
     "deep space void with subtle cosmic dust wisps slowly drifting, no light only vast emptiness moving"),

    ("cold_open", "028_no_sky_no_time.jpg",
     "no sky, no measure of time, because time itself had not yet begun.",
     "timeless void with faint golden light wisps slowly undulating, ethereal cosmic atmosphere"),

    ("cold_open", "029_only_god_and_then.jpg",
     "Only God. And then,",
     "single point of divine light slowly growing and pulsing at center of infinite darkness"),

    ("cold_open", "030_a_word_first_sound.jpg",
     "a word. The first sound the universe had ever known,",
     "divine light bursting slowly outward from central point, golden shockwave expanding through darkness"),

    ("cold_open", "031_voice_over_darkness.jpg",
     "a voice moving over the darkness,",
     "luminous golden energy slowly sweeping across dark primordial waters surface, divine breath moving"),

    ("cold_open", "032_breath_stirring_deep.jpg",
     "a breath stirring across the deep,",
     "dark water surface gently stirring as if touched by divine breath, slow ripples spreading outward"),

    ("cold_open", "033_first_command.jpg",
     "and from that voice came the first command,",
     "radiant divine light building in intensity, golden rays slowly emanating from central source"),

    ("cold_open", "034_let_there_be_light.jpg",
     "let there be light,",
     "brilliant white-gold light explosion slowly expanding outward, blazing rays sweeping through darkness"),

    ("cold_open", "035_darkness_obeyed.jpg",
     "and the darkness obeyed.",
     "darkness slowly retreating as golden light advances, divine illumination spreading across the void"),

    ("cold_open", "036_light_tore_through.jpg",
     "Light tore through the emptiness,",
     "golden light rays dramatically sweeping through dark void, brilliant illumination expanding outward"),

    ("cold_open", "037_not_from_a_star.jpg",
     "not from a star, not from a sun,",
     "pure divine light pulsing softly, no stars visible, only sacred luminescence slowly breathing"),

    ("cold_open", "038_from_the_will.jpg",
     "because neither yet existed, but from the will of the one who spoke.",
     "divine golden light slowly radiating outward, sacred energy gently pulsing through the void"),

    ("cold_open", "039_light_spread.jpg",
     "And as the light spread,",
     "golden light slowly expanding in all directions, illuminating void, particles of light drifting outward"),

    ("cold_open", "040_universe_took_shape.jpg",
     "the universe began to take shape.",
     "cosmic matter slowly coalescing, nebulae forming gently, universe gradually taking form"),

    ("cold_open", "041_second_day.jpg",
     "On the second day,",
     "vast sky slowly opening up, clouds gently forming and drifting, heavens expanding"),

    ("cold_open", "042_heavens_opened.jpg",
     "the heavens opened. The sky stretched out like a vast canopy above the waters.",
     "sky canopy slowly expanding, clouds drifting apart to reveal vast blue heavens above shimmering water"),

    ("cold_open", "043_dry_land_rose.jpg",
     "On the third, dry land rose from the seas.",
     "rocky coastline with gentle ocean waves lapping at shore, spray rising slowly, land meeting sea"),

    ("cold_open", "044_mountains_pushed_upward.jpg",
     "Mountains pushed upward.",
     "mountain range with wind moving through rocky peaks, clouds slowly drifting past summit, majestic motion"),

    ("cold_open", "045_valleys_carved.jpg",
     "Valleys carved themselves into the earth.",
     "valley landscape with gentle wind through grass and trees, river slowly flowing in distance"),

    ("cold_open", "046_forests_bloomed.jpg",
     "Forests bloomed where there had only been silence.",
     "dense ancient forest canopy with leaves gently rustling in wind, birds flying through in background"),

    ("cold_open", "047_fourth_day_sun.jpg",
     "On the fourth day, the sun was set to blaze in the heavens.",
     "blazing sun slowly moving across sky, lens flare shifting, golden light rays sweeping across landscape"),

    ("cold_open", "048_moon_took_her_place.jpg",
     "The moon took her place in the night,",
     "full moon slowly rising in night sky, moonlight reflecting on water surface below, serene motion"),

    ("cold_open", "049_stars_glittering_eternal.jpg",
     "and the stars, countless, glittering, eternal,",
     "stars slowly twinkling and glittering across vast night sky, Milky Way gently pulsing with light"),

    ("cold_open", "050_scattered_across_dark.jpg",
     "were scattered across the dark,",
     "star field slowly rotating, individual stars twinkling, cosmic dust gently drifting through darkness"),

    ("cold_open", "051_pages_of_story.jpg",
     "like the pages of a story not yet written.",
     "stars and cosmic light slowly swirling, nebula wisps moving, cosmic storytelling atmosphere"),

    ("cold_open", "052_fifth_day.jpg",
     "On the fifth day,",
     "ocean surface with gentle waves, morning light reflecting, birds beginning to appear in distant sky"),

    ("cold_open", "053_life_began_to_move.jpg",
     "life began to move.",
     "underwater scene with fish gently swimming, fins moving fluidly, water flowing, first signs of life"),

    ("cold_open", "054_oceans_creatures_stirred.jpg",
     "In the oceans, creatures stirred,",
     "underwater ocean with schools of fish swimming gracefully, fins and tails moving, water currents flowing"),

    ("cold_open", "055_fish_leviathans.jpg",
     "schools of fish, Leviathans of the deep,",
     "massive sea creatures slowly moving through deep ocean, smaller fish swimming nearby, deep water currents"),

    # THE CREATION ───────────────────────────────────────────────────────────────
    ("creation", "056_things_never_seen.jpg",
     "things that had never been seen before, because they had never existed before.",
     "diverse ocean creatures swimming through clear tropical water, fish moving fluidly, coral swaying"),

    ("creation", "057_wings_unfurled.jpg",
     "In the skies, wings unfurled.",
     "large bird wings slowly spreading and unfurling against bright sky, feathers catching wind"),

    ("creation", "058_birds_rose.jpg",
     "Birds rose into the air,",
     "birds taking flight and soaring upward, wings flapping gracefully, ascending into blue sky"),

    ("creation", "059_calling_across_new_world.jpg",
     "calling to one another across the new world.",
     "birds flying in formation across pristine new world landscape, wings flapping, soaring together"),

    ("creation", "060_sixth_day_land_alive.jpg",
     "And on the sixth day, the land itself came alive.",
     "lush landscape with animals moving in distance, grass swaying in breeze, trees rustling"),

    ("creation", "061_cattle_on_hills.jpg",
     "Cattle on the hills,",
     "cattle slowly moving across grassy hills, tails flicking, heads lowering to graze, grass swaying"),

    ("creation", "062_wild_beasts_forests.jpg",
     "wild beasts in the forests,",
     "forest with wild animals moving between trees, leaves rustling in wind, dappled light shifting"),

    ("creation", "063_creeping_things.jpg",
     "creeping things in the grass.",
     "close-up of grass with small creatures moving through it, grass blades swaying in breeze"),

    ("creation", "064_shaped_with_intention.jpg",
     "Every creature shaped with intention,",
     "animals in natural habitat with gentle movement, wind through landscape, divine intentionality"),

    ("creation", "065_every_detail.jpg",
     "every detail considered,",
     "extreme close-up of animal detail with breathing movement, fur or feathers gently moving in breeze"),

    ("creation", "066_reflection_of_maker.jpg",
     "every form a reflection of the one who made them.",
     "diverse animals in golden light, gentle movement, sacred warm light slowly shifting"),

    ("creation", "067_at_the_very_end.jpg",
     "And then, at the very end,",
     "divine pause in creation, gentle wind across landscape, sacred golden light slowly building"),

    ("creation", "068_god_paused.jpg",
     "God paused. Because he was about to do something different.",
     "dramatic divine pause, golden light slowly intensifying, sacred atmosphere of anticipation"),

    ("creation", "069_reached_into_dust.jpg",
     "He reached down into the dust of the earth he had just made.",
     "close-up of earth dust and soil with divine golden light touching it, particles slowly lifting"),

    ("creation", "070_gathered_in_hands.jpg",
     "He gathered it in his hands.",
     "divine hands cupping earth dust, golden particles of dust slowly floating upward in sacred light"),

    ("creation", "071_shaped_not_animal.jpg",
     "And he shaped it, not into another animal,",
     "clay or dust being shaped by divine hands, form slowly emerging, sacred golden light"),

    ("creation", "072_carry_his_own_image.jpg",
     "not into another beast, but into something that would carry his own image.",
     "sacred light slowly revealing human form emerging from dust, divine radiance pulsing"),

    ("creation", "073_breathed_into_it.jpg",
     "He breathed into it,",
     "golden breath of life slowly flowing into still form, divine light particles entering, sacred moment"),

    ("creation", "074_dust_became_man.jpg",
     "and dust became man.",
     "man slowly awakening from stillness, gentle breath beginning, eyes slowly opening, divine light warming face"),

    ("creation", "075_first_time_universe.jpg",
     "For the first time in the history of the universe,",
     "first man standing in awe, looking upward, gentle wind through hair, golden light bathing him"),

    ("creation", "076_stood_upright_face_of_maker.jpg",
     "a creature stood upright and looked into the face of his maker.",
     "man looking upward in wonder toward divine light, gentle wind, sacred moment of first encounter"),

    ("creation", "077_his_name_was_adam.jpg",
     "His name was Adam,",
     "Adam standing tall in golden Eden light, hair gently moving in breeze, warm light on olive skin"),

    ("creation", "078_seventh_day.jpg",
     "and on the seventh day,",
     "peaceful creation scene with gentle stillness, soft wind, divine rest atmosphere, light slowly fading warm"),

    ("creation", "079_creator_rested.jpg",
     "the creator rested. Not because he was tired, but because the work was",
     "peaceful Eden landscape with gentle breeze through trees, birds flying in distance, perfect stillness"),

    ("creation", "080_finished_perfect.jpg",
     "finished. The world was perfect.",
     "perfect paradise landscape with flowers swaying, streams flowing gently, birds soaring, golden light"),

    ("creation", "081_would_not_stay.jpg",
     "It would not stay that way for long.",
     "ominous shadow slowly creeping at edge of paradise, wind picking up slightly, foreboding atmosphere"),

    ("creation", "082_genesis_2_3.jpg",
     "Genesis 2 and 3.",
     "ancient text with soft divine light, dust motes floating slowly, sacred scrolls atmosphere"),

    ("creation", "083_adam.jpg",
     "Adam,",
     "Adam in Eden light with gentle wind moving through his dark hair, warm olive skin glowing, peaceful"),

    ("creation", "084_eve_fall_of_man.jpg",
     "Eve, and the fall of man.",
     "dramatic golden-red light slowly shifting, Eden garden beginning to look ominous, wind building slightly"),

    ("creation", "085_dawn_of_humanity.jpg",
     "The dawn of humanity,",
     "dawn light slowly rising over Eden, golden glow warming the garden, birds waking and flying"),

    ("creation", "086_god_planted_a_garden.jpg",
     "in the east, God planted a garden,",
     "lush garden coming to life with flowers blooming slowly, leaves unfurling, divine garden energy"),

    ("creation", "087_place_called_eden.jpg",
     "a place called Eden, a paradise unlike anything the earth would ever see again.",
     "sweeping pan across Eden paradise with waterfalls flowing, flowers swaying, birds flying, luminous light"),

    ("creation", "088_rivers_flowed.jpg",
     "Rivers flowed through it,",
     "crystal clear river flowing through Eden, water sparkling, gentle current moving, fish visible below"),

    ("creation", "089_trees_heavy_fruit.jpg",
     "trees heavy with fruit lined its paths,",
     "fruit trees with ripe fruit slowly swaying in gentle breeze, leaves rustling, abundance visible"),

    ("creation", "090_animals_no_fear.jpg",
     "animals roamed without fear.",
     "diverse animals peacefully moving through Eden garden, lions and lambs nearby, no fear visible"),

    ("creation", "091_no_death.jpg",
     "There was no death here,",
     "paradise scene with eternal life light slowly pulsing, golden glow, perfect harmony and stillness"),

    ("creation", "092_no_sickness_no_sorrow.jpg",
     "no sickness, no sorrow,",
     "perfect garden scene with soft golden light, flowers swaying, total peaceful harmony"),

    ("creation", "093_no_hunger_no_shame.jpg",
     "no hunger, no shame,",
     "abundant garden with fruit everywhere, gentle wind through trees, total contentment and peace"),

    ("creation", "094_two_trees.jpg",
     "and in the center of the garden stood two trees,",
     "two magnificent trees in center of garden, leaves gently rustling, magical light around them"),

    ("creation", "095_tree_of_life.jpg",
     "the tree of life,",
     "glowing tree of life with golden light emanating from within, leaves slowly moving in divine breeze"),

    ("creation", "096_tree_of_knowledge.jpg",
     "and the tree of the knowledge of good and evil.",
     "forbidden tree with mysterious red and gold glow, leaves slowly swaying, ominous beautiful atmosphere"),

    ("creation", "097_adam_receiving_rule.jpg",
     "God placed Adam in the garden and gave him only one rule.",
     "Adam listening intently, gentle wind in hair, golden divine light, sacred moment of instruction"),

    ("creation", "098_all_trees_permitted.jpg",
     "He could eat from any tree.",
     "abundant fruit trees in Eden with Adam gesturing freely, wind through leaves, abundance everywhere"),

    ("creation", "099_adam_picking_fruit.jpg",
     "Any tree at all,",
     "Adam reaching for fruit from abundant tree, gentle wind, golden light on dark hair and olive skin"),

    ("creation", "100_forbidden_fruit.jpg",
     "except one. Do not eat from the tree of the knowledge of good and evil.",
     "forbidden tree glowing with mysterious light, Adam looking at it with restraint, ominous beauty"),

    ("creation", "101_adam_warning.jpg",
     "For in the day you eat of it,",
     "Adam's face in dramatic light with warning expression, wind through hair, sacred gravity of moment"),

    ("creation", "102_single_command.jpg",
     "you will surely die. It was a single command,",
     "dramatic light and shadow on Adam's face, wind through dark hair, weight of the single rule"),

    ("creation", "103_one_boundary.jpg",
     "a single boundary, in a world overflowing with abundance.",
     "vast Eden paradise with single tree set apart, contrast of abundant world vs one boundary"),

    ("creation", "104_adam_alone_eden.jpg",
     "But Adam was alone,",
     "Adam alone in vast beautiful Eden, gentle wind, looking around at paradise but longing visible"),

    ("creation", "105_adam_alone_sunset.jpg",
     "and God said it was not good for man to be alone.",
     "Adam at sunset in Eden garden, golden light, gentle wind through hair, contemplative loneliness"),

    ("creation", "106_adam_deep_sleep.jpg",
     "So as Adam slept, God formed a companion for him,",
     "Adam sleeping peacefully, divine golden light slowly gathering, sacred creation happening beside him"),

    ("creation", "107_rib_drawn_out.jpg",
     "bone of his bone,",
     "divine golden light at Adam's side, sacred formation happening, gentle ethereal movement"),

    ("creation", "108_eve_forming.jpg",
     "flesh of his flesh.",
     "Eve slowly emerging from divine light, form gradually becoming visible, sacred beautiful creation"),

    ("creation", "109_eve_portrait.jpg",
     "Her name was Eve.",
     "Eve standing in golden Eden light, long dark hair gently moving in breeze, warm olive skin glowing"),

    ("creation", "110_adam_eve_together.jpg",
     "And for a time, for how long we do not know,",
     "Adam and Eve together in Eden paradise, gentle wind, golden light, birds flying overhead in peace"),
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


def get_audio_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())


def get_video_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True
    )
    return float(r.stdout.strip())


def call_replicate(img_path, motion_prompt, raw_out, api_token):
    """Call minimax/video-01-live via Replicate REST API with polling. Returns path to downloaded video."""
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    img_b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
    data_uri = f"data:image/jpeg;base64,{img_b64}"

    # Start prediction
    print(f"    → Submitting to Replicate (minimax/video-01-live)...")
    resp = requests.post(
        "https://api.replicate.com/v1/models/minimax/video-01-live/predictions",
        headers=headers,
        json={
            "input": {
                "prompt": motion_prompt,
                "first_frame_image": data_uri,
                "prompt_optimizer": False,
            }
        },
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Replicate submit error {resp.status_code}: {resp.text[:300]}")

    pred = resp.json()
    pred_id = pred["id"]
    poll_url = pred.get("urls", {}).get("get", f"https://api.replicate.com/v1/predictions/{pred_id}")
    print(f"    → Prediction {pred_id} submitted, polling...")

    # Poll until complete (max 10 minutes)
    for attempt in range(120):
        time.sleep(5)
        r = requests.get(poll_url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"    → Poll error {r.status_code}, retrying...")
            continue
        status = r.json().get("status")
        if status == "succeeded":
            output = r.json().get("output")
            break
        elif status == "failed":
            err = r.json().get("error", "unknown")
            raise RuntimeError(f"Replicate prediction failed: {err}")
        elif attempt % 6 == 0:
            print(f"    → Status: {status} ({attempt * 5}s elapsed)...")
    else:
        raise RuntimeError("Replicate prediction timed out after 10 minutes")

    # output is a URL string
    if isinstance(output, list):
        video_url = output[0]
    else:
        video_url = str(output)

    print(f"    → Downloading video...")
    urllib.request.urlretrieve(video_url, str(raw_out))

    size_mb = raw_out.stat().st_size / 1024 / 1024
    print(f"    → Raw AI clip saved ({size_mb:.1f} MB)")
    return raw_out


def make_animated_clip(raw_video, audio_path, out_path, audio_dur):
    """
    Loop/trim raw AI video to match audio_dur, apply fades, mux with audio.
    raw_video: Path to minimax output (typically ~6s)
    audio_dur: target duration in seconds
    """
    video_dur = audio_dur  # final clip duration = audio duration

    raw_dur = get_video_duration(raw_video)

    # Build video filter chain
    # If raw_dur < audio_dur: loop it
    # If raw_dur >= audio_dur: trim it
    fade_in_end  = FADE
    fade_out_st  = max(0.0, video_dur - FADE)

    if raw_dur < video_dur:
        # Loop the video to cover audio duration, then trim
        loop_count = int(video_dur / raw_dur) + 2
        vf = (
            f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
            f"loop={loop_count}:size=32767:start=0,"
            f"trim=0:{video_dur:.3f},"
            f"setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d={FADE},"
            f"fade=t=out:st={fade_out_st:.3f}:d={FADE},"
            f"format=yuv420p"
        )
    else:
        # Trim to audio duration
        vf = (
            f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
            f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
            f"trim=0:{video_dur:.3f},"
            f"setpts=PTS-STARTPTS,"
            f"fade=t=in:st=0:d={FADE},"
            f"fade=t=out:st={fade_out_st:.3f}:d={FADE},"
            f"format=yuv420p"
        )

    af = (
        f"apad=pad_dur={video_dur:.3f},"
        f"atrim=0:{video_dur:.3f},"
        f"afade=t=in:st=0:d=0.1,"
        f"afade=t=out:st={max(0, video_dur - 0.15):.3f}:d=0.1"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
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
        raise RuntimeError(f"FFmpeg error for {out_path.name}:\n{r.stderr[-600:]}")


def assemble_documentary(clip_paths, final_out):
    """Concat all animated clips into final MP4 using FFmpeg concat demuxer."""
    list_file = OUTPUT_DIR / "ai_concat_list.txt"
    with open(list_file, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve()}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(final_out),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Assembly FFmpeg error:\n{r.stderr[-600:]}")
    size_mb = final_out.stat().st_size / 1024 / 1024
    print(f"\n✓ Final documentary: {final_out} ({size_mb:.1f} MB)")


def submit_predictions(scenes_to_submit, replicate_token, state_file):
    """
    Submit all pending scenes to Replicate in one fast pass (~1-2s each).
    Saves prediction IDs to a JSON state file so collect_results can poll them.
    """
    import json

    # Load existing state
    state = {}
    if state_file.exists():
        state = json.loads(state_file.read_text())

    headers = {
        "Authorization": f"Bearer {replicate_token}",
        "Content-Type": "application/json",
    }

    submitted = 0
    for scene_num, img_path, motion_prompt in scenes_to_submit:
        key = str(scene_num)
        raw_path = RAW_AI_DIR / f"{scene_num:03d}_raw.mp4"

        if raw_path.exists():
            print(f"  [{scene_num:03d}] Raw clip exists, skipping")
            continue
        if key in state and state[key].get("status") in ("processing", "succeeded"):
            print(f"  [{scene_num:03d}] Already submitted ({state[key].get('status')}), skipping")
            continue

        img_b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
        data_uri = f"data:image/jpeg;base64,{img_b64}"

        resp = requests.post(
            "https://api.replicate.com/v1/models/minimax/video-01-live/predictions",
            headers=headers,
            json={"input": {"prompt": motion_prompt, "first_frame_image": data_uri, "prompt_optimizer": False}},
            timeout=30,
        )
        if resp.status_code not in (200, 201):
            print(f"  [{scene_num:03d}] ✗ Submit error {resp.status_code}: {resp.text[:200]}")
            continue

        pred = resp.json()
        pred_id = pred["id"]
        state[key] = {"pred_id": pred_id, "status": "processing"}
        state_file.write_text(json.dumps(state, indent=2))
        print(f"  [{scene_num:03d}] Submitted → {pred_id}")
        submitted += 1
        time.sleep(0.5)  # gentle rate limiting

    print(f"\nSubmitted {submitted} new predictions. State saved to {state_file}")
    return state


def collect_results(replicate_token, state_file):
    """
    Poll all in-flight Replicate predictions. Download and mux completed ones.
    Designed to run in short bursts (< 8 minutes) — call repeatedly until all done.
    """
    import json

    if not state_file.exists():
        print("No state file found. Run --submit-only first.")
        return

    state = json.loads(state_file.read_text())
    headers = {"Authorization": f"Bearer {replicate_token}"}

    pending = [(k, v) for k, v in state.items() if v.get("status") == "processing"]
    print(f"\nPolling {len(pending)} in-flight predictions...")

    for key, info in pending:
        scene_num = int(key)
        pred_id = info["pred_id"]
        raw_path = RAW_AI_DIR / f"{scene_num:03d}_raw.mp4"
        clip_path = AI_CLIPS_DIR / f"{scene_num:03d}.mp4"
        audio_path = AUDIO_DIR / f"{scene_num:03d}.mp3"

        if raw_path.exists():
            state[key]["status"] = "downloaded"
            state_file.write_text(json.dumps(state, indent=2))
            continue

        poll_url = f"https://api.replicate.com/v1/predictions/{pred_id}"
        try:
            r = requests.get(poll_url, headers=headers, timeout=15)
            if r.status_code != 200:
                print(f"  [{scene_num:03d}] Poll error {r.status_code}")
                continue
            pred_status = r.json().get("status")
            output = r.json().get("output")
        except Exception as e:
            print(f"  [{scene_num:03d}] Poll exception: {e}")
            continue

        if pred_status == "succeeded" and output:
            video_url = output[0] if isinstance(output, list) else str(output)
            print(f"  [{scene_num:03d}] Succeeded → downloading...")
            try:
                urllib.request.urlretrieve(video_url, str(raw_path))
                size_mb = raw_path.stat().st_size / 1024 / 1024
                state[key]["status"] = "downloaded"
                state_file.write_text(json.dumps(state, indent=2))
                print(f"  [{scene_num:03d}] Downloaded ({size_mb:.1f} MB)")
            except Exception as e:
                print(f"  [{scene_num:03d}] Download error: {e}")
        elif pred_status == "failed":
            err = r.json().get("error", "unknown")
            print(f"  [{scene_num:03d}] ✗ Failed: {err}")
            state[key]["status"] = "failed"
            state_file.write_text(json.dumps(state, indent=2))
        else:
            print(f"  [{scene_num:03d}] Still {pred_status}...")

    # Mux all downloaded raw clips that don't have final clips yet
    print(f"\nMuxing downloaded clips...")
    muxed = 0
    for key, info in state.items():
        if info.get("status") not in ("downloaded", "succeeded"):
            continue
        scene_num = int(key)
        raw_path = RAW_AI_DIR / f"{scene_num:03d}_raw.mp4"
        clip_path = AI_CLIPS_DIR / f"{scene_num:03d}.mp4"
        audio_path = AUDIO_DIR / f"{scene_num:03d}.mp3"

        if clip_path.exists() or not raw_path.exists() or not audio_path.exists():
            continue

        audio_dur = get_audio_duration(audio_path) + 0.45
        print(f"  [{scene_num:03d}] Muxing ({audio_dur:.2f}s)...")
        try:
            make_animated_clip(raw_path, audio_path, clip_path, audio_dur)
            print(f"  [{scene_num:03d}] ✓ Clip ready")
            muxed += 1
        except Exception as e:
            print(f"  [{scene_num:03d}] ✗ Mux error: {e}")

    # Summary
    done = sum(1 for i in range(1, 111) if (AI_CLIPS_DIR / f"{i:03d}.mp4").exists())
    still_processing = sum(1 for v in state.values() if v.get("status") == "processing")
    print(f"\nSummary: {done}/110 clips ready | {still_processing} still processing on Replicate | {muxed} newly muxed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",            type=int, default=0,   help="Only process first N scenes")
    parser.add_argument("--start",           type=int, default=1,   help="Start at scene N (1-indexed)")
    parser.add_argument("--end",             type=int, default=110, help="End at scene N")
    parser.add_argument("--skip-replicate",  action="store_true",   help="Skip Replicate calls, reuse raw clips")
    parser.add_argument("--assemble-only",   action="store_true",   help="Skip to final assembly only")
    parser.add_argument("--submit-only",     action="store_true",   help="Submit all predictions to Replicate (fast, no polling)")
    parser.add_argument("--collect-only",    action="store_true",   help="Poll Replicate, download+mux completed predictions")
    args = parser.parse_args()

    env = load_env()
    replicate_token = env.get("REPLICATE_API_TOKEN", "")
    if not replicate_token and not args.skip_replicate and not args.assemble_only:
        sys.exit("REPLICATE_API_TOKEN not in .env")

    state_file = OUTPUT_DIR / "replicate_state.json"

    # ── Submit-only mode: fire all predictions to Replicate (fast) ───────────────
    if args.submit_only:
        scenes_to_submit = []
        for i, (dir_key, filename, narration, motion_prompt) in enumerate(SCENES):
            scene_num = i + 1
            img_path = IMAGE_DIRS[dir_key] / filename
            if img_path.exists():
                scenes_to_submit.append((scene_num, img_path, motion_prompt))
        print(f"\nSubmitting {len(scenes_to_submit)} scenes to Replicate...")
        submit_predictions(scenes_to_submit, replicate_token, state_file)
        return

    # ── Collect-only mode: poll + download + mux completed predictions ───────────
    if args.collect_only:
        collect_results(replicate_token, state_file)
        return

    # ── Assemble-only mode ───────────────────────────────────────────────────────
    if not args.assemble_only:
        scenes = SCENES
        if args.test:
            scenes = SCENES[:args.test]
        elif args.start != 1 or args.end != 110:
            scenes = SCENES[args.start - 1 : args.end]

        print(f"\n{'='*60}")
        print(f"  AI Animation Pipeline — {len(scenes)} scenes")
        print(f"{'='*60}")

        for i, (dir_key, filename, narration, motion_prompt) in enumerate(scenes):
            scene_num = (args.start + i) if not args.test else (i + 1)
            img_path   = IMAGE_DIRS[dir_key] / filename
            audio_path = AUDIO_DIR / f"{scene_num:03d}.mp3"
            raw_path   = RAW_AI_DIR / f"{scene_num:03d}_raw.mp4"
            clip_path  = AI_CLIPS_DIR / f"{scene_num:03d}.mp4"

            if not img_path.exists():
                print(f"  [{scene_num:03d}] ✗ Image missing: {img_path}")
                continue
            if not audio_path.exists():
                print(f"  [{scene_num:03d}] ✗ Audio missing: {audio_path}")
                continue

            print(f"\n  [{scene_num:03d}] {filename}")

            if not args.skip_replicate and not raw_path.exists():
                try:
                    call_replicate(img_path, motion_prompt, raw_path, replicate_token)
                except Exception as e:
                    print(f"    ✗ Replicate error: {e}")
                    continue
            elif raw_path.exists():
                print(f"    → Raw AI clip exists, skipping Replicate call")
            else:
                print(f"    ✗ --skip-replicate set but no raw clip at {raw_path}")
                continue

            if clip_path.exists():
                print(f"    → Final clip exists, skipping mux")
                continue

            audio_dur = get_audio_duration(audio_path) + 0.45
            print(f"    → Muxing (audio dur: {audio_dur:.2f}s)...")
            try:
                make_animated_clip(raw_path, audio_path, clip_path, audio_dur)
                clip_dur = get_video_duration(clip_path)
                print(f"    ✓ Clip ready ({clip_dur:.2f}s)")
            except Exception as e:
                print(f"    ✗ Mux error: {e}")

    # Phase 3: Assembly
    print(f"\n{'='*60}")
    print(f"  Assembly — collecting all 110 clips")
    print(f"{'='*60}")

    all_clips = []
    missing = []
    for i in range(1, 111):
        p = AI_CLIPS_DIR / f"{i:03d}.mp4"
        if p.exists():
            all_clips.append(p)
        else:
            missing.append(i)

    if missing:
        print(f"  Missing clips: {missing}")
        print(f"  Assembling {len(all_clips)} available clips...")
    else:
        print(f"  All 110 clips ready. Assembling final documentary...")

    if not all_clips:
        print("  Nothing to assemble.")
        return

    assemble_documentary(all_clips, FINAL_OUT)

    # Optional: 720p web version
    web_out = OUTPUT_DIR / "ch01_ai_animated_720p.mp4"
    print(f"\nEncoding 720p web version...")
    cmd720 = [
        "ffmpeg", "-y", "-i", str(FINAL_OUT),
        "-vf", "scale=1280:720",
        "-c:v", "libx264", "-preset", "fast", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        str(web_out),
    ]
    r = subprocess.run(cmd720, capture_output=True, text=True)
    if r.returncode == 0:
        size_mb = web_out.stat().st_size / 1024 / 1024
        print(f"✓ Web version: {web_out} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
