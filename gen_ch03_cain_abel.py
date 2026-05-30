#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 3 — Cain and Abel (Scenes 1-55)

Generates ultra-cinematic still images for Chapter 3.
Output: project/stories/ch03_cain_abel/

Usage:
    python gen_ch03_cain_abel.py              # full run
    python gen_ch03_cain_abel.py --start 10   # resume from scene 10
    python gen_ch03_cain_abel.py --dry-run    # print prompts only
"""

import os, sys, time, base64, argparse, requests
from pathlib import Path

OUT_DIR = Path("project/stories/ch03_cain_abel")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Character descriptors ──────────────────────────────────────────────────────

# Cain — firstborn son of Adam and Eve, farmer, brooding
CAIN = (
    "Cain: ancient Middle Eastern young man, warm olive tan skin, dark hair, strong jaw, "
    "intense brooding dark eyes, mid-20s, ordinary build, not idealized, "
    "wearing rough ancient farmer's linen tunic, barefoot, ancient biblical era"
)

# Abel — second son, shepherd, gentle
ABEL = (
    "Abel: ancient Middle Eastern young man, warm olive tan skin, dark wavy hair, "
    "gentle kind face, warm dark eyes, early 20s, ordinary build, not idealized, "
    "wearing simple ancient shepherd's tunic and rough woven cloak, barefoot, ancient biblical era"
)

# Adam — now older, post-Eden, weathered by labor
ADAM = (
    "Adam: ancient Middle Eastern man in his 40s, warm olive tan skin, dark hair with streaks of gray, "
    "prominent nose, weathered tired face, dark eyes, ordinary build, "
    "wearing rough woven ancient garments, ancient biblical era"
)

# Eve — now older, post-Eden
EVE = (
    "Eve: ancient Middle Eastern woman in her 40s, warm olive tan skin, long dark hair, "
    "almond-shaped dark brown eyes, Levantine features, ordinary natural appearance, "
    "wearing rough woven ancient garments, ancient biblical era"
)

# Settings
OUTSIDE_EDEN = (
    "harsh rocky ancient landscape outside the Garden of Eden, "
    "dry brown rocky ground with thorns and thistles, sparse vegetation, "
    "distant mountains, dusty ancient Middle Eastern terrain"
)

PASTURE = (
    "ancient rolling pasture land, gentle green hills, "
    "flock of sheep grazing peacefully, golden afternoon light, "
    "ancient Middle Eastern landscape, open sky"
)

FARM_FIELD = (
    "ancient dry farming field, tilled rocky earth, "
    "rows of ancient grain crops growing under harsh sun, "
    "ancient Middle Eastern landscape, harsh and difficult terrain"
)

# Cinematic style + anti-hallucination
C = (
    "ultra photorealistic, 8K cinema camera, IMAX cinematic quality, dramatic lighting, "
    "no text overlays no watermarks no subtitles, film grain, anamorphic lens flare, movie still frame, "
    "ancient biblical setting only, no modern elements no motorcycles no cars no modern clothing "
    "no modern buildings, strictly ancient biblical era"
)

# ── Scene definitions: (scene_num, filename, narration, prompt) ────────────────
SCENES = [

    (1, "001_cain_abel_title.jpg",
     "Cain and Abel.",
     f"Two rough-hewn ancient stone tools — a farming hoe and a shepherd's crook — "
     f"lying side by side on ancient rocky earth, golden morning light casting long shadows, "
     f"no humans visible, cinematic still life. {C}"),

    (2, "002_outside_eden_hard.jpg",
     "Outside the garden, life was hard.",
     f"Wide cinematic shot of {ADAM} and {EVE} standing in the harsh landscape, "
     f"the distant silhouette of the lost Garden barely visible on the horizon behind them, "
     f"the world before them dry and difficult, {OUTSIDE_EDEN}. {C}"),

    (3, "003_ground_demands_everything.jpg",
     "The ground that had once given freely now demanded everything.",
     f"Close-up of cracked dry ancient earth, thorns and thistles growing from it, "
     f"a single struggling grain shoot pushing through the hard soil, "
     f"harsh overhead sunlight, {OUTSIDE_EDEN}. {C}"),

    (4, "004_adam_works_soil.jpg",
     "Adam worked the soil with sweat and pain, just as God had said.",
     f"{ADAM} bent over in a rocky field, working the hard ground with a primitive wooden hoe, "
     f"sweat visible on his weathered face, the labor heavy and relentless, "
     f"harsh sun overhead, {FARM_FIELD}. {C}"),

    (5, "005_eve_bears_children.jpg",
     "Eve bore children into this new and broken world.",
     f"Portrait of {EVE} holding a swaddled newborn infant close to her chest, "
     f"her expression a mixture of wonder, love, and exhaustion, "
     f"soft warm firelight inside a simple ancient stone dwelling, intimate and tender. {C}"),

    (6, "006_first_son_named_cain.jpg",
     "Her first son, she named Cain.",
     f"Close-up of {EVE}'s face as she looks down at her newborn son with profound love, "
     f"the baby's small dark-haired head cradled in her arms, "
     f"soft golden firelight, the very first moment of motherhood in the world. {C}"),

    (7, "007_with_help_of_lord.jpg",
     "With the help of the Lord, she said. I have brought forth a man.",
     f"{EVE} looking upward with an expression of reverence and gratitude, "
     f"newborn baby in her arms, "
     f"divine golden light filtering through the opening of an ancient stone dwelling, "
     f"a moment of sacred thanksgiving. {C}"),

    (8, "008_then_bore_abel.jpg",
     "Then she bore another son.",
     f"Wide gentle shot of {EVE} and {ADAM} sitting together outside their simple ancient dwelling, "
     f"Eve holding a second infant, Adam beside her with his hand on her shoulder, "
     f"a toddler Cain playing in the dirt nearby, "
     f"warm afternoon light, the family complete for a moment. {C}"),

    (9, "009_named_him_abel.jpg",
     "She named him Abel.",
     f"Close-up of a tiny newborn's face — {ABEL} as an infant — eyes barely open, "
     f"peaceful and innocent, wrapped in rough ancient cloth, "
     f"Eve's warm olive-skinned hand gently touching his cheek, "
     f"soft warm light. {C}"),

    (10, "010_two_brothers_two_paths.jpg",
     "Two brothers. Two paths.",
     f"Wide cinematic shot of two young men standing apart in the landscape — "
     f"{CAIN} on the left standing in a tilled field holding a farming tool, "
     f"{ABEL} on the right standing on a hillside with sheep behind him, "
     f"each in their own world, dramatic sky between them. {C}"),

    (11, "011_abel_became_shepherd.jpg",
     "Abel became a shepherd, tending his flocks under the open sky.",
     f"{ABEL} standing peacefully on a hillside among his flock of sheep, "
     f"his shepherd's crook in hand, gazing out over the land, "
     f"golden afternoon light, {PASTURE}. {C}"),

    (12, "012_cain_became_farmer.jpg",
     "Cain became a farmer, working the cursed earth with his hands.",
     f"{CAIN} in his field, bent over the hard rocky ground working with a primitive plow, "
     f"sweat on his brow, intense focused expression, "
     f"harsh sun overhead, {FARM_FIELD}. {C}"),

    (13, "013_both_brought_offerings.jpg",
     "In time, both brothers brought an offering to God.",
     f"Two rough stone altars standing side by side on a hillside, "
     f"{CAIN} approaching from one side carrying a bundle of grain, "
     f"{ABEL} approaching from the other side leading a lamb, "
     f"golden light over the ancient landscape, a moment of shared devotion. {C}"),

    (14, "014_cains_offering_grain.jpg",
     "Cain brought the fruits of the soil — a harvest offering.",
     f"{CAIN} laying bundles of grain and produce on a rough stone altar, "
     f"his expression serious and expectant, "
     f"the grain offering arranged on the ancient stones, "
     f"afternoon sunlight, {FARM_FIELD} in background. {C}"),

    (15, "015_abels_offering_flock.jpg",
     "Abel brought fat portions from the firstborn of his flock.",
     f"{ABEL} kneeling before a rough stone altar, offering fat portions of a lamb, "
     f"fire burning on the altar, smoke rising upward, "
     f"his expression humble and reverent, {PASTURE} in background. {C}"),

    (16, "016_god_accepted_abel.jpg",
     "And the Lord looked with favor on Abel and his offering.",
     f"Abel's stone altar with fire burning brightly, smoke rising straight up toward heaven, "
     f"a shaft of divine golden light descending from above onto the altar and {ABEL}, "
     f"Abel's face lit with wonder and joy, the divine approval visible. {C}"),

    (17, "017_god_rejected_cain.jpg",
     "But on Cain and his offering, the Lord did not look with favor.",
     f"Cain's stone altar with grain offering, the smoke drifting sideways never rising, "
     f"no divine light on it, no acknowledgment from above, "
     f"{CAIN} staring at his offering, the sky above it empty and dark, "
     f"the terrible silence of rejection. {C}"),

    (18, "018_cain_was_angry.jpg",
     "And Cain was very angry.",
     f"Portrait close-up of {CAIN}'s face — jaw clenched, dark eyes burning with anger, "
     f"fists at his sides, the frustration and fury barely contained, "
     f"dramatic harsh sidelight casting half his face in deep shadow. {C}"),

    (19, "019_cains_face_fell.jpg",
     "His face fell.",
     f"Portrait of {CAIN} looking downward, face cast in shadow, "
     f"expression dark and bitter, the joy of the world entirely drained from his features, "
     f"the light from Abel's altar visible in the background while Cain stands in darkness. {C}"),

    (20, "020_why_are_you_angry.jpg",
     "Why are you angry? God asked. Why is your face downcast?",
     f"{CAIN} standing alone in the field, divine golden light surrounding him, "
     f"the question hanging in the air, Cain's bitter face illuminated by the divine presence, "
     f"God unseen but felt, an intervention before the catastrophe. {C}"),

    (21, "021_if_you_do_right.jpg",
     "If you do what is right, will you not be accepted?",
     f"Wide atmospheric shot of {CAIN} standing at a crossroads in the ancient landscape, "
     f"one path leading toward light and the other toward shadow, "
     f"the choice before him vast and silent, "
     f"golden light on one side, growing darkness on the other. {C}"),

    (22, "022_sin_crouching_at_door.jpg",
     "But if you do not do what is right, sin is crouching at your door.",
     f"The entrance to an ancient stone dwelling at night, "
     f"a dark ominous shadowy presence crouching in the darkness at the doorway threshold, "
     f"orange firelight flickering from inside the doorway, "
     f"the shadow of something dangerous and hungry lurking, "
     f"deeply ominous symbolic image, ancient setting. {C}"),

    (23, "023_sin_desires_to_have_you.jpg",
     "It desires to have you.",
     f"Extreme close-up of {CAIN}'s face, the shadow of something dark creeping over his features "
     f"from the side, his expression caught between awareness and surrender, "
     f"dramatic chiaroscuro lighting, the darkness reaching for him. {C}"),

    (24, "024_you_must_rule_over_it.jpg",
     "But you must rule over it.",
     f"Wide shot of {CAIN} standing alone in the open ancient landscape, "
     f"divine golden light from above illuminating him, "
     f"the last moment before the wrong choice, "
     f"the weight of free will visible in his posture. {C}"),

    (25, "025_cain_did_not_listen.jpg",
     "Cain did not listen.",
     f"Profile portrait of {CAIN} turning away, his face set and cold, "
     f"the divine light behind him, his back to it, "
     f"the decision made in the darkness of his heart, "
     f"deeply somber and tragic. {C}"),

    (26, "026_lets_go_to_field.jpg",
     "He said to his brother Abel: let's go out to the field.",
     f"{CAIN} speaking to {ABEL}, Cain's expression deceptively calm, "
     f"Abel listening with an open trusting face, "
     f"the green fields behind them, the terrible innocence of the moment. {C}"),

    (27, "027_while_in_the_field.jpg",
     "And while they were out in the field...",
     f"Wide shot of the open ancient field, two small figures of {CAIN} and {ABEL} "
     f"walking together in the distance, "
     f"the vast empty landscape around them, the sky darkening, "
     f"a sense of terrible foreboding, cinematic wide shot. {C}"),

    (28, "028_cain_rose_against_abel.jpg",
     "Cain rose up against his brother Abel.",
     f"Wide distant shot of {CAIN} and {ABEL} in an open field, shown as silhouettes against "
     f"a darkening sky, the violence of the moment conveyed through posture and shadow, "
     f"not graphic but deeply devastating, ancient field setting. {C}"),

    (29, "029_and_he_killed_him.jpg",
     "And he killed him.",
     f"Wide aerial-like shot of an open ancient field, "
     f"{ABEL} fallen on the ancient ground, {CAIN} standing over him, "
     f"shot from a great distance with a long lens, both figures small against the vast landscape, "
     f"the enormity of the act made clear by the emptiness around them. {C}"),

    (30, "030_first_death_first_murder.jpg",
     "The first death. The first murder.",
     f"Wide desolate shot of the empty ancient field at golden hour, "
     f"Abel's fallen shepherd's crook lying abandoned in the grass, "
     f"a lamb standing alone looking lost without its shepherd, "
     f"no humans visible, the aftermath in silence. {C}"),

    (31, "031_abels_blood_cried_out.jpg",
     "Abel's blood cried out from the ground.",
     f"Extreme close-up of ancient dry earth with a dark stain soaking into it, "
     f"Abel's rough shepherd's sandal visible at the edge of frame, "
     f"no body visible, only what the earth received, "
     f"sacred and sorrowful, the ground as witness. {C}"),

    (32, "032_where_is_your_brother.jpg",
     "Then the Lord said to Cain: Where is your brother Abel?",
     f"{CAIN} standing alone in the empty field, "
     f"divine golden light surrounding him on all sides, inescapable, "
     f"the question hanging in the air, Cain's face exposed and guilty. {C}"),

    (33, "033_am_i_my_brothers_keeper.jpg",
     "I don't know, Cain said. Am I my brother's keeper?",
     f"Close-up portrait of {CAIN}'s face, defiant and evasive, "
     f"his jaw set, eyes not meeting the divine light, "
     f"the terrible lie written on his features, "
     f"the first human cover-up. {C}"),

    (34, "034_what_have_you_done.jpg",
     "What have you done? the Lord said.",
     f"{CAIN} in the field, the divine light now cold and judgmental rather than warm, "
     f"Cain's face caught fully in that light, "
     f"nowhere to hide, the weight of what he has done crushing him. {C}"),

    (35, "035_blood_cries_from_ground.jpg",
     "Your brother's blood cries out to me from the ground.",
     f"Wide shot of the ancient field where Abel fell, "
     f"the ground itself seeming to glow faintly at the spot where the blood was spilled, "
     f"divine light picking out the earth, "
     f"the landscape as testimony, sacred and haunting. {C}"),

    (36, "036_cursed_from_ground.jpg",
     "You are now cursed from the ground.",
     f"Portrait of {CAIN} hearing his sentence, "
     f"the divine light now a cold harsh white above him, "
     f"his face absorbing the weight of the curse, "
     f"the fields he worked visible around him, "
     f"everything he built now taken from him. {C}"),

    (37, "037_ground_yields_no_crops.jpg",
     "When you work the soil, it will no longer yield its crops for you.",
     f"Close-up of dry cracked dead earth, "
     f"a broken farming tool lying in the barren ground, "
     f"no crops growing, thorns and dust, "
     f"the curse made physical, the earth rejecting its farmer. {C}"),

    (38, "038_restless_wanderer.jpg",
     "You will be a restless wanderer on the earth.",
     f"{CAIN} walking alone across a vast empty ancient landscape, "
     f"small figure against enormous wilderness, no destination, "
     f"harsh light, {OUTSIDE_EDEN}, the loneliness of his sentence. {C}"),

    (39, "039_punishment_too_great.jpg",
     "Cain said to the Lord: my punishment is more than I can bear.",
     f"Close-up portrait of {CAIN} on his knees, face tilted upward, "
     f"expression of anguish and desperation, "
     f"tears on his olive face, the enormity of his loss hitting him, "
     f"dramatic upward light. {C}"),

    (40, "040_driving_me_from_land.jpg",
     "Today you are driving me from the land.",
     f"{CAIN} looking back at the landscape he knows — the fields, the family home in distance — "
     f"his back to camera, the last look at home, "
     f"the world he is being expelled from visible behind him. {C}"),

    (41, "041_hidden_from_presence.jpg",
     "I will be hidden from your presence.",
     f"Wide shot of {CAIN} walking away into a vast empty landscape, "
     f"the divine light visible behind him but not reaching him now, "
     f"the growing distance between Cain and God made visual. {C}"),

    (42, "042_whoever_finds_me.jpg",
     "I will be a restless wanderer — and whoever finds me will kill me.",
     f"Close-up of {CAIN}'s face, looking around with fear, "
     f"his eyes scanning the horizon for unseen threats, "
     f"the paranoia of the condemned, the empty wilderness around him, "
     f"fear and isolation. {C}"),

    (43, "043_vengeance_seven_times.jpg",
     "But the Lord said: anyone who kills Cain will suffer vengeance seven times over.",
     f"{CAIN} in the wilderness, divine light briefly returning to him, "
     f"not warm but protective, the mercy within judgment, "
     f"Cain's face showing disbelief at this unexpected grace. {C}"),

    (44, "044_lord_put_mark_on_cain.jpg",
     "And the Lord put a mark on Cain.",
     f"Close-up of {CAIN}'s forehead as a divine luminous mark is placed upon it — "
     f"a faintly glowing symbol of divine protection, "
     f"Cain's eyes closed as the mark is given, "
     f"the mercy of God visible even in exile. {C}"),

    (45, "045_none_would_kill_him.jpg",
     "So that no one who found him would kill him.",
     f"Portrait of {CAIN} standing in the wilderness, "
     f"the divine mark faintly visible on his forehead, "
     f"his expression unreadable — protected but exiled, marked but alive, "
     f"the paradox of grace and punishment. {C}"),

    (46, "046_cain_left_lords_presence.jpg",
     "So Cain left the Lord's presence.",
     f"Wide cinematic shot of {CAIN}'s back as he walks away across a vast ancient landscape, "
     f"the divine light fading behind him as he moves further away, "
     f"the silhouette of the lone wanderer against a dimming sky. {C}"),

    (47, "047_land_of_nod.jpg",
     "And settled in the land of Nod, east of Eden.",
     f"Desolate ancient wilderness landscape stretching to the horizon — the land of Nod — "
     f"dry rocky terrain, sparse ancient trees, vast emptiness, "
     f"a small lone figure of {CAIN} in the far distance, "
     f"east of Eden but very far from it. {C}"),

    (48, "048_abel_was_gone.jpg",
     "Abel was gone.",
     f"Abel's empty hillside pasture — "
     f"his shepherd's crook planted in the ground, his rough cloak folded nearby, "
     f"the sheep grazing without direction, "
     f"the absence of their shepherd felt in every frame. {C}"),

    (49, "049_flock_without_shepherd.jpg",
     "His flock grazed without a shepherd.",
     f"Wide pastoral shot of Abel's sheep scattered across the hillside, "
     f"grazing aimlessly without direction, "
     f"golden afternoon light, {PASTURE}, "
     f"the gentle sadness of animals without their keeper. {C}"),

    (50, "050_altar_stood_silent.jpg",
     "His altar stood cold and silent.",
     f"Abel's rough stone altar, cold now, no fire burning, "
     f"charred remnants of the last offering visible, "
     f"wildflowers beginning to grow around the base, "
     f"the altar as a memorial, abandoned and beautiful. {C}"),

    (51, "051_adam_eve_grieved.jpg",
     "Adam and Eve grieved deeply.",
     f"Wide shot of {ADAM} and {EVE} sitting together outside their ancient stone dwelling, "
     f"both bent forward in grief, Eve's head against Adam's shoulder, "
     f"the posture of deep mourning, "
     f"dim soft light of dusk, the loneliest evening of their lives. {C}"),

    (52, "052_eve_conceived_again.jpg",
     "And in time, Eve conceived again.",
     f"Portrait of {EVE} alone at dawn, her hands over her abdomen, "
     f"a fragile expression of tentative hope on her worn face, "
     f"soft morning light beginning to touch the ancient landscape behind her. {C}"),

    (53, "053_gave_birth_to_son.jpg",
     "She gave birth to a son.",
     f"Close-up of {EVE} holding a newborn infant — Seth — "
     f"her face older and more worn than when she held Cain, but lit with the same fierce love, "
     f"tears on her cheeks, warm firelight, an ancient stone dwelling. {C}"),

    (54, "054_named_him_seth.jpg",
     "And she named him Seth.",
     f"Intimate close-up of {EVE} looking down at baby Seth in her arms, "
     f"the baby's eyes open, the beginnings of life, "
     f"Eve's worn face full of wonder and grief and love all at once, "
     f"soft warm firelight, ancient and tender. {C}"),

    (55, "055_another_child_for_abel.jpg",
     "God has granted me another child in place of Abel, she said. The line of Adam continued. But something in the world would never be the same.",
     f"Final wide cinematic shot: {ADAM} and {EVE} sitting together outside their ancient dwelling at dusk, "
     f"Eve holding baby Seth, Adam's arm around her, "
     f"the vast harsh landscape around them, "
     f"Abel's empty hillside visible in the far distance, "
     f"the first family, diminished and grieving but still together, life continuing. {C}"),
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


def generate_google(prompt, out_path, key):
    for attempt in range(5):
        try:
            data = _imagen_predict("imagen-4.0-ultra-generate-001", prompt, key)
            out_path.write_bytes(data)
            return
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
            print("      (used Nano Banana fallback)")
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
    print(f"\nChapter 3: Cain and Abel — generating {len(scenes)} images")
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

        time.sleep(15)

    done = sum(1 for _, fn, _, _ in SCENES if (OUT_DIR / fn).exists())
    print(f"\nDone. {done}/{len(SCENES)} images in {OUT_DIR}/")


if __name__ == "__main__":
    main()
