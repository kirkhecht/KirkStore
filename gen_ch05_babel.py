#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Chapter 5 — The Covenant, The Vineyard, and The Tower of Babel (Scenes 1-50)

Covers Genesis 9-11 from the user's original 10-part script:
  - The Covenant with Noah (rainbow, new commands)
  - Noah's vineyard and Ham's sin
  - Generations multiply — one language
  - The Tower of Babel: ambition, confusion, scattering

Output: project/stories/ch05_babel/
"""

import os, sys, time, base64, argparse, requests
from pathlib import Path

OUT_DIR = Path("project/stories/ch05_babel")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Character descriptors ──────────────────────────────────────────────────────

NOAH = (
    "Noah: ancient Middle Eastern very elderly man, long silver-gray beard and hair, "
    "deep-set weathered dark eyes, dignified wise face, "
    "ordinary build not idealized, wearing rough ancient woven linen robes, ancient biblical era"
)

NOAH_SONS = (
    "Shem and Japheth: two ancient Middle Eastern men in their 40s, "
    "dark hair, olive skin, rough ancient linen robes, "
    "reverent humble posture, not idealized, ancient biblical era"
)

HAM = (
    "Ham: ancient Middle Eastern man in his 40s, "
    "dark hair, olive skin, rough ancient woven garments, "
    "mocking expression, disrespectful posture, ancient biblical era"
)

BUILDERS = (
    "a diverse crowd of ancient Mesopotamian people — men and women — "
    "wearing rough ancient linen and wool garments in muted earth tones, "
    "ordinary builds not idealized, dark hair, olive and brown skin tones, "
    "tools in hand, ancient Sumerian era, not modern"
)

C = (
    "ultra photorealistic, 8K cinema camera, IMAX cinematic quality, dramatic lighting, "
    "no text overlays no watermarks no subtitles, film grain, anamorphic lens flare, movie still frame, "
    "ancient biblical setting only, no modern elements no modern vehicles no modern clothing "
    "no modern buildings, strictly ancient biblical era"
)

# ── Scene definitions ──────────────────────────────────────────────────────────
SCENES = [

    (1, "001_babel_title.jpg",
     "The Tower of Babel.",
     f"Extreme wide shot: an ancient Mesopotamian plain at dawn, "
     f"a massive unfinished brick ziggurat tower rising in stepped tiers "
     f"toward a stormy golden sky, enormous and solitary on the flat plain, "
     f"no people visible, cinematic desolation. {C}"),

    (2, "002_rainbow_covenant.jpg",
     "The promise God made to Noah was unlike any that had come before.",
     f"Sweeping cinematic shot: enormous rainbow arching across a vast sky "
     f"over a post-flood ancient landscape, still-wet earth gleaming, "
     f"sunlight breaking through parting storm clouds, "
     f"ancient biblical landscape with NO ark in view, just the land and sky. {C}"),

    (3, "003_covenant_for_all_creatures.jpg",
     "It was made not only to one man — but to every living creature.",
     f"Wide cinematic shot: diverse animals — cattle, birds, deer — "
     f"moving freely across a lush ancient landscape under a rainbow sky, "
     f"life returning to a cleansed world, animals not people are the focus. {C}"),

    (4, "004_be_fruitful.jpg",
     "He gave Noah's family a command — be fruitful. Multiply. Fill the earth.",
     f"{NOAH_SONS} standing in open land, arms spread wide, "
     f"surveying a vast green ancient landscape, children nearby, "
     f"the weight of a new beginning, ancient biblical setting. {C}"),

    (5, "005_new_permission.jpg",
     "He gave them a new permission — they could now eat the meat of animals, as well as plants.",
     f"Ancient campfire scene: {NOAH} and his family seated around a fire, "
     f"roasting meat, simple clay pots, rough ancient garments, "
     f"the warmth of family in a fresh world, ancient Middle Eastern setting. {C}"),

    (6, "006_life_is_sacred.jpg",
     "He gave them a warning — life was sacred. Whoever shed the blood of a man, by man would his blood be shed.",
     f"Close-up of ancient hands held open, palms up, "
     f"light falling across them in a sacred gesture, "
     f"the weight of divine law conveyed in stillness, ancient biblical setting. {C}"),

    (7, "007_sign_in_sky.jpg",
     "And then — the rainbow. The sign in the sky. The unbreakable covenant.",
     f"Low-angle cinematic shot: {NOAH} standing alone on high ground, "
     f"his aged silhouette against a massive rainbow filling the sky above him, "
     f"arms slightly raised, small before the grandeur of the promise. {C}"),

    (8, "008_world_reset.jpg",
     "The world had been reset. But the human heart had not been.",
     f"Split cinematic composition: left side — pristine ancient landscape, "
     f"right side — shadowed ancient settlement with hints of conflict, "
     f"the contrast of a clean world and a fallen heart, ancient era. {C}"),

    (9, "009_noah_plants_vineyard.jpg",
     "Not long after the waters dried, Noah planted a vineyard.",
     f"{NOAH} kneeling in freshly tilled ancient soil, pressing a vine cutting "
     f"into dark earth with his aged hands, rows of young vines behind him, "
     f"afternoon light on an ancient hillside. {C}"),

    (10, "010_years_pass.jpg",
     "The vineyard grew. The grapes ripened. And one day, Noah drank too much of its wine.",
     f"Close-up: clusters of deep purple grapes heavy on an ancient vine, "
     f"sunlight filtering through the leaves, a clay wine jug at the base of the vine, "
     f"rich harvest detail, no people, ancient vineyard. {C}"),

    (11, "011_noah_in_tent.jpg",
     "He fell asleep — naked — in his tent.",
     f"Interior of a simple ancient tent, dark and shadowed, "
     f"rough woven fabric walls, an elderly sleeping figure visible from behind "
     f"in an undignified posture, no nudity visible — backs and shadow only, "
     f"the vulnerability of a great man, ancient setting. {C}"),

    (12, "012_ham_mocks.jpg",
     "His son Ham saw him there and mocked him.",
     f"{HAM} standing at the entrance of a tent, looking back with a mocking expression, "
     f"face turned away from the tent interior, ancient Middle Eastern setting, "
     f"the disrespect of a son conveyed in posture and expression. {C}"),

    (13, "013_shem_japheth_cover.jpg",
     "His other two sons — Shem and Japheth — walked in backwards and covered their father without looking.",
     f"{NOAH_SONS} walking backwards through a tent doorway together, "
     f"a woven garment spread between them, faces turned away, "
     f"the honor of these sons in their careful reverent posture, ancient setting. {C}"),

    (14, "014_sin_remains.jpg",
     "The flood had washed away the world. It had not washed away sin.",
     f"Wide shot of ancient rolling hills — clean, green, newly inhabited — "
     f"but a solitary shadow falls across the foreground, "
     f"the beauty of the new world carrying the weight of the old nature, "
     f"ancient landscape, no people, only shadow and light. {C}"),

    (15, "015_noahs_death.jpg",
     "Noah lived nine hundred and fifty years. And then he died.",
     f"Exterior of a simple ancient stone dwelling at evening, "
     f"the last light fading behind distant hills, "
     f"an empty wooden chair before the doorway, "
     f"a life fully lived and finished, ancient biblical setting. {C}"),

    (16, "016_generations_multiply.jpg",
     "The sons of Noah multiplied. They had children. Their children had children.",
     f"Wide aerial-style cinematic view of a growing ancient settlement — "
     f"tents expanding into simple stone houses, livestock, "
     f"children playing, the early multiplication of Noah's line, "
     f"ancient Middle Eastern landscape. {C}"),

    (17, "017_one_language.jpg",
     "For a time, they spoke a single language. A single tongue. They could understand each other from coast to coast.",
     f"Cinematic crowd scene: diverse ancient Mesopotamian people gathered in a marketplace, "
     f"{BUILDERS}, animated conversation, gesturing, trading, "
     f"the unity of shared language visible in their interaction, ancient Sumerian setting. {C}"),

    (18, "018_traveling_eastward.jpg",
     "As they traveled together — eastward — they came to a wide, flat land.",
     f"Wide cinematic shot: a long procession of ancient people on foot — {BUILDERS} — "
     f"moving across a vast flat plain toward the horizon, "
     f"the Mesopotamian landscape stretching endlessly before them, ancient era. {C}"),

    (19, "019_land_of_shinar.jpg",
     "A land called Shinar.",
     f"Sweeping panoramic view: the vast flat plain of ancient Mesopotamia — Shinar — "
     f"the Euphrates river visible in the distance, "
     f"fertile land stretching to the horizon under a wide sky, "
     f"ancient Mesopotamian landscape, no people. {C}"),

    (20, "020_they_settled.jpg",
     "And there, they settled.",
     f"Wide shot of ancient Mesopotamian settlement being established: "
     f"simple tents and mud brick structures, {BUILDERS} building early dwellings, "
     f"cooking fires, livestock, the beginning of a permanent settlement, "
     f"flat fertile plain, ancient Sumerian era. {C}"),

    (21, "021_ambition_grows.jpg",
     "But something had begun to grow in them. Ambition. Pride.",
     f"Close-up portrait: ancient Mesopotamian man in rough garments "
     f"looking upward with an intense ambitious expression, "
     f"dramatic side lighting, the hunger for greatness in his eyes, "
     f"ancient Sumerian setting. {C}"),

    (22, "022_make_a_name.jpg",
     "A desire to make a name for themselves.",
     f"Wide shot: group of ancient Mesopotamian leaders — {BUILDERS} — "
     f"gathered in discussion, gesturing emphatically toward the open sky, "
     f"the ambition of early civilization, ancient Sumerian plain, "
     f"flat terrain under a vast sky. {C}"),

    (23, "023_plan_the_city.jpg",
     "They said — come, let us build a city. And a tower. A tower whose top reaches to the heavens.",
     f"Ancient Mesopotamian men planning: rough clay tablets with early architectural "
     f"drawings, hands gesturing over plans, "
     f"firelight illuminating determined faces, ancient Sumerian setting. {C}"),

    (24, "024_not_for_god.jpg",
     "A name for themselves. Not for God. For themselves.",
     f"Cinematic close-up: ancient Mesopotamian man with his hand pressed "
     f"against his own chest — the gesture of self-claim — "
     f"proud expression, firelight, rough ancient garments, "
     f"the pride of human ambition. {C}"),

    (25, "025_making_bricks.jpg",
     "They invented new techniques. They learned to bake bricks instead of cutting stone.",
     f"Ancient brick-making scene: {BUILDERS} working at clay pits and kilns, "
     f"shaping mud bricks, stacking them near blazing kilns, "
     f"smoke rising, the industry of early Mesopotamian civilization. {C}"),

    (26, "026_tar_as_mortar.jpg",
     "They used tar instead of mortar.",
     f"Close-up: ancient workers applying black bitumen tar between courses of "
     f"fired mud bricks, the gleaming dark material between golden brick, "
     f"hands and tools in ancient construction detail. {C}"),

    (27, "027_tower_begins.jpg",
     "And the tower began to rise.",
     f"Wide cinematic shot: the very foundations of a massive stepped ziggurat "
     f"being laid on the Mesopotamian plain, "
     f"hundreds of {BUILDERS} carrying bricks, enormous scale of construction, "
     f"ancient Sumerian setting. {C}"),

    (28, "028_higher_than_before.jpg",
     "Higher than anything humanity had ever built.",
     f"Upward-looking cinematic angle: the base of an enormous ancient brick ziggurat "
     f"rising in stepped tiers above the viewer, "
     f"workers climbing ramps carrying bricks, the tower dwarfing the people below. {C}"),

    (29, "029_monument_to_human_will.jpg",
     "A monument to human will.",
     f"Wide cinematic shot: the partially-built ziggurat tower at mid-construction, "
     f"rising dramatically against a vast sky, "
     f"hundreds of tiny figures working on its flanks, "
     f"the scale of human ambition on the flat Mesopotamian plain. {C}"),

    (30, "030_finger_at_the_sky.jpg",
     "A finger pointing back toward the sky from which the rain had once fallen.",
     f"Dramatic low-angle cinematic shot: the upper tiers of the great ziggurat "
     f"pointing toward a wide blue sky, "
     f"the tower's peak reaching defiantly upward, "
     f"ancient brick construction detail, no people visible from this angle. {C}"),

    (31, "031_god_comes_down.jpg",
     "But the Lord came down to see the city and the tower the children of men had built.",
     f"Aerial perspective: looking down from above the clouds onto the "
     f"flat Mesopotamian plain, the tiny ant-like construction site below, "
     f"the tower small from heaven's vantage point, "
     f"divine perspective on human ambition. {C}"),

    (32, "032_unified_in_pride.jpg",
     "Unified not in worship, but in pride.",
     f"Wide cinematic panorama: vast crowd of ancient Mesopotamian workers "
     f"all working in unison around the tower base, "
     f"the unified energy of a single-minded people, "
     f"the scale of collective ambition, ancient Sumerian plain. {C}"),

    (33, "033_confusion_begins.jpg",
     "So the Creator did something strange. He confused them.",
     f"Cinematic moment: group of {BUILDERS} on a construction scaffold "
     f"suddenly looking at each other in bewilderment, "
     f"one man shouting and others looking baffled, "
     f"mouths open in incomprehension, tools in mid-swing, ancient setting. {C}"),

    (34, "034_language_fractured.jpg",
     "In a single moment — in the middle of a workday — language fractured.",
     f"Close-up of ancient Mesopotamian worker's face: "
     f"mouth open, eyes wide with confusion, "
     f"the exact moment of incomprehension, "
     f"a man speaking but not being understood, ancient construction site. {C}"),

    (35, "035_scaffold_cannot_understand.jpg",
     "The man on the scaffold could no longer understand the man below.",
     f"Cinematic two-shot: ancient worker on elevated scaffold calling down, "
     f"worker below staring up in total confusion, "
     f"both gesturing wildly, the gap of incomprehension between them, "
     f"ancient brick tower construction. {C}"),

    (36, "036_mason_architect.jpg",
     "The mason could not understand the architect.",
     f"Ancient Mesopotamian man with clay architectural plans "
     f"gesturing at the plans and then at the building, "
     f"a mason beside him shrugging in complete incomprehension, "
     f"bafflement and frustration, ancient Sumerian setting. {C}"),

    (37, "037_world_breaks_in_sound.jpg",
     "The world broke apart in sound.",
     f"Wide cinematic chaos scene: construction site suddenly in disorder — "
     f"bricks dropped, ramps abandoned, {BUILDERS} arguing and gesturing, "
     f"total breakdown of coordinated work, the chaos of language confusion. {C}"),

    (38, "038_work_on_tower_stopped.jpg",
     "And work on the tower stopped.",
     f"Wide shot: the unfinished ziggurat tower standing silent and abandoned "
     f"on the Mesopotamian plain, scaffolding empty, tools dropped, "
     f"workers standing in scattered confused groups far below, "
     f"the abandonment of human ambition. {C}"),

    (39, "039_cannot_speak.jpg",
     "They could not finish what they had started. They could not even speak to one another.",
     f"Close-up: two ancient Mesopotamian men face to face, "
     f"both talking at once and neither understanding, "
     f"hands raised in helpless frustration, "
     f"the breakdown of communication. {C}"),

    (40, "040_scattering_begins.jpg",
     "So they scattered. Family by family. Tribe by tribe. Tongue by tongue.",
     f"Wide cinematic shot: multiple groups of ancient people moving "
     f"away from the tower in different directions across the flat plain, "
     f"each group separate, the great scattering beginning, "
     f"ancient Mesopotamian landscape. {C}"),

    (41, "041_across_the_plains.jpg",
     "Across the plains. Across the mountains. Across the rivers. Across the world.",
     f"Sweeping aerial-style view: diverse groups of ancient people "
     f"traveling in all directions — toward distant hills, toward a river, "
     f"into the horizon — the scattering of humanity, ancient landscape. {C}"),

    (42, "042_place_called_babel.jpg",
     "The place was called Babel — because there the Lord confused the language of all the earth.",
     f"Wide establishing shot: the great abandoned ziggurat tower standing alone "
     f"on the empty Mesopotamian plain, "
     f"the Euphrates river in the distance, "
     f"the monument to confusion, ancient and desolate. {C}"),

    (43, "043_one_people_divided.jpg",
     "Humanity — once one people, one tongue, one ambition — was now divided into nations.",
     f"Cinematic panorama: multiple distinct groups of ancient people "
     f"in different terrain — plains, hills, forest edges — each separate, "
     f"the diversity of nations born from one scattering, ancient world. {C}"),

    (44, "044_nations_born.jpg",
     "This is where the nations of the world were born.",
     f"Sweeping cinematic view of an ancient world coming alive: "
     f"distant settlements in different landscapes — some near rivers, "
     f"some in hills, smoke from many fires — the birth of diverse civilizations, "
     f"ancient world. {C}"),

    (45, "045_thousand_languages.jpg",
     "This is where the languages of the earth began.",
     f"Cinematic montage-style image: groups of diverse ancient peoples "
     f"in varied landscapes gesturing and communicating in their own new tongues, "
     f"the richness of human diversity born from one moment, ancient world. {C}"),

    (46, "046_thousand_kings.jpg",
     "From this scattering, a thousand peoples would rise. A thousand tribes. A thousand kings.",
     f"Wide cinematic shot: an ancient walled city in Mesopotamia at golden hour, "
     f"walls and towers, people at the gates, the rise of early civilization, "
     f"the birth of kingdoms from the scattering. {C}"),

    (47, "047_god_choosing.jpg",
     "But out of all of them — God was about to choose one man. One family. One people.",
     f"Wide shot of a vast ancient landscape at dusk: "
     f"countless small campfires scattered across the plain to the horizon, "
     f"one fire glowing slightly brighter in the center, "
     f"the mystery of divine election, ancient world. {C}"),

    (48, "048_city_of_ur.jpg",
     "Somewhere in the city of Ur, in the land of the Chaldeans, a man was about to hear a voice.",
     f"Establishing shot: the ancient city of Ur at dusk — "
     f"its great ziggurat visible on the skyline, "
     f"winding streets, mud brick buildings, the glow of oil lamps in windows, "
     f"the great Sumerian city before Abraham's call. {C}"),

    (49, "049_redemption_beginning.jpg",
     "Through them — He would begin to do something He had been planning since the gates of Eden.",
     f"Close-up: an ancient clay oil lamp burning steadily in the darkness, "
     f"a single warm flame against complete black, "
     f"the promise of a plan already in motion, ancient setting. {C}"),

    (50, "050_creation_coming_back.jpg",
     "He was going to bring His creation back.",
     f"Wide cinematic shot: the ancient world at dawn — "
     f"mountains, valleys, rivers, a vast sky turning from dark to gold — "
     f"the world God made, lit by new light, "
     f"the promise of redemption in the beauty of creation. {C}"),

]

# ── API helpers (same as ch04) ─────────────────────────────────────────────────

def load_env():
    env_path = Path(__file__).parent / ".env"
    env = {}
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env

def _imagen_predict(model, prompt, key, timeout=120):
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:predict?key={key}",
        json={"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "16:9"}},
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
        json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"responseModalities": ["image"]}},
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
            if "RATE_LIMIT" not in str(e):
                print(f"      Ultra error: {str(e)[:80]}, retrying...")
                time.sleep(8)
            else:
                print("      Ultra rate limited — falling back to Nano Banana")
                break

    for attempt in range(5):
        try:
            data = _nano_banana(prompt, key)
            out_path.write_bytes(data)
            print("      (used Nano Banana fallback)")
            return
        except RuntimeError as e:
            wait = min(60, 15 * (attempt + 1))
            print(f"      Nano Banana attempt {attempt+1} failed ({str(e)[:60]}), waiting {wait}s...")
            time.sleep(wait)

    raise RuntimeError("All models failed after retries")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start",   type=int, default=1,  help="Resume from scene N")
    parser.add_argument("--end",     type=int, default=50, help="Stop at scene N")
    parser.add_argument("--dry-run", action="store_true",  help="Print prompts only")
    args = parser.parse_args()

    env = load_env()
    key = env.get("GOOGLE_AI_STUDIO_KEY", "")
    if not key and not args.dry_run:
        sys.exit("GOOGLE_AI_STUDIO_KEY not in .env")

    scenes = [s for s in SCENES if args.start <= s[0] <= args.end]
    print(f"\nChapter 5: The Tower of Babel — generating {len(scenes)} images")
    print(f"Output dir: {OUT_DIR}\n")

    for scene_num, filename, narration, prompt in scenes:
        out_path = OUT_DIR / filename
        print(f"[{scene_num:03d}] {narration[:60]}{'…' if len(narration)>60 else ''}")

        if args.dry_run:
            print(f"       PROMPT: {prompt[:120]}...\n")
            continue

        if out_path.exists():
            size_kb = out_path.stat().st_size // 1024
            print(f"       ✓ Already exists ({size_kb} KB)")
            continue

        t0 = time.time()
        try:
            generate_google(prompt, out_path, key)
            elapsed = time.time() - t0
            size_kb = out_path.stat().st_size // 1024
            print(f"       ✓ Saved ({size_kb} KB, {elapsed:.1f}s)")
        except Exception as e:
            print(f"       ✗ FAILED: {e}")

    print(f"\nDone. Images in {OUT_DIR}/")

if __name__ == "__main__":
    main()
