#!/usr/bin/env python3
"""
Fix Chapter 2 images — consistent characters, correct serpent, correct fruit, no nudity.

Key fixes:
  - Eve: consistently Middle Eastern, long dark wavy hair, white linen dress (pre-fall),
         fig leaf garment (post-awareness), animal skin dress (post-exile)
  - Adam: consistently Middle Eastern, dark wavy hair, white linen kilt (pre-fall),
          fig leaf kilt (post-awareness), animal skin tunic (post-exile)
  - Serpent: enormous ancient serpent with iridescent jade-green and gold scales,
             powerful crested head — matches Chapter 1 reference image
  - Tree: deep red pomegranates, golden apples, dark figs — NO pine cones
  - Safety: no modern vehicles, no motorcycles, no modern clothing/architecture
  - Nudity: scenes 031-036 use tasteful framing, camera angles, foliage

Usage:
    python fix_ch02_images.py                        # regenerate all problem scenes
    python fix_ch02_images.py --scenes 2,11,15,36    # specific scenes only
    python fix_ch02_images.py --start 11 --end 20    # range
    python fix_ch02_images.py --force                # overwrite even existing images
    python fix_ch02_images.py --dry-run              # print prompts, no generation
"""

import os, sys, time, base64, argparse, requests
from pathlib import Path

OUT_DIR = Path("project/stories/ch02_the_fall")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Consistent character + setting descriptors ─────────────────────────────────

# Serpent — matches the magnificent serpent from Chapter 1
SERPENT = (
    "enormous ancient serpent with iridescent jade-green and gold scales that shimmer brilliantly, "
    "powerful muscular coiled body, regal majestic crested head with golden feather-like spiky "
    "scales forming a crown, deep intelligent golden-amber eyes, forked tongue, "
    "far larger and more magnificent than any normal snake, ancient and powerful"
)

# Eve — pre-fall (scenes 002-032): plain white linen dress, Middle Eastern
EVE = (
    "Eve: ancient Middle Eastern woman, warm olive tan skin, long dark wavy black hair past her shoulders, "
    "almond-shaped dark brown eyes, Levantine features, ordinary natural appearance, early 20s, "
    "wearing a simple sleeveless ankle-length plain white linen dress loosely draped, "
    "plain woven fabric not fur not leather, barefoot"
)

# Eve — fig-leaf period (scenes 033-049)
EVE_FIG = (
    "Eve: ancient Middle Eastern woman, warm olive tan skin, long dark wavy black hair, "
    "almond-shaped dark brown eyes, Levantine features, ordinary natural appearance, early 20s, "
    "wearing a hastily sewn garment of large broad green fig leaves covering her body, "
    "ancient biblical era"
)

# Eve — after God clothes them (scenes 050-055)
EVE_SKIN = (
    "Eve: ancient Middle Eastern woman, warm olive tan skin, long dark wavy black hair, "
    "dark brown eyes, Levantine features, ordinary natural appearance, early 20s, "
    "wearing a simple rough-hewn animal skin wrap dress, belted at the waist, ancient biblical era"
)

# Adam — pre-fall (scenes 002-032): linen tunic, Middle Eastern, ordinary build
ADAM = (
    "Adam: ancient Middle Eastern man, warm olive tan skin, dark wavy black hair, "
    "prominent nose, dark brown eyes, ordinary average build not muscular not idealized, early 30s, "
    "wearing a simple plain rough linen tunic, plain woven fabric, barefoot"
)

# Adam — fig-leaf period (scenes 033-049)
ADAM_FIG = (
    "Adam: ancient Middle Eastern man, warm olive tan skin, dark wavy black hair, "
    "prominent nose, dark brown eyes, ordinary average build not muscular, early 30s, "
    "wearing a crude woven fig leaf garment around his waist, ancient biblical era"
)

# Adam — after God clothes them (scenes 050-055)
ADAM_SKIN = (
    "Adam: ancient Middle Eastern man, warm olive tan skin, dark wavy black hair, "
    "prominent nose, dark brown eyes, ordinary average build not muscular, early 30s, "
    "wearing a simple belted animal skin tunic, ancient biblical era"
)

# The forbidden tree
TREE = (
    "the sacred forbidden Tree of Knowledge: massive ancient tree with deeply gnarled dark bark, "
    "enormous canopy heavy with deep red pomegranates, golden apples, and dark luscious figs, "
    "absolutely NO pine cones NO pine trees NO conifer elements, "
    "surrounded by a subtle mystical golden-red glow that sets it apart from all other trees"
)

# Eden background
EDEN = (
    "lush ancient Garden of Eden, towering fruit trees with golden light filtering through canopy, "
    "exotic tropical flowers, crystal clear rivers, vibrant green paradise"
)

# Cinematic style + anti-hallucination guard
C = (
    "ultra photorealistic, 8K cinema camera, IMAX cinematic quality, dramatic lighting, "
    "no text overlays no watermarks no subtitles, film grain, anamorphic lens flare, movie still frame, "
    "ancient biblical setting only, absolutely no modern vehicles no motorcycles no cars no modern clothing "
    "no modern buildings no contemporary elements, strictly ancient biblical era, "
    "inspired by Ridley Scott epic cinematography"
)

# ── Scene definitions ──────────────────────────────────────────────────────────
SCENES = [

    (1, "001_the_fall_title.jpg",
     f"Ancient stone tablet partially buried in Eden garden soil, carved text glowing faint amber, "
     f"fallen deep-red pomegranates on lush green grass, dramatic golden light through ancient trees, "
     f"a shadow beginning to creep across paradise, no humans. {C}"),

    (2, "002_they_had_everything.jpg",
     f"Wide cinematic establishing shot: {ADAM} and {EVE} standing together at the edge of endless "
     f"Eden paradise, both gazing out over crystal rivers and towering fruit-laden trees stretching "
     f"to the horizon, golden divine light bathing everything, absolute paradise in every direction. "
     f"{EDEN}. {C}"),

    (3, "003_garden_without_end.jpg",
     f"Breathtaking aerial view of the Garden of Eden stretching to every horizon, "
     f"rivers branching in four directions through lush green paradise, "
     f"mountains of fruit trees, exotic flowers in full bloom, golden afternoon light, "
     f"absolute perfection, no humans visible. {C}"),

    (4, "004_rivers_of_clear_water.jpg",
     f"Crystal clear ancient river in Eden flowing over smooth stones, "
     f"water so transparent every pebble visible beneath, "
     f"vibrant green ferns and tropical flowers lining both banks, "
     f"golden light sparkling on the water surface, no humans. {C}"),

    (5, "005_fruit_heavy_on_branches.jpg",
     f"Close-up of ancient fruit tree branches impossibly heavy with ripe fruit: "
     f"deep red pomegranates, golden apples, purple figs, dates — lush divine abundance, "
     f"absolutely NO pine cones NO conifer elements, warm amber light illuminating fruit from behind, "
     f"Eden garden softly in background, no humans. {C}"),

    (6, "006_animals_that_came_when_called.jpg",
     f"{ADAM} standing peacefully in Eden surrounded by animals with no fear: "
     f"a majestic lion resting at his feet, a deer beside him, colorful exotic birds perched on his "
     f"outstretched arm, a lamb in the foreground, total peace between man and beast, "
     f"golden Eden light. {EDEN}. {C}"),

    (7, "007_god_walked_cool_of_day.jpg",
     f"Long winding ancient footpath through Eden garden at golden hour, "
     f"divine presence suggested by a radiant pillar of warm golden light between the ancient trees, "
     f"two sets of human barefoot footprints in soft earth alongside a luminous divine path, "
     f"warm amber light filtering through ancient canopy, sacred and peaceful atmosphere, "
     f"no modern elements whatsoever, ancient garden path only. {C}"),

    (8, "008_one_thing_not_to_touch.jpg",
     f"{TREE} standing alone in a clearing at the heart of Eden, "
     f"other trees keeping a slight reverent distance, "
     f"atmospheric tension, golden-red light emanating from it, "
     f"no humans in frame. {EDEN}. {C}"),

    (9, "009_one_tree.jpg",
     f"Extreme close-up portrait of {TREE}, "
     f"ancient deeply gnarled dark bark with subtle inner glow, "
     f"deep red pomegranates and golden apples hanging tantalizingly close, "
     f"ominous beautiful atmosphere, sacred and dangerous. {C}"),

    (10, "010_that_was_enough.jpg",
     f"Wide shot of vast Eden garden with {TREE} visible at its center, "
     f"small but drawing the eye irresistibly, "
     f"all of paradise spread around it, "
     f"golden light across the garden, dramatic composition, no humans. {C}"),

    (11, "011_serpent_most_cunning.jpg",
     f"Close-up portrait of {SERPENT} coiled elegantly around a large branch in Eden garden, "
     f"iridescent jade-green and gold scales catching golden light brilliantly, "
     f"intelligent golden-amber eyes fixed directly at camera, "
     f"beautiful and dangerous, unlike any other creature, lush Eden foliage in background, "
     f"no humans, no modern elements. {C}"),

    (12, "012_serpent_came_to_eve.jpg",
     f"{EVE} alone near the forbidden tree in Eden, "
     f"{SERPENT} descending sinuously from a branch toward her, "
     f"its intelligent golden eyes level with hers, "
     f"intimate close scene, golden afternoon light, tension beginning. {C}"),

    (13, "013_did_god_really_say.jpg",
     f"Extreme close-up of {SERPENT}'s magnificent crested head, inches from {EVE}'s ear, "
     f"golden intelligent eyes, forked tongue barely visible, "
     f"Eve's dark hair and olive skin at edge of frame, "
     f"tension and temptation, dramatic lighting, ancient garden setting. {C}"),

    (14, "014_eve_answered.jpg",
     f"{EVE} standing thoughtfully before the serpent in Eden garden, "
     f"her expression composed but uncertain, gesturing slightly toward the garden around her, "
     f"{SERPENT} listening intently coiled on a branch, "
     f"warm light on her olive skin, the abundant garden behind her. {C}"),

    (15, "015_may_eat_from_trees.jpg",
     f"{EVE} gesturing gracefully across vast Eden garden filled with fruit trees, "
     f"her arm extended toward the abundance of paradise, "
     f"countless trees heavy with pomegranates and golden apples in every direction, "
     f"the generosity of creation visible everywhere, golden light, ancient biblical setting. {C}"),

    (16, "016_not_from_center_tree.jpg",
     f"{EVE} turning toward {TREE} pointing at it with solemn expression, "
     f"her expression carrying the weight of God's warning, "
     f"{SERPENT} watching her carefully from a nearby branch, studying her reaction, "
     f"ominous atmosphere. {C}"),

    (17, "017_serpent_smiled.jpg",
     f"Close-up of {SERPENT}'s magnificent crested face showing a chilling expression of cunning satisfaction, "
     f"iridescent jade-green and gold scales gleaming, golden eyes lit with knowing intelligence, "
     f"the ghost of a smile on its features, "
     f"dramatic ominous close-up, Eden foliage behind. {C}"),

    (18, "018_you_will_not_die.jpg",
     f"{SERPENT} coiled gracefully before {EVE}, speaking with absolute confidence, "
     f"Eve listening, her expression shifting from caution toward curiosity, "
     f"{TREE} glowing behind them both. {C}"),

    (19, "019_eyes_will_be_opened.jpg",
     f"Extreme close-up of {SERPENT}'s penetrating golden-amber eyes, unnaturally wise and knowing, "
     f"reflecting the image of the forbidden tree in their depths, "
     f"ancient intelligence and deception visible in their gleam. {C}"),

    (20, "020_like_god_knowing.jpg",
     f"{SERPENT} rearing upright with regal confidence, crested head raised, "
     f"{EVE} looking up intrigued, expression caught between wonder and uncertainty, "
     f"{TREE} framing the moment, "
     f"the greatest lie ever told hanging in the air. {C}"),

    (21, "021_eve_looked_at_tree.jpg",
     f"Profile portrait of {EVE} gazing at {TREE}, "
     f"her dark almond-shaped eyes reflecting the tree's golden-red glow, "
     f"expression of deep longing and contemplation, "
     f"the tree filling half the frame, warm golden-red light on her olive face. {C}"),

    (22, "022_fruit_good_for_food.jpg",
     f"Close-up of a perfectly ripe deep-red pomegranate from {TREE} hanging close to {EVE}'s face, "
     f"Eve's lips parted slightly, dark eyes fixed on the beautiful fruit, "
     f"the fruit impossibly lustrous and appealing. {C}"),

    (23, "023_beautiful_to_the_eye.jpg",
     f"Extreme close-up of the forbidden fruit — a deep-red pomegranate or golden apple — "
     f"skin rich and lustrous, catching warm golden light perfectly, "
     f"visually more beautiful than any other fruit, "
     f"{EVE}'s dark eyes visible at the edge of frame reflecting it. {C}"),

    (24, "024_desirable_for_wisdom.jpg",
     f"{EVE}'s face very close to the forbidden fruit, dark eyes wide with yearning, "
     f"desire and intellect warring on her beautiful olive face, "
     f"{SERPENT} watching from shadows of the branch above. {C}"),

    (25, "025_she_reached_out.jpg",
     f"Close-up of {EVE}'s hand — slender fingers with warm olive skin — "
     f"reaching out and closing around the forbidden pomegranate fruit, "
     f"the tree's glow pulsing at the moment of contact, "
     f"the most consequential moment in human history. {C}"),

    (26, "026_she_ate.jpg",
     f"Portrait of {EVE} biting into the forbidden fruit, eyes closing, "
     f"juice running over her lips, "
     f"an expression of ecstasy and something darker crossing her face, "
     f"the garden's light subtly changing around her. {C}"),

    (27, "027_gave_some_to_adam.jpg",
     f"{EVE} turning to {ADAM} with the bitten forbidden fruit extended toward him, "
     f"both in the shadow of {TREE}, "
     f"Eve's expression urgent and pleading, fruit in her outstretched hand, "
     f"Adam's face showing surprise and hesitation. {C}"),

    (28, "028_and_he_ate.jpg",
     f"{ADAM} taking the forbidden fruit and biting into it, "
     f"his eyes closing as he eats, "
     f"expression changing from hesitation to something irrevocable, "
     f"the garden light visibly shifting around them both, dramatic close-up. {C}"),

    (29, "029_in_that_instant.jpg",
     f"Wide cinematic shot of {ADAM} and {EVE} at {TREE} the moment after eating, "
     f"the garden light dramatically different, shadows deeper, "
     f"the golden paradise somehow diminished, sky subtly darker above them. {C}"),

    (30, "030_eyes_were_opened.jpg",
     f"Split composition: {ADAM}'s dark brown eyes and {EVE}'s dark almond eyes simultaneously in "
     f"extreme close-up, both pairs wide open with sudden awareness, "
     f"something fundamentally changed — the light of Eden reflected but also new terrible knowledge. {C}"),

    (31, "031_knew_they_were_naked.jpg",
     f"{ADAM} and {EVE} looking down at themselves in sudden horrified awareness, "
     f"shown from shoulders up only, "
     f"dense green foliage surrounds both figures providing complete modesty, "
     f"absolutely no nudity, no exposed private areas, "
     f"both expressions shifting from wonder to shock to shame, "
     f"camera angle from above looking down at their faces. {C}"),

    (32, "032_they_were_ashamed.jpg",
     f"{ADAM} and {EVE} with backs turned away from camera, hunched slightly in shame, "
     f"shot from behind at distance showing them from waist up, "
     f"both fully covered by natural foliage from camera angle, no nudity whatsoever, "
     f"the golden light of Eden still present but their joy completely gone. {C}"),

    (33, "033_sewed_fig_leaves.jpg",
     f"Close-up of two pairs of ancient olive-skinned hands working frantically with large broad green fig leaves, "
     f"interweaving and pinning the leaves into crude coverings, "
     f"urgency and shame in the movement, Eden garden softly in background, "
     f"the first human clothing made from desperation. {C}"),

    (34, "034_then_they_heard_it.jpg",
     f"{ADAM_FIG} and {EVE_FIG} frozen in place, heads turning with identical expressions of terror, "
     f"both looking in the same direction with wide frightened eyes, "
     f"the sound of something approaching through the garden, "
     f"dread on both their faces. {C}"),

    (35, "035_sound_of_god_walking.jpg",
     f"Ancient winding path through Eden garden at sunset, warm amber and golden light, "
     f"divine presence conveyed by radiant footsteps of light on the ancient path, "
     f"leaves gently parting as something passes through, "
     f"sacred and terrifying atmosphere, no humans. {C}"),

    (36, "036_they_hid.jpg",
     f"{ADAM_FIG} and {EVE_FIG} pressing themselves desperately against the massive trunk of an ancient tree, "
     f"both crouched in the shadows between enormous gnarled roots, "
     f"faces buried against the bark in terror, completely covered by their fig-leaf garments and surrounding foliage, "
     f"absolutely no nudity, both fully clothed in fig-leaf garments, "
     f"the divine radiant light visible approaching in the far distance behind them. {C}"),

    (37, "037_first_time_hid_from_god.jpg",
     f"Wide atmospheric shot of {ADAM_FIG} and {EVE_FIG} hidden in deep shadows at the base of ancient trees, "
     f"small figures in vast darkness, "
     f"radiant divine light visible in the far distance, "
     f"the vast gulf between creature and Creator for the first time, "
     f"devastating wide shot. {C}"),

    (38, "038_where_are_you.jpg",
     f"The Eden garden at dusk, golden light shafting between ancient trees, "
     f"the divine question hanging in still air, leaves trembling, "
     f"the most haunting question ever asked, no humans visible. {C}"),

    (39, "039_adam_i_was_afraid.jpg",
     f"{ADAM_FIG} emerging slightly from hiding behind ancient tree roots, speaking from the shadows, "
     f"his face half in shadow, expression of terror and profound guilt, "
     f"the weight of disobedience on every feature, "
     f"his voice breaking the silence of the garden. {C}"),

    (40, "040_who_told_you_naked.jpg",
     f"The divine confrontation: {ADAM_FIG} cowering in the garden, "
     f"overwhelming divine golden light filling the frame from one side, "
     f"Adam's face caught in that light, nowhere to hide, "
     f"the confrontation that will determine the fate of humanity. {C}"),

    (41, "041_woman_you_gave_me.jpg",
     f"{ADAM_FIG} pointing accusingly toward {EVE_FIG}, "
     f"Adam's arm extended in blame, Eve's face showing hurt and betrayal, "
     f"the first human accusation, the first broken relationship, "
     f"the light of Eden diminished around them. {C}"),

    (42, "042_serpent_deceived_me.jpg",
     f"{EVE_FIG}'s face — desperate and ashamed — pointing toward {SERPENT} on the ground, "
     f"Eve's dark almond eyes filled with tears, "
     f"the serpent watching impassively, "
     f"Eve's guilt written across her beautiful olive face. {C}"),

    (43, "043_god_turned_to_serpent.jpg",
     f"{SERPENT} in Eden garden, suddenly no longer confident, "
     f"its iridescent teal and gold scales catching divine light that has turned from warm to cold, "
     f"the serpent's expression changed — no longer cunning but trapped, "
     f"divine presence bearing down upon it, judgment about to fall. {C}"),

    (44, "044_cursed_above_all.jpg",
     f"{SERPENT} in the moment of its curse: "
     f"the magnificent upright crested serpent losing its regal posture, "
     f"its elegant form collapsing downward toward the earth, "
     f"scales still beautiful but now destined for the dust, "
     f"divine judgment visible in the cold light above it. {C}"),

    (45, "045_enmity_between_you.jpg",
     f"{EVE_FIG} looking down at {SERPENT} now on the ground with revulsion and fear, "
     f"the serpent looking up at her with ancient cold hatred, "
     f"the eternal enmity established between woman and serpent, "
     f"dramatic low angle: serpent below, Eve above. {C}"),

    (46, "046_greatly_increase_pain.jpg",
     f"{EVE_FIG} standing alone in the dimming garden, expression of deep sorrow and acceptance, "
     f"hands folded, tears on her olive cheeks, "
     f"the garden around her less vibrant, golden light fading to amber. {C}"),

    (47, "047_cursed_is_the_ground.jpg",
     f"{ADAM_FIG} kneeling and looking down at the earth with solemn grief, "
     f"a single sharp thorn visible in the soil before him, "
     f"the garden less vibrant, sky heavier, "
     f"the weight of consequence on his face. {C}"),

    (48, "048_sweat_of_your_brow.jpg",
     f"{ADAM_FIG} standing with open hands, gazing at his capable hands now destined for hard labor, "
     f"Eden garden softly visible behind him, "
     f"his expression carrying the weight of a new harsh reality. {C}"),

    (49, "049_dust_you_shall_return.jpg",
     f"Divine golden-white light descending to touch ancient dry earth, "
     f"close-up of glowing light meeting dry soil, dust particles rising in the divine light, "
     f"the profound truth made visual: life from dust returning to dust, "
     f"no humans, abstract and philosophical. {C}"),

    (50, "050_garments_of_skin.jpg",
     f"{ADAM_SKIN} and {EVE_SKIN} being clothed by divine light, "
     f"divine golden light surrounding them as simple animal skin garments are placed upon them, "
     f"an act of mercy within judgment, God covering their shame, "
     f"the first animal sacrifice visible in the skins they wear. {C}"),

    (51, "051_become_like_one_of_us.jpg",
     f"{ADAM_SKIN} and {EVE_SKIN} standing together in their new garments, "
     f"faces carrying the weight of knowledge they cannot unlearn, "
     f"no longer innocent, "
     f"the garden still around them but their place in it forever changed. {C}"),

    (52, "052_banished_from_eden.jpg",
     f"Wide cinematic shot: {ADAM_SKIN} and {EVE_SKIN} walking away from the garden's entrance, "
     f"backs to camera, moving toward a darker harsher landscape beyond the gate, "
     f"the garden's golden light fading behind them, "
     f"the world outside dry and brown by comparison, "
     f"the most tragic exit in human history. {C}"),

    (53, "053_adam_looked_back.jpg",
     f"Profile portrait of {ADAM_SKIN} turning to look back at Eden over his shoulder, "
     f"Eden visible behind him in all its golden beauty, now impossibly distant, "
     f"his dark brown eyes filled with loss and regret, "
     f"the last look at paradise, devastating and beautiful. {C}"),

    (54, "054_cherubim_and_sword.jpg",
     f"Two massive angelic beings of blinding white light standing at the garden's ancient stone gate, "
     f"between them a great sword of actual roaring flames turning in every direction, "
     f"the gate to Eden sealed forever by terrifying divine guardians, "
     f"the small retreating figures of {ADAM_SKIN} and {EVE_SKIN} visible as tiny silhouettes in the distance. {C}"),

    (55, "055_they_would_never_return.jpg",
     f"Final wide cinematic shot: {ADAM_SKIN} and {EVE_SKIN} walking into the vast harsh wilderness, "
     f"small figures in an empty landscape, "
     f"behind them the flaming sword blazing at the garden gate, "
     f"ahead only wilderness and uncertainty, "
     f"the golden light of Eden fading behind them forever. {C}"),
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


def _imagen_predict(model_id, prompt, key, timeout=90):
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:predict?key={key}",
        json={
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9",
                "safetyFilterLevel": "block_only_high",
                "personGeneration": "allow_adult",
            },
        },
        timeout=timeout,
    )
    if resp.status_code == 429:
        raise RuntimeError("RATE_LIMIT")
    if resp.status_code != 200:
        raise RuntimeError(resp.json().get("error", {}).get("message", resp.text[:200]))
    preds = resp.json().get("predictions", [])
    if not preds:
        raise RuntimeError("EMPTY")
    return base64.b64decode(preds[0]["bytesBase64Encoded"])


def _nano_banana(prompt, key, timeout=90):
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={key}",
        json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["image"]},
        },
        timeout=timeout,
    )
    if resp.status_code == 429:
        raise RuntimeError("RATE_LIMIT")
    if resp.status_code != 200:
        raise RuntimeError(resp.json().get("error", {}).get("message", resp.text[:200]))
    parts = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        if "inlineData" in p:
            return base64.b64decode(p["inlineData"]["data"])
    raise RuntimeError("EMPTY")


def generate(prompt, out_path, key):
    """Try Imagen 4 Ultra first, fall back to Nano Banana."""
    for attempt in range(5):
        try:
            data = _imagen_predict("imagen-4.0-ultra-generate-001", prompt, key)
            out_path.write_bytes(data)
            return "ultra"
        except RuntimeError as e:
            err = str(e)
            if "RATE_LIMIT" in err:
                print("      Ultra rate limited — falling back to Nano Banana")
                break
            elif "EMPTY" in err:
                time.sleep(8)
            else:
                print(f"      Ultra error: {err[:100]}, retrying...")
                time.sleep(8)

    for attempt in range(5):
        try:
            data = _nano_banana(prompt, key)
            out_path.write_bytes(data)
            return "nano"
        except RuntimeError as e:
            err = str(e)
            wait = min(60, 15 * (attempt + 1))
            print(f"      Nano Banana attempt {attempt + 1} failed ({err[:60]}), waiting {wait}s...")
            time.sleep(wait)

    raise RuntimeError("All models failed after retries")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenes", help="Comma-separated scene numbers to fix, e.g. 2,11,15,36")
    parser.add_argument("--start",  type=int, default=1,  help="Start scene number")
    parser.add_argument("--end",    type=int, default=55, help="End scene number")
    parser.add_argument("--force",  action="store_true",  help="Overwrite existing images")
    parser.add_argument("--dry-run", action="store_true", help="Print prompts, no generation")
    args = parser.parse_args()

    if args.scenes:
        target = set(int(x.strip()) for x in args.scenes.split(","))
    else:
        target = set(range(args.start, args.end + 1))

    env = load_env()
    key = env.get("GOOGLE_AI_STUDIO_KEY", "")
    if not key and not args.dry_run:
        sys.exit("GOOGLE_AI_STUDIO_KEY not in .env")

    scenes_to_run = [(n, fn, prompt) for n, fn, prompt in SCENES if n in target]
    print(f"\nFix Chapter 2 images — {len(scenes_to_run)} scenes targeted\n")

    for scene_num, filename, prompt in scenes_to_run:
        out_path = OUT_DIR / filename
        exists = out_path.exists()

        if args.dry_run:
            print(f"[{scene_num:03d}] {filename}")
            print(f"       {prompt[:120]}...\n")
            continue

        if exists and not args.force and args.scenes is None:
            print(f"[{scene_num:03d}] {filename} — exists, skipping (use --force to overwrite)")
            continue

        if exists:
            out_path.unlink()
            print(f"[{scene_num:03d}] {filename} — regenerating...")
        else:
            print(f"[{scene_num:03d}] {filename} — generating...")

        for attempt in range(3):
            try:
                model = generate(prompt, out_path, key)
                size_kb = out_path.stat().st_size // 1024
                print(f"       ✓ Saved ({size_kb} KB) [{model}]\n")
                break
            except Exception as e:
                print(f"       ✗ Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(10)
        else:
            print(f"       ✗ All attempts failed for scene {scene_num}\n")

        time.sleep(15)

    done = sum(1 for _, fn, _ in SCENES if (OUT_DIR / fn).exists())
    print(f"\nDone. {done}/{len(SCENES)} images in {OUT_DIR}/")
    print("\nNext: re-render clips with:  python gen_ch02_documentary.py --skip-audio")


if __name__ == "__main__":
    main()
