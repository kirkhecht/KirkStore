"""
Genesis 2-3 Demo — 25 cinematic images depicting Adam, Eve, and the Fall of Man.
Uses google/nano-banana-2 via Replicate. Saves to project/genesis_demo/.
Run: python gen_genesis_demo.py
"""
import os
import time
import urllib.request
from pathlib import Path

OUT_DIR = Path("project/genesis_demo")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SCENES = [
    # (filename, prompt)
    ("01_eden_establishing.jpg",
     "Lush paradise garden of Eden at golden hour, a great river splitting into four tributaries, "
     "towering ancient trees with glowing fruit, vibrant flowers, lions and deer drinking peacefully side by side, "
     "mist rising from the water. Wide cinematic establishing shot, no human figures. "
     "Ultra photorealistic, 8K cinema camera, warm golden light."),

    ("02_two_trees.jpg",
     "Two magnificent ancient trees at the center of paradise garden. The Tree of Life radiates soft golden light, "
     "its bark glowing, fruit luminous. The Tree of Knowledge of Good and Evil stands beside it, "
     "ripe red fruit hanging heavy, a faint darker aura around it. "
     "Extreme wide shot, no people, late afternoon light filtering through canopy. "
     "Ultra photorealistic, 8K, cinematic."),

    ("03_adam_portrait.jpg",
     "Adam, the first man — a powerfully built young Middle Eastern man, dark tanned skin, dark curly hair, "
     "strong jaw, brown eyes, early 30s. Standing in paradise garden surrounded by lush greenery. "
     "Close-up portrait, face fully visible, serene expression, looking at camera. "
     "Natural daylight, photorealistic 8K cinema camera."),

    ("04_adam_naming_animals.jpg",
     "Adam, a powerfully built young Middle Eastern man with dark curly hair and tanned skin, standing in a vast "
     "sun-drenched savanna in Eden. Around him, every kind of animal — elephant, giraffe, lion, eagle perched on his arm, "
     "deer, ox — all looking toward him attentively. Wide cinematic landscape shot. "
     "Golden hour light, ultra photorealistic, 8K."),

    ("05_adam_alone_longing.jpg",
     "Adam, a young Middle Eastern man with dark curly hair, sitting alone on a mossy rock beside the river in Eden, "
     "gazing into the distance with a pensive, searching expression. Animals nearby but none beside him as a companion. "
     "Medium wide shot, warm dusk light. Ultra photorealistic, 8K cinematic."),

    ("06_deep_sleep.jpg",
     "A man lying in a deep supernatural sleep on soft Eden grass, body still, face peaceful, surrounded by flowers. "
     "A divine ethereal golden glow emanates from his side where something is being drawn out. "
     "Cinematic overhead angle, dramatic warm light, no visible face of God. "
     "Ultra photorealistic, 8K."),

    ("07_eve_created.jpg",
     "Eve, the first woman — a strikingly beautiful young Middle Eastern woman with long dark wavy hair, "
     "olive skin, dark almond-shaped eyes, early 20s. She stands newly created in Eden, surrounded by soft light, "
     "an expression of wonder and awakening on her face. "
     "Close-up portrait, looking directly at camera. Natural daylight, ultra photorealistic, 8K cinema camera."),

    ("08_adam_and_eve_together.jpg",
     "Adam and Eve, a young Middle Eastern couple, walking hand in hand through the paradise garden of Eden. "
     "He is tall and dark-haired with tanned skin; she has long dark wavy hair, olive skin, a serene joyful expression. "
     "Lush trees, flowers, and animals around them. Medium wide shot, golden afternoon light. "
     "Ultra photorealistic, 8K cinematic."),

    ("09_serpent_in_tree.jpg",
     "A large, ancient serpent coiled elegantly in the branches of the Tree of Knowledge, its scales iridescent, "
     "gleaming green and gold in dappled light. Red forbidden fruit hanging around it. "
     "No human figures. Macro cinematic close-up of the serpent's intelligent, watchful eyes. "
     "Ultra photorealistic, 8K, cinematic, slightly ominous atmosphere."),

    ("10_eve_and_serpent.jpg",
     "Eve, a beautiful young Middle Eastern woman with long dark wavy hair and olive skin, standing beneath "
     "the Tree of Knowledge, gazing up at a large serpent coiled in its branches. "
     "The serpent looks down at her, as if speaking. "
     "Medium cinematic shot, dramatic light filtering through tree canopy, "
     "expression of fascination and curiosity on Eve's face. Ultra photorealistic, 8K."),

    ("11_forbidden_fruit_closeup.jpg",
     "Extreme macro close-up of a single luminous red fruit hanging from the Tree of Knowledge. "
     "The skin glistens with morning dew, rich crimson color, visually perfect and irresistible. "
     "No people visible. Shallow depth of field, bokeh paradise garden background, "
     "a hint of ominous ethereal glow. Ultra photorealistic, 8K cinematic."),

    ("12_eve_reaching.jpg",
     "Eve, a beautiful young Middle Eastern woman with long dark wavy hair, reaching up with one hand "
     "toward a glowing red fruit on the Tree of Knowledge. Her expression: torn between desire and hesitation. "
     "Close-up of her face and outstretched hand, the fruit inches away. "
     "Dramatic cinematic lighting, ultra photorealistic, 8K."),

    ("13_eve_eating.jpg",
     "Extreme close-up of Eve's face and lips — a beautiful young Middle Eastern woman — as she takes the "
     "first bite of the forbidden fruit. Eyes wide open, a complex expression: the instant of transgression. "
     "Juice on her lips, dramatic light, cinematic shallow focus. Ultra photorealistic, 8K."),

    ("14_adam_eating.jpg",
     "Adam, a powerfully built young Middle Eastern man with dark curly hair, receiving the fruit from Eve's hands "
     "and taking a bite. His eyes begin to widen. The moment of choice. "
     "Close-up, dramatic side-lighting, ultra photorealistic, 8K cinematic."),

    ("15_eyes_opened_shame.jpg",
     "Adam and Eve standing together in Eden, both clutching large fig leaves to their bodies, "
     "eyes wide with sudden shame and awareness, hands trembling. "
     "Their faces show horror and vulnerability — the innocence is gone. "
     "Medium shot, hard dramatic light cutting through the canopy, ultra photorealistic, 8K."),

    ("16_hiding_in_leaves.jpg",
     "Adam and Eve crouching together among massive tropical fig leaves deep in the garden, "
     "pressing their bodies against the undergrowth, hiding. Fearful expressions, looking upward. "
     "Medium close shot, dappled shadow light, ultra photorealistic, 8K cinematic."),

    ("17_god_walking_in_garden.jpg",
     "Ancient garden path in Eden at dusk, glowing footsteps of divine presence walking along the path "
     "through dense trees. The air shimmers with golden light. No human visible, no face of God — "
     "only the approach of divine light. "
     "Wide cinematic shot, atmospheric haze, ultra photorealistic, 8K."),

    ("18_confrontation.jpg",
     "Adam and Eve standing before an overwhelming column of divine golden light in the garden clearing, "
     "both looking downward in shame and fear, arms crossed over themselves. "
     "The light is blinding and majestic, filling the frame. "
     "Wide cinematic shot, ultra photorealistic, dramatic lighting, 8K."),

    ("19_adam_blaming_eve.jpg",
     "Adam, a young Middle Eastern man, pointing accusingly at Eve beside him, "
     "his face full of fear and blame. Eve looks away in anguish. "
     "Both surrounded by shafts of harsh light in the garden clearing. "
     "Medium shot, dramatic cinematic lighting, ultra photorealistic, 8K."),

    ("20_serpent_cursed.jpg",
     "The iridescent serpent falling from the Tree of Knowledge, striking the ground, "
     "beginning to writhe and crawl on its belly in the dirt. "
     "A visible aura of divine judgment — amber light and shadow — pressing it down. "
     "No people visible. Dramatic wide-angle shot, ultra photorealistic, 8K cinematic."),

    ("21_consequences.jpg",
     "Eve, a beautiful Middle Eastern woman, sitting on a rock in a suddenly harsher landscape — "
     "the flowers wilting at the edges, thorns appearing among the vines. "
     "Her expression: grief, pain, understanding the weight of what was lost. "
     "Medium shot, cooler dramatic light, ultra photorealistic, 8K."),

    ("22_toil_and_thorns.jpg",
     "Adam, a strong Middle Eastern man, bent over hard rocky ground outside Eden, "
     "hands grasping a crude wooden tool, sweat on his brow, thorns and thistles around him. "
     "A vast barren landscape stretches behind him. "
     "Wide cinematic shot, harsh midday light, ultra photorealistic, 8K."),

    ("23_garments_of_skin.jpg",
     "Adam and Eve dressed in simple rough animal-skin garments, standing solemnly in a clearing. "
     "Their expressions: grateful but grieving. A soft divine amber light still touches them. "
     "Medium wide shot, cinematic lighting, ultra photorealistic, 8K."),

    ("24_expelled_from_eden.jpg",
     "Adam and Eve walking away from Eden, seen from behind, silhouetted against the blazing light "
     "of the garden gates. The landscape ahead is stark and barren. "
     "They walk together, leaning on each other. "
     "Wide cinematic shot, extreme contrast, ultra photorealistic, 8K."),

    ("25_cherubim_and_sword.jpg",
     "The gates of the Garden of Eden — two massive ancient stone pillars — guarded by a blazing "
     "supernatural being, a cherubim with wings of fire, holding a flaming sword that rotates in all directions. "
     "The blade roils with living fire and golden light. No people visible. "
     "Wide dramatic shot looking toward the sealed garden entrance, ultra photorealistic, 8K cinematic."),
]


def main():
    import replicate

    api_key = os.getenv("REPLICATE_API_KEY", "")
    if not api_key:
        # Try loading from .env file
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("REPLICATE_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        raise RuntimeError("REPLICATE_API_KEY not set. Add it to .env or export it.")

    os.environ["REPLICATE_API_TOKEN"] = api_key

    total = len(SCENES)
    already = sum(1 for fn, _ in SCENES if (OUT_DIR / fn).exists())
    print(f"Genesis 2-3 Demo — {total} scenes | {already} already done | {total - already} remaining")
    print(f"Saving to: {OUT_DIR.resolve()}\n")

    for i, (filename, prompt) in enumerate(SCENES, 1):
        out = OUT_DIR / filename
        if out.exists():
            print(f"[{i:02d}/{total}] {filename} — cached")
            continue

        print(f"[{i:02d}/{total}] Generating: {filename}...")
        for attempt in range(5):
            try:
                output = replicate.run(
                    "google/nano-banana-2",
                    input={
                        "prompt":        prompt,
                        "aspect_ratio":  "16:9",
                        "output_format": "jpg",
                    }
                )
                url = str(output[0]) if isinstance(output, list) else str(output)
                urllib.request.urlretrieve(url, out)
                print(f"  → saved {filename}")
                break
            except Exception as exc:
                msg = str(exc)
                if "429" in msg or "throttled" in msg.lower() or "rate limit" in msg.lower():
                    wait = 15 * (2 ** attempt)
                    print(f"  Rate-limited (attempt {attempt+1}) — sleeping {wait}s")
                    time.sleep(wait)
                    continue
                print(f"  FAIL: {msg[:120]}")
                break

    done = sum(1 for fn, _ in SCENES if (OUT_DIR / fn).exists())
    print(f"\nDone: {done}/{total} images in {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
