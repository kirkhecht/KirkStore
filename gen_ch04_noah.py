#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 4 — Noah and the Flood (Scenes 1-55)

Generates ultra-cinematic still images for Chapter 4.
Output: project/stories/ch04_noah/

Usage:
    python gen_ch04_noah.py              # full run
    python gen_ch04_noah.py --start 10   # resume from scene 10
    python gen_ch04_noah.py --dry-run    # print prompts only
"""

import os, sys, time, base64, argparse, requests
from pathlib import Path

OUT_DIR = Path("project/stories/ch04_noah")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Character descriptors ──────────────────────────────────────────────────────

NOAH = (
    "Noah: ancient Middle Eastern elderly man, long silver-gray beard and hair, "
    "warm olive tan skin, deep-set weathered dark eyes, dignified wise face, "
    "ordinary build not idealized, wearing rough ancient woven linen robes, ancient biblical era"
)

NOAH_FAMILY = (
    "Noah's family: ancient Middle Eastern people — Noah and his sons and their wives — "
    "wearing rough ancient woven linen garments, ordinary natural appearance, "
    "not idealized, ancient biblical era"
)

ARK = (
    "the great ancient ark: enormous rectangular wooden vessel of dark cypress wood "
    "sealed with black pitch, three massive decks tall, dwarfing everything around it, "
    "built exactly to God's specifications, ancient and colossal"
)

C = (
    "ultra photorealistic, 8K cinema camera, IMAX cinematic quality, dramatic lighting, "
    "no text overlays no watermarks no subtitles, film grain, anamorphic lens flare, movie still frame, "
    "ancient biblical setting only, no modern elements no modern vehicles no modern clothing "
    "no modern buildings, strictly ancient biblical era"
)

# ── Scene definitions ──────────────────────────────────────────────────────────
SCENES = [

    (1, "001_noah_title.jpg",
     "Noah.",
     f"Ancient weathered wooden plank of dark cypress wood, "
     f"rain-soaked and gleaming, a single white dove feather resting on it, "
     f"stormy sky reflected in a shallow puddle on the ancient ground, "
     f"no humans, cinematic still life. {C}"),

    (2, "002_world_became_wicked.jpg",
     "The world God had made became corrupted.",
     f"Wide cinematic shot of a dark ancient settlement at night, "
     f"fires burning, shadows of people in conflict, "
     f"the beautiful world twisted and broken, smoke rising, "
     f"the moral darkness made visually palpable, ancient Middle Eastern landscape. {C}"),

    (3, "003_wickedness_of_man.jpg",
     "The wickedness of man was great upon the earth.",
     f"Close-up of ancient hands — rough, grasping, violent — "
     f"conveying the fallen nature of humanity, "
     f"harsh harsh light casting deep shadows, "
     f"the darkness of human nature in the ancient world. {C}"),

    (4, "004_every_intention_evil.jpg",
     "And every intention of man's heart was only evil, continually.",
     f"Ancient crowd scene — people in rough ancient garments turning away from light, "
     f"backs to a divine glow, faces turned toward shadow, "
     f"the collective rejection of goodness, ancient Middle Eastern setting. {C}"),

    (5, "005_lord_saw_and_grieved.jpg",
     "The Lord saw this. And his heart was deeply troubled.",
     f"Abstract divine perspective: looking down over a dark ancient world, "
     f"a shaft of warm golden divine light trying to pierce through heavy storm clouds, "
     f"the light dimmed but not extinguished, "
     f"grief and love in the tension between light and darkness. {C}"),

    (6, "006_will_wipe_from_earth.jpg",
     "I will wipe from the face of the earth the human race I have created.",
     f"Wide shot of ancient landscape under an ominous gathering sky, "
     f"dark storm clouds massing on the horizon, "
     f"the beauty of the creation still visible but the judgment approaching, "
     f"no humans, atmospheric and foreboding. {C}"),

    (7, "007_but_noah_was_different.jpg",
     "But Noah was different.",
     f"Portrait of {NOAH} standing alone in the open landscape, "
     f"facing toward a shaft of divine golden light, "
     f"his back to the dark world behind him, "
     f"the one man who stood apart, dignified and solitary. {C}"),

    (8, "008_noah_found_favor.jpg",
     "Noah found favor in the eyes of the Lord.",
     f"Close-up portrait of {NOAH}'s weathered face, "
     f"divine golden light falling on his features, "
     f"his eyes calm and deep with faith, "
     f"the favor of God visible in the light that rests on him. {C}"),

    (9, "009_noah_was_righteous.jpg",
     "He was a righteous man, blameless among the people of his time.",
     f"{NOAH} kneeling alone in prayer in an open field at dawn, "
     f"hands folded, head bowed, "
     f"the early golden light of morning on his silver hair and robes, "
     f"a man at peace with his God. {C}"),

    (10, "010_noah_walked_with_god.jpg",
     "And Noah walked with God.",
     f"Wide shot of {NOAH} walking along a quiet ancient path, "
     f"divine golden light walking beside him — suggested by a luminous presence — "
     f"the two in companionship, the ancient landscape peaceful around them. {C}"),

    (11, "011_god_spoke_to_noah.jpg",
     "God said to Noah: I am going to put an end to all people.",
     f"{NOAH} alone, the divine presence surrounding him as overwhelming golden light, "
     f"Noah's face lifted upward, listening with solemn attention, "
     f"the gravity of what he is hearing visible in every line of his face. {C}"),

    (12, "012_build_an_ark.jpg",
     "So make yourself an ark of cypress wood.",
     f"{NOAH} standing before an enormous ancient cypress forest, "
     f"divine light illuminating the trees, "
     f"Noah's expression of overwhelming responsibility and absolute obedience, "
     f"the sheer scale of what God has asked made visible. {C}"),

    (13, "013_ark_dimensions.jpg",
     "Make it three hundred cubits long, fifty wide, and thirty high.",
     f"Wide shot of the vast open plain where the ark will be built, "
     f"Noah measuring the ground with rough rope, "
     f"the scale of the construction laid out, "
     f"an enormous open field with divine light showing the dimensions. {C}"),

    (14, "014_noah_obeyed.jpg",
     "Noah did everything just as God commanded him.",
     f"Portrait of {NOAH} with simple determination on his face, "
     f"ancient building tools in his hands, "
     f"the first timber of the ark visible behind him, "
     f"the obedience of faith made tangible. {C}"),

    (15, "015_noah_building_ark.jpg",
     "He built the ark with his sons, beam by beam, plank by plank.",
     f"{NOAH_FAMILY} working together on the massive ark construction, "
     f"{ARK} rising in the background, "
     f"ancient tools, rough-hewn timber, the enormous scale of the project, "
     f"sweat and labor in the hot sun, ancient landscape. {C}"),

    (16, "016_animals_coming.jpg",
     "Then God said: bring two of every living creature into the ark.",
     f"Wide cinematic shot of the completed {ARK} standing on dry land, "
     f"an extraordinary procession of animals approaching from every direction, "
     f"lions, elephants, deer, birds — every kind — "
     f"moving peacefully toward the ark, golden afternoon light. {C}"),

    (17, "017_two_by_two.jpg",
     "Two by two they came — every creature of the earth.",
     f"Magnificent wide shot of paired animals walking toward {ARK}: "
     f"two lions, two camels, two deer, two elephants, two horses, pairs of birds, "
     f"all moving peacefully in pairs, the great procession of life, "
     f"golden light, dramatic and beautiful. {C}"),

    (18, "018_male_and_female.jpg",
     "Male and female, every kind.",
     f"Close-up of a pair of doves landing together on the ramp of {ARK}, "
     f"wings folding, the intimacy of a pair, "
     f"other animals visible in soft focus behind them, "
     f"warm golden light on their white feathers. {C}"),

    (19, "019_enter_the_ark.jpg",
     "Then the Lord said: Go into the ark, you and your whole family.",
     f"{NOAH} standing at the great entrance ramp of {ARK}, "
     f"divine light behind and above him, "
     f"his face upturned in final obedience, "
     f"the enormous dark doorway of the ark before him. {C}"),

    (20, "020_noahs_family_entered.jpg",
     "Noah entered the ark, and his sons, his wife, and his sons' wives.",
     f"Wide shot of {NOAH_FAMILY} walking up the great ramp into {ARK}, "
     f"their figures small against the enormous vessel, "
     f"the last glimpse of the outside world visible behind them, "
     f"solemn and purposeful. {C}"),

    (21, "021_god_shut_the_door.jpg",
     "Then the Lord shut them in.",
     f"The great wooden door of {ARK} swinging closed from the outside, "
     f"sealed by divine force, "
     f"no human hand visible, the door closing by itself, "
     f"the final crack of daylight disappearing as the door seals shut, "
     f"dramatic and momentous. {C}"),

    (22, "022_seven_days_waiting.jpg",
     "For seven days, nothing happened.",
     f"Wide still shot of {ARK} sitting alone on the dry landscape, "
     f"utterly still and silent, "
     f"the sky beginning to darken at the horizon, "
     f"the waiting, the last days of the old world. {C}"),

    (23, "023_the_rain_began.jpg",
     "And then the rain began.",
     f"Cinematic wide shot of the first massive raindrops beginning to fall, "
     f"the sky opening with torrential rain, "
     f"{ARK} visible in the background as rain begins to sheet down, "
     f"the first drops hitting dry dusty earth, dramatic and ominous. {C}"),

    (24, "024_forty_days_nights.jpg",
     "For forty days and forty nights, the rain fell.",
     f"Dramatic shot of {ARK} in the midst of a catastrophic storm, "
     f"torrential rain, lightning illuminating the sky, "
     f"the waters beginning to rise around the ark, "
     f"the fury of the flood at its height. {C}"),

    (25, "025_waters_rose.jpg",
     "The waters rose and increased greatly on the earth.",
     f"Wide cinematic shot of floodwaters spreading rapidly across the ancient landscape, "
     f"trees and hills disappearing under the rising water, "
     f"{ARK} beginning to lift off the ground and float, "
     f"the scale of the catastrophe overwhelming. {C}"),

    (26, "026_mountains_covered.jpg",
     "They rose and covered the mountains to a depth of more than fifteen cubits.",
     f"Aerial-perspective shot of the entire world under water, "
     f"only the very peaks of mountains still barely visible, "
     f"then even those disappearing beneath the endless gray water, "
     f"the total obliteration of the world. {C}"),

    (27, "027_everything_perished.jpg",
     "Every living thing that moved on land perished.",
     f"Haunting wide shot of the flooded world — "
     f"vast gray water stretching to every horizon, "
     f"complete silence and stillness, "
     f"no land visible, nothing alive, only water and sky, "
     f"the most total silence in history. {C}"),

    (28, "028_ark_floated.jpg",
     "But the ark floated on the surface of the water.",
     f"Majestic wide shot of {ARK} alone on the vast endless floodwaters, "
     f"the tiny vessel carrying all remaining life on an ocean that covers the world, "
     f"storm clouds above, gray water in every direction, "
     f"the ark small but unbroken. {C}"),

    (29, "029_god_remembered_noah.jpg",
     "But God remembered Noah.",
     f"The surface of the endless floodwaters at dawn, "
     f"a single shaft of warm golden divine light breaking through the storm clouds "
     f"and finding {ARK} on the water below, "
     f"the first light of grace returning after the long darkness. {C}"),

    (30, "030_wind_sent_over_earth.jpg",
     "And God sent a wind over the earth, and the waters receded.",
     f"Dramatic wide shot of powerful ancient winds moving across the surface of the floodwaters, "
     f"the water beginning to ripple and recede, "
     f"light breaking through the parting clouds above, "
     f"the turning point of the flood, the beginning of the end. {C}"),

    (31, "031_waters_receded.jpg",
     "The waters receded steadily from the earth.",
     f"Wide cinematic shot showing the gradual recession of floodwaters, "
     f"muddy shorelines beginning to emerge, "
     f"the very tops of hills reappearing from the water, "
     f"golden light beginning to warm the newly revealed earth. {C}"),

    (32, "032_ark_rested_on_ararat.jpg",
     "And on the seventeenth day, the ark came to rest on the mountains of Ararat.",
     f"Dramatic wide shot of {ARK} resting on the snow-capped peaks of Mount Ararat, "
     f"majestic ancient mountain emerging from receding clouds, "
     f"the ark settled firmly on the mountain, "
     f"golden light breaking through, the first solid ground. {C}"),

    (33, "033_mountaintops_appeared.jpg",
     "The tops of the mountains became visible.",
     f"Panoramic wide shot of ancient mountain peaks emerging from receding floodwaters, "
     f"their summits breaking the surface one by one, "
     f"golden morning light illuminating the revealed peaks, "
     f"the world returning, dramatic and beautiful. {C}"),

    (34, "034_noah_opened_window.jpg",
     "After forty more days, Noah opened the window of the ark.",
     f"Close-up of {NOAH}'s weathered hands pushing open a small wooden window in the side of {ARK}, "
     f"blinding white light flooding through the opening, "
     f"Noah's eyes squinting against the light after months of darkness, "
     f"the first fresh air. {C}"),

    (35, "035_sent_out_raven.jpg",
     "He sent out a raven, and it kept flying back and forth.",
     f"{NOAH} releasing a large black raven from the ark window, "
     f"the raven spreading its wings against a sky of clearing clouds, "
     f"flying out over the still-vast floodwaters, "
     f"a lone black bird against a brightening sky. {C}"),

    (36, "036_sent_out_dove.jpg",
     "Then he sent out a dove to see if the water had receded.",
     f"{NOAH}'s weathered hands gently releasing a pure white dove from the ark window, "
     f"the dove taking flight with wings spread, "
     f"white against the gray sky over the floodwaters, "
     f"hope sent out over the water. {C}"),

    (37, "037_dove_returned.jpg",
     "But the dove could find no place to set its feet. It returned.",
     f"The white dove returning to the ark window, "
     f"{NOAH}'s hands reaching out to receive it, "
     f"the dove's feet finding no rest in all the flooded world, "
     f"the disappointing but tender return. {C}"),

    (38, "038_noah_reached_out.jpg",
     "Noah reached out his hand and brought it back inside the ark.",
     f"Extreme close-up of {NOAH}'s gentle weathered hands "
     f"carefully cupping the small white dove and drawing it back inside, "
     f"the dove settling into the warmth of his hands, "
     f"an intimate tender moment of care. {C}"),

    (39, "039_second_dove.jpg",
     "He waited seven days and sent the dove out again.",
     f"{NOAH} at the window of {ARK}, "
     f"releasing the white dove a second time into a brightening sky, "
     f"more light now, fewer clouds, "
     f"his expression of hopeful patience. {C}"),

    (40, "040_dove_with_olive_branch.jpg",
     "This time, the dove returned with a fresh olive leaf in its beak.",
     f"The white dove returning to Noah's outstretched hand "
     f"with a small fresh green olive branch in its beak, "
     f"the green of new life vivid against the white feathers, "
     f"Noah's face breaking into wonder and joy, "
     f"the most hopeful image in the story. {C}"),

    (41, "041_noah_knew.jpg",
     "Then Noah knew that the water had receded from the earth.",
     f"Portrait of {NOAH}'s face as he holds the olive branch, "
     f"tears on his weathered cheeks, expression of overwhelming relief and gratitude, "
     f"the tiny green branch in his trembling hands, "
     f"the end of the long ordeal finally visible. {C}"),

    (42, "042_third_dove_sent.jpg",
     "He waited seven more days and sent the dove again.",
     f"{NOAH} releasing the white dove a third time from the ark window, "
     f"the sky now clearly brightening, the water visibly lower, "
     f"his expression of cautious hope as the dove takes flight once more. {C}"),

    (43, "043_dove_did_not_return.jpg",
     "This time it did not return.",
     f"Wide shot of the brightening sky over the receding floodwaters, "
     f"the tiny white silhouette of the dove flying away into the distance, "
     f"growing smaller and smaller until it vanishes, "
     f"the sky open and free, a world waiting. {C}"),

    (44, "044_god_said_come_out.jpg",
     "Then God said to Noah: Come out of the ark.",
     f"{NOAH} inside the ark, divine golden light flooding through the open door, "
     f"his face lifted toward the light, hearing the long-awaited command, "
     f"the weight of months lifting from his features. {C}"),

    (45, "045_noah_emerged.jpg",
     "So Noah came out, together with his sons and his wife and his sons' wives.",
     f"Wide cinematic shot of {NOAH_FAMILY} emerging from {ARK} "
     f"onto a world washed clean, "
     f"stepping onto muddy but solid ground, "
     f"squinting into the overwhelming brightness, "
     f"the first steps on a new earth. {C}"),

    (46, "046_animals_came_out.jpg",
     "And all the animals and creatures came out of the ark.",
     f"Magnificent wide shot of all the animals streaming out of {ARK} "
     f"onto the freshly washed earth, "
     f"lions and deer and birds and every creature, "
     f"spreading out across the new world, "
     f"golden light on a gleaming wet landscape. {C}"),

    (47, "047_noah_built_altar.jpg",
     "Then Noah built an altar to the Lord.",
     f"{NOAH} arranging rough ancient stones into a simple altar on the newly emerged ground, "
     f"his sons helping him build it, "
     f"the gesture of worship as the first act on the new earth, "
     f"gratitude made physical. {C}"),

    (48, "048_burnt_offering.jpg",
     "And taking some of all the clean animals and birds, he sacrificed burnt offerings.",
     f"{NOAH} kneeling before a rough stone altar with fire burning brightly, "
     f"smoke rising straight upward into a clearing sky, "
     f"his expression of profound gratitude and reverence, "
     f"the first offering on the new earth. {C}"),

    (49, "049_pleasing_aroma.jpg",
     "The Lord smelled the pleasing aroma.",
     f"The smoke from Noah's offering rising in a clean straight column "
     f"up through the clearing sky toward heaven, "
     f"divine golden light descending to meet the rising smoke, "
     f"the acceptance of the offering made visible. {C}"),

    (50, "050_never_again_curse_ground.jpg",
     "Never again will I curse the ground because of humans.",
     f"Wide shot of the freshly washed ancient earth, "
     f"new green shoots already beginning to emerge from the rich wet soil, "
     f"golden sunlight on the glistening new world, "
     f"the promise of renewal written in every blade of grass. {C}"),

    (51, "051_as_long_as_earth_endures.jpg",
     "As long as the earth endures, seedtime and harvest, cold and heat, summer and winter, day and night will never cease.",
     f"Breathtaking wide panoramic shot of the renewed earth under a clearing sky, "
     f"rich soil, new growth, rivers running clear again, "
     f"the full cycle of seasons suggested in a single cinematic frame, "
     f"the permanence of the created order restored. {C}"),

    (52, "052_rainbow_in_clouds.jpg",
     "I have set my rainbow in the clouds.",
     f"Dramatic wide cinematic shot of a magnificent full rainbow arching across "
     f"a clearing storm sky over the freshly flooded landscape, "
     f"every color vivid and perfect, "
     f"the first rainbow ever seen, "
     f"the world wet and gleaming below it. {C}"),

    (53, "053_sign_of_covenant.jpg",
     "It will be a sign of the covenant between me and the earth.",
     f"{NOAH} and {NOAH_FAMILY} standing on the new earth looking up at the rainbow overhead, "
     f"their faces lifted in wonder, "
     f"the colors of the rainbow reflected in their upturned faces, "
     f"the rainbow vast above them, the family tiny below. {C}"),

    (54, "054_whenever_rainbow_appears.jpg",
     "Whenever I bring clouds over the earth and the rainbow appears, I will remember my covenant.",
     f"Extreme close-up of the rainbow itself — bands of vivid color across clearing clouds, "
     f"raindrops still in the air catching the light, "
     f"the divine promise written across the sky in light and color, "
     f"breathtakingly beautiful. {C}"),

    (55, "055_never_again_flood.jpg",
     "And the waters will never again become a flood to destroy all life. The promise was made. And the earth began again.",
     f"Final wide cinematic shot: {NOAH} standing alone on the new earth, "
     f"the great rainbow arching overhead, "
     f"the ark visible behind him on the mountain, "
     f"the vast new clean world stretching before him, "
     f"golden light on everything, the beginning of a new chapter. {C}"),
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
    print(f"\nChapter 4: Noah and the Flood — generating {len(scenes)} images")
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
