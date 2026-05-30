"""
Ultra-detailed story image generator for:
  - Chapter 2: The Fall (scenes 1-55)

Each scene gets a hand-crafted, ultra-specific prompt ensuring perfect visual-to-narration alignment.
Images saved to: project/stories/ch02_the_fall/

Usage:
    python gen_ch02_the_fall.py                     # full run (Google Imagen 4)
    python gen_ch02_the_fall.py --start 10          # resume from scene 10
    python gen_ch02_the_fall.py --dry-run           # show prompts, no generation
"""

import os, sys, time, base64, argparse, requests
from pathlib import Path

# ── Output dir ─────────────────────────────────────────────────────────────────
OUT_DIR = Path("project/stories/ch02_the_fall")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Base style suffix ──────────────────────────────────────────────────────────
CINEMATIC = (
    "Ultra photorealistic, 8K cinema camera, IMAX cinematic quality, "
    "dramatic lighting, no text overlays, no watermarks, no subtitles, "
    "film grain, anamorphic lens flare, movie still frame"
)

# ── Character descriptors (used consistently across all scenes) ────────────────
ADAM = (
    "Adam: athletic Middle Eastern man, warm olive tan skin, dark wavy black hair, "
    "strong Levantine features, prominent nose, dark brown eyes, early 30s, "
    "no clothing, dignified and noble bearing"
)
EVE = (
    "Eve: beautiful Middle Eastern woman, warm olive tan skin, long dark wavy black hair, "
    "almond-shaped dark brown eyes, strong Levantine features, early 20s, "
    "no clothing, ethereally beautiful and graceful"
)
EDEN = (
    "lush ancient Eden garden, towering trees with golden light filtering through canopy, "
    "exotic tropical flowers, crystal clear rivers, vibrant green paradise"
)

# ═══════════════════════════════════════════════════════════════════════════════
# SCENE DEFINITIONS
# Each entry: (scene_number, filename, narration, prompt)
# ═══════════════════════════════════════════════════════════════════════════════

SCENES = [

    (1, "001_the_fall_title.jpg",
     "The Fall.",
     "Ancient stone tablet partially buried in Eden garden soil, carved letters glowing faint amber, "
     "fallen fruit nearby on lush green grass, dramatic golden light through ancient trees, "
     "a shadow beginning to creep across paradise. " + CINEMATIC),

    (2, "002_they_had_everything.jpg",
     "They had everything.",
     "Wide establishing shot of Adam and Eve standing together at the edge of an endless Eden paradise — "
     + ADAM + ", " + EVE + " — both gazing out over rivers of crystal water, "
     "towering fruit-laden trees stretching to the horizon, golden divine light bathing everything, "
     "absolute paradise in every direction, cinematic wide shot. " + CINEMATIC),

    (3, "003_garden_without_end.jpg",
     "A garden without end,",
     "Breathtaking aerial view of the Garden of Eden stretching to every horizon — "
     "rivers branching in four directions through lush green paradise, "
     "mountains of fruit trees, exotic flowers in full bloom, "
     "golden afternoon light, absolute perfection, no sign of any civilization. " + CINEMATIC),

    (4, "004_rivers_of_clear_water.jpg",
     "rivers of clear water,",
     "Crystal clear river in Eden flowing over smooth ancient stones, "
     "water so transparent every pebble visible beneath, "
     "vibrant green ferns and tropical flowers lining both banks, "
     "golden light sparkling on the water surface, paradise atmosphere. " + CINEMATIC),

    (5, "005_fruit_heavy_on_branches.jpg",
     "fruit heavy on every branch,",
     "Close-up of ancient fruit tree branches impossibly heavy with ripe golden fruit, "
     "pomegranates, figs, grapes, dates all clustered together in divine abundance, "
     "warm amber light illuminating the fruit from behind, "
     "Eden garden visible softly in the background. " + CINEMATIC),

    (6, "006_animals_that_came_when_called.jpg",
     "animals that came when called,",
     "Adam standing in Eden surrounded by animals with no fear — "
     + ADAM + " — a lion resting at his feet, deer beside him, colorful birds perched on his outstretched arm, "
     "a lamb in the foreground, total peace between man and beast, golden Eden light. " + CINEMATIC),

    (7, "007_god_walked_cool_of_day.jpg",
     "and a God who walked with them in the cool of the day.",
     "Long winding path through Eden garden at golden hour, "
     "divine presence suggested by radiant light between the trees, "
     "two sets of footprints in soft earth alongside a third luminous path, "
     "warm amber and gold light filtering through ancient canopy, "
     "sacred and peaceful atmosphere. " + CINEMATIC),

    (8, "008_one_thing_not_to_touch.jpg",
     "But there was one thing in the garden they had been told not to touch.",
     "The forbidden tree standing alone in a clearing at the heart of Eden — "
     "ancient massive tree with dark twisted bark, beautiful dark fruits hanging from its branches, "
     "a subtle aura of mysterious golden-red light around it, "
     "other trees keeping a slight distance, atmospheric tension. " + CINEMATIC),

    (9, "009_one_tree.jpg",
     "One tree.",
     "Extreme close-up portrait of the forbidden tree trunk — "
     "ancient deeply gnarled dark bark with subtle glow emanating from within, "
     "fruit hanging tantalizingly close, "
     "mysterious light catching each piece of fruit, "
     "ominous beautiful atmosphere, sacred and dangerous. " + CINEMATIC),

    (10, "010_that_was_enough.jpg",
     "And that was enough.",
     "Wide shot of the vast Eden garden with the single forbidden tree visible at its center, "
     "small and distant yet somehow drawing the eye, "
     "all of paradise spread around it but the eye cannot look away from that one tree, "
     "golden light across the garden, dramatic composition. " + CINEMATIC),

    (11, "011_serpent_most_cunning.jpg",
     "The serpent was the most cunning of all the creatures God had made.",
     "A magnificent ancient serpent — not crawling but upright and regal, "
     "coiled elegantly around a branch in Eden, "
     "iridescent scales catching golden light, unnaturally intelligent eyes, "
     "beautiful and dangerous, unlike any other creature in the garden, "
     "close-up portrait shot, mysterious atmosphere. " + CINEMATIC),

    (12, "012_serpent_came_to_eve.jpg",
     "He came to Eve, not with a threat, but with a question.",
     "Eve alone near the forbidden tree, "
     + EVE + ", the serpent descending sinuously from a branch toward her, "
     "its intelligent eyes level with hers, "
     "golden afternoon light in the background, "
     "close and intimate scene, tension beginning to build. " + CINEMATIC),

    (13, "013_did_god_really_say.jpg",
     "Did God really say you must not eat from any tree in the garden?",
     "Extreme close-up of the serpent's face, inches from Eve's, "
     "iridescent scales, deep knowing eyes, "
     "forked tongue barely visible, the question hanging in the air, "
     "Eve's dark hair visible at the edge of frame, "
     "tension and temptation, dramatic lighting. " + CINEMATIC),

    (14, "014_eve_answered.jpg",
     "Eve answered carefully.",
     "Eve standing thoughtfully before the serpent, "
     + EVE + ", her expression composed but uncertain, "
     "she gestures slightly toward the garden around her, "
     "the serpent listening intently, "
     "warm light on her olive skin, the garden abundant behind her. " + CINEMATIC),

    (15, "015_may_eat_from_trees.jpg",
     "We may eat from the trees of the garden,",
     "Eve gesturing across the vast Eden garden filled with fruit trees — "
     + EVE + " — arm extended toward the abundance of paradise, "
     "countless trees heavy with fruit in every direction, "
     "the generosity of creation visible in every direction. " + CINEMATIC),

    (16, "016_not_from_center_tree.jpg",
     "but not from the tree in the center. God said, do not eat from it, or you will die.",
     "Eve turning back toward the forbidden tree, pointing at it with a solemn expression — "
     + EVE + " — the tree visible behind her with its ominous glow, "
     "her expression carrying the weight of God's warning, "
     "the serpent watching her carefully, studying her reaction. " + CINEMATIC),

    (17, "017_serpent_smiled.jpg",
     "And the serpent smiled.",
     "Close-up of the serpent's face showing a chilling expression of cunning satisfaction — "
     "scales gleaming, eyes lit with knowing intelligence, "
     "the ghost of a smile on its features, "
     "this is the moment the trap is sprung, "
     "dramatic and ominous close-up. " + CINEMATIC),

    (18, "018_you_will_not_die.jpg",
     "You will not die, he said.",
     "The serpent coiled gracefully before Eve, speaking with absolute confidence — "
     + EVE + " listening, her expression shifting from caution toward curiosity, "
     "the forbidden tree glowing behind them both, "
     "the serpent's certainty filling the air between them. " + CINEMATIC),

    (19, "019_eyes_will_be_opened.jpg",
     "God knows that when you eat from it, your eyes will be opened.",
     "Extreme close-up of the serpent's penetrating eyes, unnaturally wise and knowing, "
     "reflecting the image of the forbidden tree in their depths, "
     "ancient intelligence and deception visible in their gleam, "
     "the most dangerous moment in human history. " + CINEMATIC),

    (20, "020_like_god_knowing.jpg",
     "And you will be like God, knowing good and evil.",
     "The serpent gesturing upward with regal confidence, "
     "Eve looking up, intrigued, her expression caught between wonder and uncertainty, "
     + EVE + ", the forbidden tree framing the moment, "
     "light shifting around them, "
     "the greatest lie ever told hanging in the air. " + CINEMATIC),

    (21, "021_eve_looked_at_tree.jpg",
     "Eve looked at the tree.",
     "Eve's profile as she gazes at the forbidden tree, "
     + EVE + " — her dark eyes reflecting the tree's glow, "
     "expression of deep longing and contemplation, "
     "the tree filling most of the frame, "
     "golden-red light on her face, the moment before everything changes. " + CINEMATIC),

    (22, "022_fruit_good_for_food.jpg",
     "She saw that its fruit was good for food.",
     "Close-up of the forbidden fruit hanging tantalizingly close to Eve's face — "
     "perfectly formed dark fruit with a subtle inner glow, "
     "Eve's lips parted slightly, her eyes fixed on it, "
     + EVE + " in soft focus, "
     "the fruit impossibly beautiful and appealing. " + CINEMATIC),

    (23, "023_beautiful_to_the_eye.jpg",
     "That it was beautiful to the eye.",
     "The forbidden fruit in extreme close-up — "
     "skin rich and dark, catching golden light, "
     "visually perfect, more beautiful than any other fruit in the garden, "
     "Eve's dark eyes reflecting it, her hand moving slightly toward it. " + CINEMATIC),

    (24, "024_desirable_for_wisdom.jpg",
     "That it was desirable for making one wise.",
     "Eve's face very close to the fruit, eyes wide with yearning — "
     + EVE + " — desire and intellect warring on her face, "
     "the serpent watching from the shadows of the branch above, "
     "this is the moment of decision, "
     "warm dramatic light on her features. " + CINEMATIC),

    (25, "025_she_reached_out.jpg",
     "And she reached out and took it.",
     "Eve's hand reaching out and closing around the forbidden fruit — "
     + EVE + " — the moment of taking it, fingers wrapping around the beautiful dark fruit, "
     "the tree's light pulsing at the moment of contact, "
     "dramatic close-up of hand and fruit, "
     "the most consequential moment in human history. " + CINEMATIC),

    (26, "026_she_ate.jpg",
     "She ate.",
     "Eve biting into the forbidden fruit, eyes closing — "
     + EVE + " — juice running over her lips, "
     "an expression crossing her face that is both ecstasy and something darker, "
     "the garden's light subtly changing around her, "
     "close-up portrait, devastating beauty. " + CINEMATIC),

    (27, "027_gave_some_to_adam.jpg",
     "And she gave some to Adam, who was with her.",
     "Eve turning to Adam with the bitten fruit extended toward him — "
     + EVE + " and " + ADAM + " — both in the shadow of the forbidden tree, "
     "Eve's expression urgent and pleading, the fruit in her outstretched hand, "
     "Adam's face showing surprise and hesitation. " + CINEMATIC),

    (28, "028_and_he_ate.jpg",
     "And he ate.",
     "Adam taking the fruit from Eve and eating — "
     + ADAM + " — the moment of his bite, "
     "his eyes closing as he eats, "
     "expression changing from hesitation to something irrevocable, "
     "the garden light visibly shifting around them both, "
     "dramatic close-up. " + CINEMATIC),

    (29, "029_in_that_instant.jpg",
     "In that instant, everything changed.",
     "Wide shot of Adam and Eve at the forbidden tree, the moment after — "
     + ADAM + " and " + EVE + " — "
     "the garden light dramatically different, shadows deeper, "
     "the golden paradise somehow diminished, "
     "the sky subtly darker, the beauty slightly faded, "
     "cinematic wide shot of the before-and-after moment. " + CINEMATIC),

    (30, "030_eyes_were_opened.jpg",
     "Their eyes were opened.",
     "Extreme close-up of Adam and Eve's eyes simultaneously — split composition — "
     "both pairs of eyes wide open, dark brown irises suddenly aware, "
     "something fundamentally changed in their gaze, "
     "the light of Eden reflected in their eyes but also something new: knowledge. " + CINEMATIC),

    (31, "031_knew_they_were_naked.jpg",
     "And for the first time, they knew they were naked.",
     "Adam and Eve looking down at themselves in sudden awareness — "
     + ADAM + " and " + EVE + " — "
     "both their expressions shifting from wonder to shock to shame, "
     "hands moving instinctively to cover themselves, "
     "the first moment of human shame, devastating and beautiful. " + CINEMATIC),

    (32, "032_they_were_ashamed.jpg",
     "And they were ashamed.",
     "Adam and Eve turned away from each other and from the camera — "
     + ADAM + " and " + EVE + " — "
     "hunched slightly, faces turned down, "
     "the golden light of Eden still present but their joy in it completely gone, "
     "shame visible in every line of their bodies. " + CINEMATIC),

    (33, "033_sewed_fig_leaves.jpg",
     "They sewed fig leaves together and covered themselves.",
     "Close-up of hands working frantically with large fig leaves — "
     "interweaving broad green leaves into crude coverings, "
     "urgency and shame in the movement, "
     "Eden garden visible softly behind, "
     "the first human clothing, woven from desperation. " + CINEMATIC),

    (34, "034_then_they_heard_it.jpg",
     "Then they heard it.",
     "Adam and Eve frozen in place, heads turning with identical expressions of terror — "
     + ADAM + " and " + EVE + " — "
     "both looking in the same direction, "
     "fig leaf coverings hastily worn, "
     "the sound of something approaching through the garden, "
     "dread on both their faces. " + CINEMATIC),

    (35, "035_sound_of_god_walking.jpg",
     "The sound of God walking in the garden in the cool of the evening.",
     "A path through the Eden garden at sunset, golden and amber light — "
     "divine presence conveyed by radiant footsteps of light on the path, "
     "leaves gently parting as something passes, "
     "the sound of presence without a visible form, "
     "sacred and terrifying atmosphere. " + CINEMATIC),

    (36, "036_they_hid.jpg",
     "And they hid.",
     "Adam and Eve pressing themselves against the trunk of a large tree, hiding — "
     + ADAM + " and " + EVE + " — "
     "both crouched in the shadows between gnarled roots, "
     "fig leaves covering them, "
     "faces pressed against the bark in terror, "
     "the divine light visible approaching in the distance behind them. " + CINEMATIC),

    (37, "037_first_time_hid_from_god.jpg",
     "For the first time in their lives, they hid from God.",
     "Wide shot of Adam and Eve hidden in shadows at the base of trees — "
     + ADAM + " and " + EVE + " — "
     "small figures against the vast darkness of the garden, "
     "the radiant divine light visible in the distance, "
     "the vast distance between creature and Creator for the first time, "
     "devastating cinematic composition. " + CINEMATIC),

    (38, "038_where_are_you.jpg",
     "Where are you? God called.",
     "The Eden garden at dusk, golden light shafting between trees — "
     "the question hanging in the still air, "
     "leaves trembling slightly, "
     "divine presence filling the frame without being visible, "
     "the most haunting question ever asked, "
     "atmospheric and sacred. " + CINEMATIC),

    (39, "039_adam_i_was_afraid.jpg",
     "I heard you in the garden, Adam said. And I was afraid. And I hid.",
     "Adam emerging slightly from hiding, speaking from the shadows — "
     + ADAM + " — fig leaves covering him, "
     "his face half in shadow, expression of terror and guilt, "
     "the weight of disobedience on every feature, "
     "his voice breaking the silence of the garden. " + CINEMATIC),

    (40, "040_who_told_you_naked.jpg",
     "Who told you that you were naked? Have you eaten from the tree?",
     "The question hanging over Adam cowering in the garden — "
     + ADAM + " — fig leaves around him, "
     "the divine light filling the frame from one side, "
     "Adam's face caught in that light, nowhere to hide, "
     "the confrontation that will determine the fate of humanity. " + CINEMATIC),

    (41, "041_woman_you_gave_me.jpg",
     "The woman you put here with me — she gave me some fruit from the tree.",
     "Adam pointing toward Eve, his expression guilty and desperate — "
     + ADAM + " and " + EVE + " both visible — "
     "Adam's arm extended accusingly, Eve's face showing hurt and betrayal, "
     "the first human blame, the first broken relationship, "
     "the light of Eden diminished around them. " + CINEMATIC),

    (42, "042_serpent_deceived_me.jpg",
     "The serpent deceived me, Eve said.",
     "Eve's face — desperate, ashamed, pointing toward the serpent — "
     + EVE + " — her dark eyes filled with tears, "
     "the serpent visible coiled on a branch nearby, watching impassively, "
     "Eve's guilt and shame written across her beautiful face, "
     "the garden dark around her. " + CINEMATIC),

    (43, "043_god_turned_to_serpent.jpg",
     "And God turned to the serpent.",
     "The serpent on its branch, suddenly no longer confident — "
     "iridescent scales catching divine light that has turned from warm to cold, "
     "the serpent's expression changed, no longer cunning but trapped, "
     "the divine presence bearing down upon it, "
     "judgment about to fall, dramatic atmosphere. " + CINEMATIC),

    (44, "044_cursed_above_all.jpg",
     "Cursed are you above all livestock. You will crawl on your belly all the days of your life.",
     "The serpent in the moment of its curse — "
     "the magnificent upright serpent losing its posture, "
     "its elegant form collapsing downward toward the earth, "
     "scales still beautiful but now destined for the dust, "
     "divine judgment visible in the light, "
     "the moment the serpent became what it is today. " + CINEMATIC),

    (45, "045_enmity_between_you.jpg",
     "And I will put enmity between you and the woman, between your offspring and hers.",
     "Eve looking down at the serpent now on the ground with an expression of revulsion — "
     + EVE + " — the serpent looking up at her with ancient hatred, "
     "the divide between woman and serpent established for all time, "
     "dramatic low angle showing the serpent below and Eve above, "
     "the eternal enmity beginning. " + CINEMATIC),

    (46, "046_greatly_increase_pain.jpg",
     "To Eve, God said: I will greatly increase your pain in childbearing.",
     "Eve receiving her judgment — "
     + EVE + " — her expression one of sorrow and acceptance, "
     "hands at her side, the weight of the curse beginning to fall, "
     "the garden around her less vibrant than before, "
     "divine light now carrying judgment alongside grace. " + CINEMATIC),

    (47, "047_cursed_is_the_ground.jpg",
     "To Adam: Cursed is the ground because of you. Through painful toil you will eat of it.",
     "Adam standing in what was once paradise, now seeing thorns and thistles beginning to appear — "
     + ADAM + " — looking down at the ground as the earth itself changes, "
     "the first thorn visible pushing through perfect soil, "
     "the curse of labor beginning, "
     "the garden's perfection cracking. " + CINEMATIC),

    (48, "048_sweat_of_your_brow.jpg",
     "By the sweat of your brow you will eat your food,",
     "Adam with hands rough and open, looking at them as if seeing them differently — "
     + ADAM + " — these hands that once simply reached for fruit now destined for labor, "
     "Eden garden visible but somehow further away, "
     "the weight of toil beginning to fall on his broad shoulders. " + CINEMATIC),

    (49, "049_dust_you_shall_return.jpg",
     "For dust you are, and to dust you shall return.",
     "God's hand (or divine light) reaching toward the earth — "
     "close-up of a hand of light touching soil, "
     "the profound theological truth made visual, "
     "dust and light and the space between, "
     "the mortality of man made plain for the first time. " + CINEMATIC),

    (50, "050_garments_of_skin.jpg",
     "God made garments of skin for Adam and Eve and clothed them.",
     "Adam and Eve being clothed in simple animal skins — "
     + ADAM + " and " + EVE + " — "
     "divine hands or divine light surrounding them as the garments are placed, "
     "an act of mercy within judgment, "
     "God clothing the shame he did not cause but chose to cover, "
     "the first sacrifice visible in the skins they wear. " + CINEMATIC),

    (51, "051_become_like_one_of_us.jpg",
     "The man has now become like one of us, knowing good and evil.",
     "Adam and Eve standing together in their new garments of skin — "
     + ADAM + " and " + EVE + " — "
     "faces carrying the weight of knowledge they cannot return, "
     "no longer innocent, no longer free, "
     "the garden still around them but their place in it forever changed. " + CINEMATIC),

    (52, "052_banished_from_eden.jpg",
     "So God banished them from the Garden of Eden.",
     "Wide shot of Adam and Eve walking away from the garden's entrance — "
     + ADAM + " and " + EVE + " — "
     "their backs to us, moving toward a darker, harsher landscape beyond the garden gate, "
     "the garden's golden light behind them fading, "
     "the world outside dry and brown by comparison, "
     "the most tragic exit in human history. " + CINEMATIC),

    (53, "053_adam_looked_back.jpg",
     "Adam looked back at the garden for the last time.",
     "Adam turning to look back at Eden over his shoulder — "
     + ADAM + " — profile shot, "
     "Eden visible behind him in all its golden beauty, now impossibly distant, "
     "his eyes filled with loss and regret, "
     "the last look at paradise, "
     "devastating and beautiful. " + CINEMATIC),

    (54, "054_cherubim_and_sword.jpg",
     "Behind them, God placed cherubim, and a flaming sword flashing back and forth.",
     "Two massive angelic figures standing at the garden's entrance with a flaming sword — "
     "enormous powerful beings of light flanking the gate, "
     "between them a sword of actual fire turning in every direction, "
     "the gate to Eden sealed forever, "
     "terrifying divine guardians, "
     "Adam and Eve's small retreating figures visible in the distance. " + CINEMATIC),

    (55, "055_they_would_never_return.jpg",
     "The gate was closed. They would never return.",
     "Final wide shot: Adam and Eve walking into the harsh world beyond Eden, "
     + ADAM + " and " + EVE + " — "
     "small figures in a vast empty landscape, "
     "behind them the flaming sword visible at the garden gate, "
     "ahead of them only wilderness and uncertainty, "
     "the golden light of Eden a memory behind them, "
     "the first chapter of human suffering beginning. " + CINEMATIC),

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
    """Call an Imagen predict-endpoint model. Returns raw bytes or raises."""
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


def _nano_banana_generate(prompt, key, timeout=90):
    """Call Nano Banana (gemini-2.5-flash-image) via generateContent. Returns raw bytes or raises."""
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


def generate_google(prompt, out_path, key):
    """Try Imagen 4 Ultra first (best quality, 30 RPD), fall back to Nano Banana (500 RPD)."""
    for attempt in range(5):
        try:
            data = _imagen_predict("imagen-4.0-ultra-generate-001", prompt, key)
            out_path.write_bytes(data)
            return
        except RuntimeError as e:
            err = str(e)
            if "RATE_LIMIT" in err:
                print(f"      Ultra rate limited — falling back to Nano Banana")
                break
            elif "EMPTY" in err:
                time.sleep(8)
                continue
            else:
                print(f"      Ultra error: {err[:100]}, retrying...")
                time.sleep(8)
                continue

    # Fallback: Nano Banana (gemini-2.5-flash-image)
    for attempt in range(5):
        try:
            data = _nano_banana_generate(prompt, key)
            out_path.write_bytes(data)
            print(f"      (used Nano Banana fallback)")
            return
        except RuntimeError as e:
            err = str(e)
            wait = min(60, 15 * (attempt + 1))
            print(f"      Nano Banana attempt {attempt+1} failed ({err[:60]}), waiting {wait}s...")
            time.sleep(wait)

    raise RuntimeError("All models failed after retries")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start",   type=int, default=1,  help="Resume from scene N")
    parser.add_argument("--end",     type=int, default=55, help="Stop at scene N")
    parser.add_argument("--dry-run", action="store_true",  help="Print prompts only")
    args = parser.parse_args()

    env = load_env()
    key = env.get("GOOGLE_AI_STUDIO_KEY", "")
    if not key and not args.dry_run:
        sys.exit("GOOGLE_AI_STUDIO_KEY not in .env")

    scenes = [s for s in SCENES if args.start <= s[0] <= args.end]
    print(f"\nChapter 2: The Fall — generating {len(scenes)} images")
    print(f"Output dir: {OUT_DIR}\n")

    for scene_num, filename, narration, prompt in scenes:
        out_path = OUT_DIR / filename
        print(f"[{scene_num:03d}] {narration[:60]}{'…' if len(narration)>60 else ''}")

        if args.dry_run:
            print(f"       PROMPT: {prompt[:120]}...\n")
            continue

        if out_path.exists():
            print(f"       ✓ Exists, skipping\n")
            continue

        for attempt in range(3):
            try:
                generate_google(prompt, out_path, key)
                size_kb = out_path.stat().st_size // 1024
                print(f"       ✓ Saved ({size_kb} KB)\n")
                break
            except Exception as e:
                print(f"       ✗ Attempt {attempt+1} failed: {e}")
                if attempt < 2:
                    time.sleep(10)
        else:
            print(f"       ✗ All attempts failed for scene {scene_num}\n")

        # Rate limiting — Imagen 4 Standard: 70 RPD, 10 RPM
        time.sleep(15)

    done = sum(1 for _, fn, _, _ in SCENES if (OUT_DIR / fn).exists())
    print(f"\nDone. {done}/{len(SCENES)} images in {OUT_DIR}/")


if __name__ == "__main__":
    main()
