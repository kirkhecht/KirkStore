#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Genesis Patriarchs — Image Generation (Scenes 1-218)

Covers Genesis 11-50 from the user's 10-part script:
  Story 1:  The Calling of Abram         (~2000 BC)  scenes 001-018
  Story 2:  The Covenant with God                     scenes 019-034
  Story 3:  The Three Visitors                        scenes 035-046
  Story 4:  Sodom and Gomorrah          (~1900 BC)   scenes 047-064
  Story 5:  The Birth of Isaac                        scenes 065-076
  Story 6:  The Binding of Isaac                      scenes 077-094
  Story 7:  Rebekah — Wife of Isaac                   scenes 095-106
  Story 8:  Jacob and Esau                            scenes 107-126
  Story 9:  Jacob's Dream at Bethel                   scenes 127-136
  Story 10: Jacob — Leah and Rachel                   scenes 137-150
  Story 11: Jacob Wrestles with God                   scenes 151-162
  Story 12: Joseph and His Brothers     (~1900 BC)   scenes 163-180
  Story 13: Joseph in Egypt                           scenes 181-196
  Story 14: Pharaoh's Dreams                          scenes 197-218

Output: project/stories/genesis_patriarchs/NNN_slug.jpg
"""

import os, sys, time, base64, argparse, requests
from pathlib import Path

OUT_DIR = Path("project/stories/genesis_patriarchs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Quality / safety string ────────────────────────────────────────────────────
C = (
    "ultra photorealistic, 8K cinema camera, IMAX cinematic quality, dramatic lighting, "
    "no text overlays no watermarks no subtitles, film grain, anamorphic lens flare, movie still frame, "
    "ancient biblical setting only, no modern elements no modern vehicles no modern clothing "
    "no modern buildings, strictly ancient biblical era"
)

# ── Character descriptors ──────────────────────────────────────────────────────
ABRAM = (
    "Abram: ancient Middle Eastern man in his 70s, long silver-gray beard, "
    "deep weathered dark eyes, dignified wise face, wearing rough ancient woven linen robes, "
    "a wandering patriarch, ancient Mesopotamian setting"
)

ABRAHAM = (
    "Abraham: ancient Middle Eastern man in his 90s-100s, very long silver-white beard, "
    "deeply weathered dark eyes, a face of extraordinary dignity and faith, "
    "wearing rough ancient woven robes, ancient Canaanite highland setting"
)

SARAH = (
    "Sarah: ancient Middle Eastern woman in her 60s-90s, silver-streaked dark hair, "
    "strong wise weathered face, wearing ancient woven linen headscarf and robes, "
    "dignified beauty even in age, ancient Near Eastern setting"
)

SARAI = (
    "Sarai: ancient Middle Eastern woman in her 60s, dark hair streaked with silver, "
    "strong beautiful face, wearing ancient woven linen headscarf and flowing robes, "
    "ancient Mesopotamian setting"
)

LOT = (
    "Lot: ancient Middle Eastern man in his 40s-50s, dark beard, weathered face, "
    "rough ancient linen garments, anxious expression, ancient Canaanite-Jordanian setting"
)

HAGAR = (
    "Hagar: ancient Egyptian woman in her 20s-30s, dark Egyptian features, "
    "wearing simple ancient linen garments, carrying a water skin, "
    "ancient desert setting"
)

ISAAC_BOY = (
    "Isaac: ancient Middle Eastern boy of 12-15 years, dark curly hair, olive skin, "
    "innocent trusting face, wearing simple rough ancient linen garments, "
    "ancient Canaanite highland setting"
)

ISAAC = (
    "Isaac: ancient Middle Eastern young man in his 20s-30s, dark hair, olive skin, "
    "gentle earnest face, wearing rough ancient linen garments, ancient Canaanite setting"
)

REBEKAH = (
    "Rebekah: ancient Middle Eastern young woman in her late teens, dark flowing hair, "
    "olive skin, bright gentle eyes, wearing ancient woven headscarf and linen robes, "
    "a large clay water jar on her shoulder, ancient Near Eastern well setting"
)

JACOB = (
    "Jacob: ancient Middle Eastern man in his 20s-30s, dark hair, smooth olive skin, "
    "bright watchful eyes, wearing rough ancient linen garments, "
    "ancient Canaanite-Mesopotamian setting"
)

ESAU = (
    "Esau: ancient Middle Eastern man in his 20s-30s, reddish-brown thick hair and beard, "
    "rugged weather-beaten face, muscular hunter's build, "
    "wearing rough ancient animal skin garments, bow and arrows, ancient Canaanite setting"
)

LABAN = (
    "Laban: ancient Middle Eastern man in his 40s-50s, dark beard, calculating eyes, "
    "wearing finer ancient Mesopotamian robes than a shepherd, ancient Haran setting"
)

RACHEL = (
    "Rachel: ancient Middle Eastern beautiful young woman, dark flowing hair, "
    "olive skin, bright expressive eyes, wearing ancient linen headscarf and robes, "
    "a shepherdess with a flock, ancient Near Eastern setting"
)

LEAH = (
    "Leah: ancient Middle Eastern young woman, dark hair, gentle but sad eyes, "
    "wearing ancient linen headscarf and robes, "
    "the older sister, ancient Near Eastern Haran setting"
)

JOSEPH_YOUNG = (
    "Joseph: ancient Middle Eastern young man of about 17, handsome with dark curly hair, "
    "bright intelligent eyes, olive skin, wearing an elaborately decorated "
    "ancient coat of many colors — striped and richly dyed in reds and blues and golds, "
    "ancient Canaanite setting"
)

JOSEPH_EGYPT = (
    "Joseph: ancient Middle Eastern man in his early 30s, "
    "dark hair, strong dignified face, wearing fine ancient Egyptian linen garments, "
    "a gold chain and signet ring, second in command of all Egypt, "
    "ancient Egyptian palace setting"
)

JACOB_OLD = (
    "Jacob — now called Israel: ancient Middle Eastern very old man in his 120s-130s, "
    "long white beard, deeply lined wise face, wearing rich ancient robes, "
    "ancient Canaanite-Egyptian setting"
)

BROTHERS = (
    "ten ancient Middle Eastern men, brothers ranging from 20s to 40s, "
    "dark hair, olive skin, rough ancient Canaanite linen garments, "
    "not idealized, ordinary build, ancient Near Eastern setting"
)

PHARAOH_EGYPT = (
    "Pharaoh of ancient Egypt: powerful ruler in traditional royal garments, "
    "linen kilt and collar, gold headband, seated on an elaborate throne, "
    "ancient Egyptian palace court setting"
)

# ── Scene definitions ──────────────────────────────────────────────────────────
# Format: (scene_number, "NNN_slug.jpg", "narration text", "image prompt")
SCENES = [

    # ─── STORY 1: THE CALLING OF ABRAM ──────────────────────────────────────

    (1, "001_abram_in_ur.jpg",
     "His name was Abram.",
     f"Wide cinematic establishing shot: the great ancient city of Ur at dusk — "
     f"its massive stepped ziggurat on the skyline, winding mud-brick streets, "
     f"oil lamps beginning to glow in windows, the grandeur of ancient Sumerian civilization. {C}"),

    (2, "002_city_of_ur.jpg",
     "He lived in Ur of the Chaldeans — one of the greatest cities in the ancient world.",
     f"Aerial-perspective cinematic view of ancient Ur: "
     f"densely packed mud-brick dwellings, the great ziggurat towering above everything, "
     f"the Euphrates river beyond, a thriving ancient Mesopotamian city at sunset. {C}"),

    (3, "003_temples_and_trade.jpg",
     "A city of ziggurats and merchant roads. Of temples and trade.",
     f"Street-level cinematic shot in ancient Ur: a bustling marketplace, "
     f"merchants with clay tablets and woven goods, animals, dust, commerce, "
     f"the ziggurat looming in the background, ancient Sumerian street life. {C}"),

    (4, "004_god_comes_to_abram.jpg",
     "But God came to him there.",
     f"Close-up portrait of {ABRAM} at night, face turned upward, "
     f"a look of sudden awe and attention, moonlight on his weathered features, "
     f"as if hearing something no one else can hear, ancient setting. {C}"),

    (5, "005_the_call_go.jpg",
     "Go. Leave your country, your people, your father's household.",
     f"Wide cinematic shot: {ABRAM} standing at the edge of the ancient city, "
     f"looking out across the open desert beyond the walls, "
     f"the city behind him, the vast unknown ahead, a man at the threshold of departure. {C}"),

    (6, "006_land_i_will_show.jpg",
     "Go to the land I will show you.",
     f"Sweeping cinematic view: an ancient desert plain stretching to a distant mountain range "
     f"under a vast open sky, the promised horizon, "
     f"no people — just the open invitation of the unknown land. {C}"),

    (7, "007_great_nation.jpg",
     "I will make you into a great nation.",
     f"Wide cinematic shot: a vast ancient plain at golden hour, "
     f"with countless small campfires scattered across it to the horizon, "
     f"a vision of a people yet to be born, ancient Near Eastern landscape. {C}"),

    (8, "008_bless_you.jpg",
     "I will bless you. I will make your name great.",
     f"Low-angle cinematic shot: {ABRAM} standing on high rocky ground, "
     f"his silhouette against a vast golden sky, arms slightly raised, "
     f"the weight of a divine promise settling on one man, ancient setting. {C}"),

    (9, "009_blessed_through_you.jpg",
     "And all peoples on earth will be blessed through you.",
     f"Sweeping aerial cinematic view of the ancient world — "
     f"multiple diverse peoples in different terrains, all lit by the same golden light, "
     f"the scope of a promise that reaches to all nations. {C}"),

    (10, "010_abram_did_not_know.jpg",
     "Abram did not know where he was going.",
     f"Wide cinematic shot: a long desert road disappearing into the haze of the horizon, "
     f"the flat Mesopotamian plain stretching endlessly, "
     f"uncertainty and faith captured in an empty road, ancient setting. {C}"),

    (11, "011_but_he_went.jpg",
     "But he went.",
     f"Wide cinematic shot: {ABRAM} leading a procession — camels, servants, flocks — "
     f"away from the walled city of Ur in the early morning, "
     f"the gates behind them, the open desert ahead, a people on the move. {C}"),

    (12, "012_sarai_lot_flocks.jpg",
     "He packed everything — his wife Sarai, his nephew Lot, his flocks and herds and servants.",
     f"Cinematic caravan scene: {SARAI} riding a camel, {LOT} walking beside loaded donkeys, "
     f"servants driving sheep and cattle, all moving through an ancient landscape, "
     f"the family of Abram on the great journey. {C}"),

    (13, "013_they_set_out.jpg",
     "And they set out.",
     f"Wide aerial cinematic view: a caravan of people and animals moving "
     f"across a vast ancient plain — tiny against the landscape — "
     f"heading toward a distant horizon, ancient Mesopotamian-Canaanite route. {C}"),

    (14, "014_across_desert.jpg",
     "Across the desert. Across the rivers. Toward a land they had never seen.",
     f"Three-panel style cinematic image: a vast sun-bleached desert plain, "
     f"a wide ancient river crossing, a green distant hilltop — "
     f"the journey of a lifetime condensed in landscape, ancient Near East. {C}"),

    (15, "015_came_to_canaan.jpg",
     "At last, they came to the land of Canaan.",
     f"Sweeping cinematic view: rolling green Canaanite hills and valleys "
     f"seen from a high vantage point, ancient terraced agriculture, "
     f"the Promised Land seen for the first time, afternoon light. {C}"),

    (16, "016_to_your_offspring.jpg",
     "God appeared to Abram there. 'To your offspring I will give this land.'",
     f"Close-up portrait: {ABRAM} standing in Canaan, "
     f"face turned skyward in a moment of divine encounter, "
     f"the green Canaanite landscape around him, afternoon light on his weathered face. {C}"),

    (17, "017_abram_builds_altar.jpg",
     "Abram built an altar. His first act in the promised land was worship.",
     f"{ABRAM} carefully placing stones for a rough altar in the ancient Canaanite hills, "
     f"kneeling in worship, morning light, the act of gratitude and dedication, "
     f"ancient stone altar with smoke rising, ancient Canaanite landscape. {C}"),

    (18, "018_left_everything.jpg",
     "He had left everything. He would wait to receive everything.",
     f"Wide cinematic shot: {ABRAM} and {SARAI} seated outside their tent at evening, "
     f"the Canaanite hills behind them, campfire light, "
     f"the peace and patience of faith in two aged faces. {C}"),

    # ─── STORY 2: THE COVENANT WITH GOD ─────────────────────────────────────

    (19, "019_years_passed.jpg",
     "Years passed. Abram grew old. The promise seemed impossible.",
     f"Close-up portrait: {ABRAM} — older now, more lined — "
     f"sitting alone at the entrance of his tent at dusk, "
     f"eyes distant, the weight of waiting in his face, ancient Canaanite setting. {C}"),

    (20, "020_sarai_barren.jpg",
     "He had no children. Sarai was barren.",
     f"{SARAI} — older, dignified, deeply sad — seated alone inside an ancient tent, "
     f"hands in her lap, the grief of a woman who has not been given what she most desires, "
     f"ancient Near Eastern interior. {C}"),

    (21, "021_do_not_be_afraid.jpg",
     "But God came to Abram in a vision. 'Do not be afraid. I am your shield.'",
     f"Cinematic vision scene: {ABRAM} kneeling in darkness, "
     f"a beam of otherworldly light falling on him from above, "
     f"his face upturned in awe and wonder, ancient tent interior. {C}"),

    (22, "022_what_can_you_give.jpg",
     "Abram asked — what can you give me, since I have no child?",
     f"Close-up of {ABRAM}'s aged face in firelight, "
     f"the honest grief and confusion of a man whose deepest longing remains unfulfilled, "
     f"the raw honesty of prayer, ancient night setting. {C}"),

    (23, "023_count_the_stars.jpg",
     "God took him outside and said — look at the sky. Count the stars.",
     f"Cinematic upward shot: {ABRAM} standing outside his tent at night, "
     f"head tilted back, gazing at an absolutely vast star-filled sky, "
     f"the Milky Way brilliant above the ancient Canaanite hills, "
     f"one small man before an infinite heaven. {C}"),

    (24, "024_so_shall_your_offspring.jpg",
     "So shall your offspring be.",
     f"Wide cinematic shot: the star-filled night sky seen from an ancient hilltop, "
     f"countless stars blazing in the clear ancient dark, "
     f"a staggering density of light, the promise of a numberless people. {C}"),

    (25, "025_abram_believed.jpg",
     "Abram believed. And God counted it to him as righteousness.",
     f"Close-up portrait: {ABRAM} looking upward with an expression of pure, quiet faith — "
     f"not certainty, but trust — the moment a man chooses to believe the impossible. {C}"),

    (26, "026_god_made_covenant.jpg",
     "Then God made a covenant — a binding promise.",
     f"Wide cinematic shot: a solemn ancient ceremony — "
     f"halved animals laid in two rows on the ground in the ancient Near Eastern way, "
     f"a covenant being prepared at twilight, no human figures — just the solemn arrangement. {C}"),

    (27, "027_animals_cut.jpg",
     "He had Abram cut animals in half and lay them in two rows.",
     f"Close-up cinematic detail: halved animals laid on either side of a path "
     f"in the ancient Canaanite hillside, the weight and formality of an ancient covenant rite, "
     f"fading evening light. {C}"),

    (28, "028_sun_goes_down.jpg",
     "And as the sun went down, Abram fell into a deep, terrifying sleep.",
     f"Wide cinematic shot: {ABRAM} lying on the ground between the animal halves, "
     f"the sun setting in blazing orange behind the hills, "
     f"a deep supernatural sleep overtaking him, ancient hillside. {C}"),

    (29, "029_smoking_firepot.jpg",
     "A smoking firepot. A blazing torch. Moving between the pieces.",
     f"Cinematic supernatural scene: a glowing smoking brazier and a blazing torch "
     f"moving through the darkness between rows of halved animals, "
     f"no human hand holding them — God alone passing through the covenant, "
     f"ancient night, eerie sacred light. {C}"),

    (30, "030_god_passing_through.jpg",
     "God alone passing through — taking the full weight of the promise onto Himself.",
     f"Wide cinematic night shot: the two rows of halved animals, "
     f"divine fire moving between them in the darkness, "
     f"the sacred solemnity of a one-sided oath, ancient Canaanite night. {C}"),

    (31, "031_ninety_nine_years.jpg",
     "When Abram was ninety-nine years old, God appeared again.",
     f"Close-up portrait: {ABRAHAM} — now very old, white-bearded — "
     f"at the entrance of his tent in strong afternoon light, "
     f"looking upward with the patient expectation of a man who has waited decades. {C}"),

    (32, "032_walk_before_me.jpg",
     "I am God Almighty. Walk before me and be blameless.",
     f"{ABRAHAM} prostrate on the ground, face pressed into the ancient Canaanite soil, "
     f"an elderly man in the dust before a holy presence, "
     f"profound humility and worship, ancient setting. {C}"),

    (33, "033_name_abraham.jpg",
     "Your name will no longer be Abram. It will be Abraham — father of many nations.",
     f"Close-up portrait: {ABRAHAM} lifting his face from the ground, "
     f"eyes wide with wonder, a new name settling on him like a mantle, "
     f"the transformation of identity through divine encounter. {C}"),

    (34, "034_sarah_mother_of_nations.jpg",
     "And Sarai — she will be called Sarah. She will become the mother of nations.",
     f"Portrait of {SARAH} — very old, dignified, silver-haired — "
     f"inside her ancient tent, light falling on her strong wise face, "
     f"the improbable grace of a woman chosen for something she cannot yet imagine. {C}"),

    # ─── STORY 3: THE THREE VISITORS ────────────────────────────────────────

    (35, "035_tent_at_mamre.jpg",
     "One day, Abraham was sitting at the entrance of his tent in the heat of the day.",
     f"Wide cinematic shot: {ABRAHAM} sitting in the shade of his tent entrance "
     f"under a great oak tree at Mamre, the midday heat shimmering, "
     f"ancient Canaanite pastoral landscape, quiet and still. {C}"),

    (36, "036_three_strangers.jpg",
     "He looked up — and three strangers were standing before him.",
     f"Cinematic shot: three figures standing in the blazing midday light before Abraham's tent, "
     f"their faces hard to see against the brightness, "
     f"an otherworldly quality to their appearance, ancient setting. {C}"),

    (37, "037_ran_to_meet_them.jpg",
     "He ran to meet them. He bowed low. He begged them to rest and eat.",
     f"{ABRAHAM} hurrying toward the three visitors, bowing deeply in ancient hospitality, "
     f"his aged face animated with welcome, the oak tree shade behind him, "
     f"ancient Canaanite setting. {C}"),

    (38, "038_curds_and_milk.jpg",
     "He killed a calf. He brought curds and milk. He stood beneath a tree while they ate.",
     f"Cinematic meal scene under an ancient oak tree: a simple feast laid out — "
     f"clay bowls of curds and milk, bread, roasted meat — "
     f"the three visitors seated in the shade, {ABRAHAM} standing respectfully nearby, "
     f"ancient hospitality. {C}"),

    (39, "039_where_is_sarah.jpg",
     "Then one of them asked — where is Sarah your wife?",
     f"Close-up: {ABRAHAM} and one of the visitors in conversation, "
     f"the visitor's face composed and knowing, {ABRAHAM}'s expression attentive and wondering, "
     f"ancient Canaanite midday. {C}"),

    (40, "040_she_is_in_the_tent.jpg",
     "She is there. In the tent.",
     f"Cinematic shot of a simple ancient tent in the midday heat, "
     f"the entrance flap slightly open, "
     f"the shadow of a figure visible inside — {SARAH} listening, "
     f"ancient Canaanite setting. {C}"),

    (41, "041_return_next_year.jpg",
     "'I will return to you at this time next year. And your wife Sarah will have a son.'",
     f"Close-up: one of the three visitors speaking with calm certainty, "
     f"a supernatural confidence in his face and voice, "
     f"ancient Canaanite midday, the tent entrance behind him. {C}"),

    (42, "042_sarah_listening.jpg",
     "Sarah was listening at the tent entrance behind them.",
     f"{SARAH} — very old, silver-haired — standing just inside the tent entrance, "
     f"partially hidden by the tent fabric, listening intently, "
     f"her face caught between disbelief and desperate hope. {C}"),

    (43, "043_sarah_ninety.jpg",
     "She was ninety years old.",
     f"Close-up portrait: {SARAH}'s aged face — deeply lined, wise, still beautiful — "
     f"in the shadow of the tent, "
     f"the look of a woman who has waited her entire life for this moment, "
     f"ancient Near Eastern setting. {C}"),

    (44, "044_sarah_laughed.jpg",
     "She laughed to herself.",
     f"Close-up: {SARAH}'s face breaking into a surprised, involuntary laugh, "
     f"hand going to her mouth, eyes wide — the laughter of disbelief "
     f"mixed with something dangerously close to hope. {C}"),

    (45, "045_anything_too_hard.jpg",
     "The Lord asked — why did Sarah laugh? Is anything too hard for the Lord?",
     f"Cinematic two-shot: one of the visitors turned toward the tent, "
     f"his voice penetrating, {SARAH} visible in the background with startled eyes, "
     f"the question that silences all doubt. {C}"),

    (46, "046_yes_you_did.jpg",
     "Sarah said, 'I did not laugh.' But the Lord said — 'Yes, you did.'",
     f"{SARAH} at the tent entrance facing the visitor, "
     f"her face torn between fear and a reluctant smile, "
     f"caught between denial and wonder, ancient Canaanite setting. {C}"),

    # ─── STORY 4: SODOM AND GOMORRAH ────────────────────────────────────────

    (47, "047_men_looked_toward_sodom.jpg",
     "The men rose and looked toward Sodom.",
     f"Wide cinematic shot: three figures standing on a Canaanite hillside "
     f"looking down toward a distant ancient city on a plain, "
     f"the Dead Sea valley visible, a fateful gaze. {C}"),

    (48, "048_abraham_walked_with_them.jpg",
     "Abraham walked with them part of the way.",
     f"{ABRAHAM} walking alongside the three visitors on an ancient path, "
     f"the rocky Canaanite hills around them, "
     f"the gravity of their destination felt in their movement. {C}"),

    (49, "049_shall_i_hide.jpg",
     "And the Lord said — shall I hide from Abraham what I am about to do?",
     f"Close-up portrait: {ABRAHAM} walking, pausing, face turned inward "
     f"as if suddenly aware of something weighty being shared with him, "
     f"the privilege and burden of being chosen. {C}"),

    (50, "050_outcry_against_sodom.jpg",
     "The outcry against Sodom and Gomorrah was great. Their sin was very grave.",
     f"Wide cinematic shot of ancient Sodom at night: a walled city on the Jordan plain, "
     f"fires and noise within, a sense of deep moral darkness, "
     f"ancient city of sin in the Dead Sea valley. {C}"),

    (51, "051_will_you_sweep_away.jpg",
     "Abraham stood before God and asked — will you sweep away the righteous with the wicked?",
     f"{ABRAHAM} standing in prayer on a rocky Canaanite overlook, "
     f"hands raised, head bowed, the posture of a man interceding with all his heart, "
     f"ancient evening sky behind him. {C}"),

    (52, "052_fifty_righteous.jpg",
     "What if there are fifty righteous in the city?",
     f"Close-up of {ABRAHAM}'s face in prayer, deeply earnest, "
     f"the courage of a man negotiating for the lives of others, "
     f"ancient setting, evening light. {C}"),

    (53, "053_god_will_spare.jpg",
     "God said — if I find fifty, I will spare the whole place.",
     f"Wide shot of ancient Canaan at evening, {ABRAHAM} on a hilltop, "
     f"the distant Jordan plain visible below where the cities lie, "
     f"the mystery of divine mercy being negotiated under the open sky. {C}"),

    (54, "054_bargaining.jpg",
     "Abraham bargained — forty-five? Forty? Thirty? Twenty? Ten?",
     f"Close-up portrait: {ABRAHAM}'s face in earnest prayer, "
     f"the intensity of a man pushing the limits of intercession, "
     f"bold love for others radiating from his aged face, ancient setting. {C}"),

    (55, "055_ten_righteous.jpg",
     "God agreed — for the sake of ten, I will not destroy it.",
     f"Wide cinematic shot: the ancient Jordan plain at dusk, "
     f"the twin cities of Sodom and Gomorrah visible in the distance, "
     f"the fragile mercy of ten souls holding back destruction. {C}"),

    (56, "056_angels_at_sodom.jpg",
     "Two angels arrived in Sodom at evening. Lot was sitting in the gateway.",
     f"Cinematic city gate scene: ancient Sodom's massive gate at evening, "
     f"{LOT} sitting nearby, two travelers approaching, "
     f"the first light of oil lamps in the streets behind the gate. {C}"),

    (57, "057_lot_begged.jpg",
     "He begged them to come to his house. They came in. He made them a feast.",
     f"{LOT} welcoming two visitors into his ancient home, "
     f"urgently insisting, a simple ancient interior, clay lamps lit, "
     f"bread and food being prepared, the grace of hospitality. {C}"),

    (58, "058_men_surrounded.jpg",
     "But before they could sleep, the men of the city surrounded Lot's house.",
     f"Exterior of an ancient mud-brick house at night: "
     f"a threatening crowd pressing against the door, torchlight, "
     f"the darkness of mob violence in an ancient city. {C}"),

    (59, "059_angels_struck_blind.jpg",
     "The angels struck the men outside with blindness.",
     f"Cinematic scene: the crowd outside Lot's door suddenly staggering and groping, "
     f"hands reaching uselessly in the torchlight, "
     f"the sudden supernatural incapacitation of an entire mob. {C}"),

    (60, "060_flee_to_escape.jpg",
     "They said to Lot — get your family out. We are about to destroy this place.",
     f"{LOT} inside his ancient home, two visitors standing urgently before him, "
     f"the gravity and terror of the warning on everyone's faces, "
     f"ancient interior lit by clay lamps. {C}"),

    (61, "061_angels_urged_hurry.jpg",
     "At dawn, the angels urged Lot to hurry. 'Flee! And don't look back.'",
     f"Cinematic dawn scene: {LOT} and his family being physically pulled out of Sodom "
     f"by the two visitors, urgency and fear, the ancient city gate behind them, "
     f"the first light of a terrible dawn. {C}"),

    (62, "062_burning_sulfur.jpg",
     "Then the Lord rained burning sulfur on Sodom and Gomorrah.",
     f"Dramatic wide cinematic shot: the ancient cities of the plain "
     f"engulfed in fire and billowing smoke, pillars of fire descending, "
     f"the Jordan plain illuminated by catastrophe, ancient divine judgment. {C}"),

    (63, "063_lots_wife.jpg",
     "Lot's wife looked back. And she became a pillar of salt.",
     f"Wide cinematic shot: a lone figure standing frozen on the plain near Sodom, "
     f"solid white against the dark smoking background, "
     f"the fiery destruction of Sodom visible beyond, ancient Near Eastern landscape. {C}"),

    (64, "064_dense_smoke.jpg",
     "Abraham looked toward Sodom. Dense smoke rose from the land, like smoke from a furnace.",
     f"Wide cinematic shot: {ABRAHAM} standing on the Canaanite hills, "
     f"looking down at the Jordan plain where thick black smoke billows "
     f"from the place where Sodom stood, the morning after destruction. {C}"),

    # ─── STORY 5: THE BIRTH OF ISAAC ────────────────────────────────────────

    (65, "065_god_remembered.jpg",
     "God remembered His promise.",
     f"Wide cinematic shot: a new dawn over the ancient Canaanite hills, "
     f"a bright clear sky, the light of a morning that brings something long-promised, "
     f"ancient Near Eastern landscape. {C}"),

    (66, "066_sarah_conceived.jpg",
     "Sarah conceived. At ninety years old.",
     f"Portrait of {SARAH} — very old, silver-haired — her hands pressed to her heart, "
     f"an expression of pure disbelief and dawning joy, the miracle settling on her, "
     f"ancient tent interior. {C}"),

    (67, "067_bore_a_son.jpg",
     "She bore a son.",
     f"Cinematic scene: {SARAH} resting in an ancient tent, cradling a newborn, "
     f"her aged face radiant with exhausted wonder, "
     f"the impossible gift in her arms, ancient Near Eastern setting. {C}"),

    (68, "068_named_isaac.jpg",
     "Abraham named him Isaac — which means: he laughs.",
     f"{ABRAHAM} — very old, white-bearded — holding a newborn infant, "
     f"his ancient weathered face split in the most genuine smile, "
     f"joy and disbelief and wonder in an old man's eyes. {C}"),

    (69, "069_sarah_said.jpg",
     "Sarah said — God has brought me laughter. Everyone who hears about this will laugh with me.",
     f"Portrait of {SARAH} laughing with genuine joy, "
     f"her aged face transformed by happiness, the laughter that faith finally earns, "
     f"ancient Near Eastern setting. {C}"),

    (70, "070_who_would_have_said.jpg",
     "Who would have said that Sarah would nurse children? Yet I have borne him a son in his old age.",
     f"{SARAH} nursing a baby, her aged face tender and overwhelmed, "
     f"the miracle of late motherhood, ancient tent interior with warm light. {C}"),

    (71, "071_abraham_hundred.jpg",
     "Abraham was one hundred years old when Isaac was born.",
     f"Wide cinematic shot: {ABRAHAM} — ancient, white-bearded — and {SARAH} — "
     f"equally aged — sitting together with a small infant between them, "
     f"ancient Canaanite setting, the improbable family. {C}"),

    (72, "072_trouble_entered.jpg",
     "But not long after, trouble entered the tent.",
     f"Interior of an ancient tent: two women visible, tension in the air, "
     f"a small child playing between them, the shadow of conflict, "
     f"ancient Near Eastern domestic setting. {C}"),

    (73, "073_hagar_son_mocking.jpg",
     "Sarah saw Hagar's son Ishmael mocking Isaac.",
     f"{HAGAR} and a young boy on one side, {SARAH} watching with growing anger, "
     f"the tension of a household divided, ancient Canaanite setting. {C}"),

    (74, "074_send_them_away.jpg",
     "She told Abraham — send that woman and her son away.",
     f"{SARAH} speaking to {ABRAHAM} with fierce resolve, "
     f"her aged face set with determination, the hard necessity of a painful choice. {C}"),

    (75, "075_hard_thing.jpg",
     "It was a hard thing. But God told Abraham — listen to what Sarah says.",
     f"Close-up portrait: {ABRAHAM}'s face showing deep grief — the pain of a father "
     f"being asked to send away a son he loves. {C}"),

    (76, "076_hagar_desert.jpg",
     "Hagar and Ishmael went into the desert. And God was with the boy.",
     f"{HAGAR} walking through a harsh desert landscape with a young boy, "
     f"a water skin nearly empty, the bleached desert around them, "
     f"yet a quality of divine protection in the scene, ancient setting. {C}"),

    # ─── STORY 6: THE BINDING OF ISAAC ──────────────────────────────────────

    (77, "077_god_tested_abraham.jpg",
     "Then God tested Abraham.",
     f"Close-up portrait: {ABRAHAM} at night, face upturned, "
     f"receiving a summons that will cost everything, "
     f"the gravity of divine testing on his aged face. {C}"),

    (78, "078_take_your_son.jpg",
     "Take your son. Your only son. The one you love. Isaac.",
     f"{ABRAHAM} alone in darkness, every word of the command landing like a blow, "
     f"his face absorbing something incomprehensible, ancient tent interior at night. {C}"),

    (79, "079_go_to_moriah.jpg",
     "Go to the region of Moriah and offer him as a burnt offering.",
     f"Wide cinematic shot: the rocky heights of Moriah visible in the distance "
     f"under a vast cold sky, the journey ahead made terrible by what waits at the end. {C}"),

    (80, "080_rose_early.jpg",
     "Abraham rose early in the morning. He saddled his donkey.",
     f"{ABRAHAM} in the pre-dawn dark, tying a load onto a donkey's back, "
     f"quiet efficient movement, the terrible purpose of a man who has decided to obey. {C}"),

    (81, "081_cut_the_wood.jpg",
     "He cut the wood for the offering. He set out with two servants and his son.",
     f"{ABRAHAM} and {ISAAC_BOY} walking together on an ancient path, "
     f"two servants behind them, {ISAAC_BOY} carrying wood, "
     f"the morning light of a day neither fully understands. {C}"),

    (82, "082_third_day_mountain.jpg",
     "On the third day, he looked up and saw the place in the distance.",
     f"Wide cinematic shot: {ABRAHAM} shading his eyes with his hand, "
     f"looking toward a rocky mountain ahead, "
     f"three days of silence behind him, the destination finally visible. {C}"),

    (83, "083_stay_here_with_donkey.jpg",
     "He told his servants — stay here with the donkey. The boy and I will go over there. We will worship. And we will come back.",
     f"{ABRAHAM} speaking to two servants, {ISAAC_BOY} beside him, "
     f"the careful choice of his words — we will come back — "
     f"faith or hope or both, ancient stony path. {C}"),

    (84, "084_wood_on_isaac.jpg",
     "Abraham laid the wood on Isaac. He carried the fire and the knife.",
     f"Wide shot: {ISAAC_BOY} carrying a bundle of wood on his back up a stony path, "
     f"{ABRAHAM} walking beside him with a small fire and a knife, "
     f"the image heavy with what it foreshadows. {C}"),

    (85, "085_isaac_said_father.jpg",
     "Isaac said — Father?",
     f"Close-up portrait: {ISAAC_BOY} looking up at his father with innocent questioning eyes, "
     f"the simple trust of a son, the wood heavy on his back, ancient stony hillside. {C}"),

    (86, "086_abraham_answered.jpg",
     "Abraham answered — Yes, my son?",
     f"Close-up portrait: {ABRAHAM}'s face turning to his son, "
     f"love and grief and resolve all present at once, "
     f"the most painful yes a father ever spoke. {C}"),

    (87, "087_where_is_the_lamb.jpg",
     "The fire and the wood are here. But where is the lamb?",
     f"Cinematic two-shot: {ISAAC_BOY} and {ABRAHAM} walking together, "
     f"the boy looking up in innocent curiosity, "
     f"his father's face carrying a secret too heavy to share, ancient path. {C}"),

    (88, "088_god_will_provide.jpg",
     "Abraham said — God will provide the lamb, my son.",
     f"Close-up: {ABRAHAM} placing his hand on {ISAAC_BOY}'s shoulder as they walk, "
     f"the four most faithful words ever spoken, "
     f"both their faces turned toward the mountain ahead. {C}"),

    (89, "089_went_on_together.jpg",
     "And the two of them went on together.",
     f"Wide cinematic shot: {ABRAHAM} and {ISAAC_BOY} — small figures — "
     f"walking up a stony mountain path together, "
     f"the ancient landscape around them, moving toward the summit. {C}"),

    (90, "090_built_the_altar.jpg",
     "Abraham built the altar. He bound his son. He laid him on the wood.",
     f"Wide cinematic shot: a rough stone altar on a rocky Canaanite summit, "
     f"wood arranged, {ISAAC_BOY} lying bound on top, "
     f"{ABRAHAM} standing beside it in prayer, ancient stony hilltop. {C}"),

    (91, "091_raised_the_knife.jpg",
     "He raised the knife.",
     f"Close-up of an aged ancient hand holding a stone knife raised above an altar, "
     f"the stillness before the most terrible moment, "
     f"the faith that goes beyond all human understanding. {C}"),

    (92, "092_angel_called.jpg",
     "Then the angel called — Abraham! Abraham! Do not harm the boy.",
     f"{ABRAHAM} at the altar, arm raised, frozen — "
     f"a sudden look of electrified relief breaking across his face, "
     f"a voice stopping everything. {C}"),

    (93, "093_ram_in_thicket.jpg",
     "Abraham looked — and saw a ram caught in the thicket.",
     f"Cinematic detail shot: a brown ram's horns tangled in a dense thornbush "
     f"on the rocky summit of Moriah, the animal struggling gently, "
     f"the provided sacrifice, ancient stony hilltop. {C}"),

    (94, "094_lord_will_provide.jpg",
     "He called that place — The Lord Will Provide. And so the saying arose.",
     f"Wide cinematic shot: {ABRAHAM} and {ISAAC_BOY} descending the mountain together, "
     f"smoke from the altar visible behind them, "
     f"a column of smoke rising toward heaven, the valley below, ancient setting. {C}"),

    # ─── STORY 7: REBEKAH — WIFE OF ISAAC ───────────────────────────────────

    (95, "095_sarah_died.jpg",
     "Sarah died at one hundred and twenty-seven years old. Abraham mourned deeply for her.",
     f"{ABRAHAM} kneeling beside an ancient stone burial cave, "
     f"head bowed in deep grief, his silver-white hair and robes, "
     f"the Canaanite hills around the burial site at Machpelah. {C}"),

    (96, "096_cave_of_machpelah.jpg",
     "He bought a field and a cave from the Hittites at Machpelah to bury her.",
     f"Cinematic shot of an ancient Canaanite cave entrance in a rocky hillside, "
     f"a stone door, the gravity of a burial place purchased with silver, "
     f"the permanence of grief made tangible. {C}"),

    (97, "097_swear_to_me.jpg",
     "Then Abraham called his oldest servant. 'Swear you will not get a wife for my son from the Canaanites.'",
     f"{ABRAHAM} — very old — speaking to a trusted servant, "
     f"the servant's hand beneath Abraham's thigh in the ancient oath posture, "
     f"the solemn weight of a deathbed commission. {C}"),

    (98, "098_go_to_my_homeland.jpg",
     "You will go to my homeland. And find a wife for Isaac from among my own people.",
     f"Wide cinematic shot: a servant loading ten camels with gifts — "
     f"gold and silver jewelry in panniers, fine cloth, "
     f"the preparation for a great journey, ancient Canaanite setting. {C}"),

    (99, "099_ten_camels.jpg",
     "The servant set out with ten camels loaded with gifts.",
     f"Wide cinematic shot: a caravan of ten camels moving through an ancient landscape, "
     f"the dust of the journey, the far Mesopotamian horizon ahead, "
     f"a servant on a mission of love. {C}"),

    (100, "100_well_of_nahor.jpg",
     "At a well outside the city of Nahor, he stopped and prayed.",
     f"Cinematic scene: a servant kneeling beside an ancient stone well at the edge of a city, "
     f"the camels resting behind him, the city gate visible ahead, "
     f"a man in earnest prayer at a pivotal moment. {C}"),

    (101, "101_the_prayer.jpg",
     "Let the girl who gives water to my camels be the one you have chosen for Isaac.",
     f"Close-up: a man's face in quiet, intense prayer at an ancient well, "
     f"the specific and bold request of a servant who trusts God, "
     f"the ancient stone well beside him. {C}"),

    (102, "102_rebekah_approaches.jpg",
     "Before he had finished praying — Rebekah came out with a jar on her shoulder.",
     f"{REBEKAH} approaching an ancient stone well, "
     f"a large clay water jar balanced on her shoulder, "
     f"moving with grace and purpose, the city of Nahor behind her, ancient Mesopotamian setting. {C}"),

    (103, "103_she_watered_camels.jpg",
     "She gave him water. Then she watered all ten camels — without being asked.",
     f"Cinematic action shot: {REBEKAH} pouring water from her clay jar "
     f"into a stone trough for camels, running back and forth with energy and generosity, "
     f"the servant watching in silent wonder, ancient stone well setting. {C}"),

    (104, "104_servant_bowed.jpg",
     "The servant bowed his head and worshiped the Lord.",
     f"Close-up: an aged man's face at an ancient well, "
     f"head bowed, tears of gratitude and wonder, "
     f"the instant recognition of an answered prayer. {C}"),

    (105, "105_this_is_from_the_lord.jpg",
     "He went to her family. He told them everything. And they said — this is from the Lord.",
     f"Interior of an ancient Mesopotamian home: the servant speaking, "
     f"{REBEKAH}'s family listening with growing wonder, "
     f"Rebekah sitting nearby, the arranged blessing being received. {C}"),

    (106, "106_isaac_loved_her.jpg",
     "Isaac saw her coming from a distance. He married her. He loved her.",
     f"Wide romantic cinematic shot: {ISAAC} in a Canaanite field at evening, "
     f"seeing {REBEKAH} for the first time as she approaches on a camel, "
     f"the sunset light, the beginning of a love story. {C}"),

    # ─── STORY 8: JACOB AND ESAU ────────────────────────────────────────────

    (107, "107_two_sons.jpg",
     "Isaac and Rebekah had two sons.",
     f"Cinematic shot of {ISAAC} and {REBEKAH} — now in their 40s — "
     f"looking at twin infants in their home, wonder and love in their faces, "
     f"ancient Canaanite interior. {C}"),

    (108, "108_esau_red_hairy.jpg",
     "The first came out red and hairy — they named him Esau.",
     f"Portrait of {ESAU} as a young man: reddish-brown thick hair, rugged tanned face, "
     f"the physicality of a natural hunter, ancient Canaanite setting. {C}"),

    (109, "109_jacob_grasping_heel.jpg",
     "The second came out grasping Esau's heel — they named him Jacob.",
     f"Portrait of {JACOB} as a young man: smooth dark hair, watchful intelligent eyes, "
     f"olive skin, a quieter intensity than his brother, ancient Canaanite setting. {C}"),

    (110, "110_esau_hunter.jpg",
     "Esau was a skillful hunter. A man of the open country.",
     f"{ESAU} in the ancient Canaanite wilderness: "
     f"bow in hand, crouching near rocks, tracking prey, "
     f"the confidence of a man in his natural element. {C}"),

    (111, "111_jacob_stayed_tents.jpg",
     "Jacob was a quiet man. He stayed among the tents.",
     f"{JACOB} inside or near ancient tents, "
     f"a more reflective posture, perhaps tending a fire or watching the horizon, "
     f"the contrast of a man who lives by observation, ancient pastoral setting. {C}"),

    (112, "112_isaac_loved_esau.jpg",
     "Isaac loved Esau. Rebekah loved Jacob.",
     f"Cinematic family scene: {ISAAC} and {ESAU} together outside, "
     f"sharing a meal from the hunt, {REBEKAH} and {JACOB} visible together at a distance, "
     f"the divided family, ancient Canaanite setting. {C}"),

    (113, "113_esau_came_in_exhausted.jpg",
     "One day, Esau came in from the fields exhausted. Jacob was cooking stew.",
     f"{ESAU} entering an ancient campsite, his hunting bow on his back, "
     f"visibly exhausted and hungry, {JACOB} stirring a pot over a fire, "
     f"the rich smell of red lentil stew in the air. {C}"),

    (114, "114_give_me_the_stew.jpg",
     "Esau said — give me some of that red stew. I'm starving.",
     f"Close-up: {ESAU}'s face — ravenous, demanding — leaning over the fire toward {JACOB}, "
     f"the stew in the clay pot between them, the moment of temptation. {C}"),

    (115, "115_sell_me_your_birthright.jpg",
     "Jacob said — sell me your birthright first.",
     f"Cinematic two-shot: {JACOB} looking at {ESAU} with calm, calculating eyes "
     f"across the fire, the ladle in his hand, the negotiation beginning. {C}"),

    (116, "116_what_good_is_birthright.jpg",
     "Esau said — what good is my birthright if I die of hunger?",
     f"Close-up of {ESAU}'s face: impatient, dismissive, his hunger overtaking all prudence, "
     f"the look of a man who lives for the moment. {C}"),

    (117, "117_sold_for_stew.jpg",
     "He sold his birthright for a bowl of stew.",
     f"Cinematic close-up: {ESAU} eating hungrily from a clay bowl of dark red stew, "
     f"{JACOB} watching quietly, the weight of what just happened settling on the scene, "
     f"ancient campfire. {C}"),

    (118, "118_isaac_old_eyes_dim.jpg",
     "Years passed. Isaac grew old and his eyes grew dim.",
     f"Portrait of {ISAAC} in old age: deeply lined face, clouded eyes, "
     f"the dignified frailty of great age, seated in an ancient interior. {C}"),

    (119, "119_isaac_calls_esau.jpg",
     "He called Esau — go hunt and make me a meal. Before I die, I will give you my blessing.",
     f"Interior scene: old {ISAAC} lying on his bed speaking to {ESAU}, "
     f"the urgency of a dying man arranging his affairs, "
     f"the weight of a father's blessing about to be given, ancient interior. {C}"),

    (120, "120_rebekah_overheard.jpg",
     "Rebekah overheard. She told Jacob — listen to what I say.",
     f"{REBEKAH} — middle-aged, intense — speaking urgently in low tones to {JACOB}, "
     f"her face determined, the plan already forming in her mind, "
     f"ancient tent interior. {C}"),

    (121, "121_jacob_disguised.jpg",
     "She dressed Jacob in Esau's clothes. She put goatskin on his hands and neck.",
     f"{REBEKAH} carefully draping goatskin pieces on {JACOB}'s smooth hands and neck, "
     f"Esau's hunting garments on him, the deception taking shape, "
     f"ancient tent interior. {C}"),

    (122, "122_i_am_esau.jpg",
     "Jacob went to his blind father. 'I am Esau your firstborn.'",
     f"{JACOB} kneeling before old blind {ISAAC} in his dimly lit room, "
     f"the false words spoken, ancient interior, oil lamps. {C}"),

    (123, "123_voice_is_jacobs.jpg",
     "Isaac said — the voice is Jacob's. But the hands are Esau's.",
     f"Close-up: old blind {ISAAC}'s hands reaching out to feel {JACOB}'s goatskin-covered hands, "
     f"the confusion between what he hears and what he feels, ancient interior. {C}"),

    (124, "124_isaac_blessed_jacob.jpg",
     "He was deceived. He blessed Jacob with Esau's blessing.",
     f"Old blind {ISAAC} placing both hands on {JACOB}'s head in solemn blessing, "
     f"his face earnest and trusting, unaware of the deception, ancient interior. {C}"),

    (125, "125_esau_discovered.jpg",
     "Esau came in — and discovered it too late.",
     f"{ESAU} entering his father's room with fresh game, "
     f"his face changing from anticipation to horrified disbelief, "
     f"old blind Isaac's face turning with dread, ancient interior. {C}"),

    (126, "126_esau_wept.jpg",
     "He wept. He raged. He said — my brother has stolen from me twice.",
     f"Close-up portrait: {ESAU}'s face contorted with anguish and fury, "
     f"tears running through his rough beard, "
     f"the grief of a man who has lost everything through one moment of hunger "
     f"and one act of betrayal. {C}"),

    # ─── STORY 9: JACOB'S DREAM AT BETHEL ───────────────────────────────────

    (127, "127_esau_hated_jacob.jpg",
     "Esau hated Jacob for what he had done. He planned to kill him.",
     f"{ESAU} alone on a Canaanite hillside, his face dark with murderous anger, "
     f"looking out over the landscape with cold fury, "
     f"a man consumed by vengeance. {C}"),

    (128, "128_flee_to_haran.jpg",
     "Rebekah warned Jacob — flee to my brother Laban in Haran.",
     f"{REBEKAH} speaking urgently to {JACOB}, both faces close, "
     f"the mother protecting her son, desperation and love in her face, "
     f"ancient tent interior. {C}"),

    (129, "129_jacob_left_alone.jpg",
     "Jacob left with nothing but his staff.",
     f"Wide cinematic shot: {JACOB} — alone — walking away from the family tents "
     f"on an ancient path, a single wooden staff in his hand, "
     f"everything behind him, nothing before him. {C}"),

    (130, "130_stone_under_head.jpg",
     "That night, he lay down on the ground, a stone under his head.",
     f"{JACOB} lying on bare ground in the open countryside, "
     f"a flat stone beneath his head for a pillow, "
     f"the vulnerability of a fugitive sleeping under the stars, ancient Canaanite landscape. {C}"),

    (131, "131_jacobs_ladder.jpg",
     "He dreamed. A stairway reaching from earth to heaven. Angels ascending and descending.",
     f"Dramatic cinematic dream scene: a vast shimmering stairway or ramp of light "
     f"rising from the rocky ground into the clouds, "
     f"luminous figures moving upon it in both directions, "
     f"the earth and heaven connected, ancient landscape at night. {C}"),

    (132, "132_i_am_the_god.jpg",
     "The Lord stood above it and said — I am the God of Abraham and Isaac.",
     f"Wide cinematic view from the base of the divine stairway looking up: "
     f"the structure rising into brilliant heavenly light, "
     f"a sense of the divine presence at the top, ancient night setting. {C}"),

    (133, "133_land_i_give_you.jpg",
     "The land you lie on — I give to you and your descendants.",
     f"Wide cinematic shot of the Canaanite landscape at night: "
     f"hills and valleys stretching to the horizon, "
     f"starlight and the promise of inheritance, ancient Near Eastern setting. {C}"),

    (134, "134_i_will_be_with_you.jpg",
     "And I will be with you wherever you go.",
     f"Close-up of {JACOB} sleeping on the ground, his face at peace in the dream, "
     f"the stone beneath his head, "
     f"a solitary man wrapped in divine promise and starlight. {C}"),

    (135, "135_jacob_woke_in_awe.jpg",
     "Jacob woke in awe. 'Surely the Lord is in this place. How awesome is this place.'",
     f"{JACOB} sitting up suddenly, gasping, face wide-eyed with holy terror and wonder, "
     f"the plain around him completely ordinary, yet charged with the sacred, "
     f"ancient dawn light. {C}"),

    (136, "136_bethel.jpg",
     "He set the stone upright as a pillar and poured oil over it. He called the place Bethel — House of God.",
     f"{JACOB} standing the flat stone upright as a pillar, "
     f"pouring oil over the top, the act of consecration, "
     f"the ancient Canaanite landscape around him, morning light, the place named forever. {C}"),

    # ─── STORY 10: JACOB — LEAH AND RACHEL ──────────────────────────────────

    (137, "137_land_of_the_east.jpg",
     "Jacob arrived in the land of the east.",
     f"Wide cinematic establishing shot: the ancient Mesopotamian plain near Haran, "
     f"rolling hills, a town visible in the distance, "
     f"{JACOB} arriving as a solitary traveler, ancient setting. {C}"),

    (138, "138_well_with_shepherds.jpg",
     "He came to a well. Shepherds were gathered there, waiting to water their flocks.",
     f"Cinematic scene at an ancient stone well: several shepherds with their flocks waiting, "
     f"the flat Mesopotamian landscape around the well, "
     f"ancient pastoral life near Haran. {C}"),

    (139, "139_rachel_approaches.jpg",
     "A beautiful young woman approached with her father's sheep.",
     f"{RACHEL} approaching the ancient well with a flock of white sheep, "
     f"her dark hair under a headscarf, a long staff in her hand, "
     f"the classic image of ancient pastoral beauty, afternoon light. {C}"),

    (140, "140_daughter_of_laban.jpg",
     "Her name was Rachel. She was the daughter of Laban — his mother's brother.",
     f"Portrait of {RACHEL} at the well: dark eyes bright with intelligence and life, "
     f"her headscarf and robes, a beautiful young shepherdess in ancient Haran. {C}"),

    (141, "141_jacob_kissed_rachel.jpg",
     "Jacob kissed Rachel and wept.",
     f"{JACOB} at the ancient well, meeting {RACHEL}, "
     f"his face overcome with emotion — the tears of a man who has found family "
     f"after a long lonely road. {C}"),

    (142, "142_work_for_laban.jpg",
     "He worked for Laban for a month. Then Laban asked — what shall I pay you?",
     f"{LABAN} and {JACOB} in conversation in an ancient Mesopotamian courtyard, "
     f"the negotiation of a wage, ancient Haran setting. {C}"),

    (143, "143_seven_years_for_rachel.jpg",
     "Jacob said — I will serve you seven years for Rachel, your younger daughter.",
     f"Cinematic two-shot: {JACOB} and {LABAN} — the bold proposal spoken, "
     f"{LABAN} with a calculating expression, {JACOB} with determined love. {C}"),

    (144, "144_seemed_few_days.jpg",
     "The seven years seemed like only a few days to him, because he loved her.",
     f"Pastoral cinematic montage: {JACOB} working in the fields, tending sheep, "
     f"seasons changing, {RACHEL} visible nearby — "
     f"love making time fly, ancient Mesopotamian pastoral setting. {C}"),

    (145, "145_wedding_night_deceived.jpg",
     "But on the wedding night, Laban deceived him — and gave him Leah, the older daughter, instead.",
     f"Cinematic scene: a heavily veiled ancient bride being brought into a tent, "
     f"the deception of the wedding night, firelight and shadows, ancient Haran setting. {C}"),

    (146, "146_in_morning_saw_leah.jpg",
     "In the morning, Jacob saw it was Leah. He went to Laban — what have you done to me?",
     f"{JACOB} confronting {LABAN} in anger and disbelief, "
     f"{LEAH} visible nearby with sad eyes, "
     f"the rage of a man who has been deceived with his own weapon. {C}"),

    (147, "147_older_before_younger.jpg",
     "Laban said — in our country, we do not give the younger daughter before the firstborn.",
     f"{LABAN} speaking to {JACOB} with maddening calm and reasonableness, "
     f"the calculated justification of a deceiver, ancient courtyard. {C}"),

    (148, "148_seven_more_years.jpg",
     "Finish this week — and I will give you Rachel as well. For seven more years of work.",
     f"{LABAN} making his new offer to {JACOB}, "
     f"who stands trapped but still determined, "
     f"the price of love doubled, ancient Haran setting. {C}"),

    (149, "149_jacob_loved_rachel.jpg",
     "Jacob agreed. He loved Rachel. He served seven more years.",
     f"{JACOB} and {RACHEL} together in a pastoral setting, "
     f"the quiet endurance of love deferred, ancient Mesopotamian landscape. {C}"),

    (150, "150_twelve_tribes.jpg",
     "From Jacob and his wives, twelve sons were born — the twelve tribes of Israel.",
     f"Wide cinematic shot: {JACOB} — older — surrounded by a large family "
     f"of women and children in an ancient pastoral camp, "
     f"the abundance of a promised people, ancient Mesopotamian setting. {C}"),

    # ─── STORY 11: JACOB WRESTLES WITH GOD ──────────────────────────────────

    (151, "151_return_to_canaan.jpg",
     "After twenty years, God told Jacob — return to the land of your fathers.",
     f"{JACOB} — now middle-aged, more weathered — looking toward the south, "
     f"the direction of Canaan, ancient Mesopotamian landscape. {C}"),

    (152, "152_jacob_set_out.jpg",
     "Jacob set out with his wives, his children, his flocks, his herds, his servants.",
     f"Wide cinematic caravan shot: a vast procession of people, camels, cattle, and sheep "
     f"moving across an ancient landscape, "
     f"the family of Jacob on the move toward Canaan. {C}"),

    (153, "153_esau_four_hundred.jpg",
     "But he was afraid. Esau was coming to meet him with four hundred men.",
     f"Wide cinematic shot: a large column of ancient men moving across a Canaanite plain, "
     f"dust rising from their movement, "
     f"the advance of a force that could mean war or peace, ancient setting. {C}"),

    (154, "154_divided_into_two.jpg",
     "Jacob divided his people and animals into two groups — if Esau attacks one, the other may escape.",
     f"{JACOB} directing servants, flocks being separated into two large groups moving apart, "
     f"the anxious preparation of a man who fears the worst, ancient landscape. {C}"),

    (155, "155_left_alone.jpg",
     "He sent everything ahead and was left alone.",
     f"Wide cinematic shot: {JACOB} standing alone on the bank of an ancient river "
     f"at night — the Jabbok — everything and everyone gone ahead, "
     f"total solitude in the dark, the sound of water. {C}"),

    (156, "156_man_wrestled.jpg",
     "A man wrestled with him until the breaking of the day.",
     f"Dramatic cinematic scene: {JACOB} locked in combat with a mysterious figure "
     f"in the pre-dawn darkness beside an ancient river, "
     f"both figures evenly matched, intense and wordless struggle, ancient riverbank. {C}"),

    (157, "157_touched_hip.jpg",
     "When the man saw that he could not overpower him, he touched Jacob's hip — and wrenched it.",
     f"Cinematic moment: the mysterious figure's hand touching {JACOB}'s hip "
     f"at the moment of the wrenching, {JACOB} wincing and staggering "
     f"but refusing to let go, ancient riverbank at night. {C}"),

    (158, "158_let_me_go.jpg",
     "The man said — let me go. The day is breaking.",
     f"Cinematic close-up of the struggle: two figures locked together at the riverbank, "
     f"the first gray light beginning to appear on the horizon, "
     f"the mysterious urgency to leave before dawn. {C}"),

    (159, "159_i_will_not_let_go.jpg",
     "Jacob said — I will not let you go unless you bless me.",
     f"Close-up portrait: {JACOB}'s face in the gray pre-dawn light, "
     f"exhausted and limping but gripping with total determination, "
     f"the most important request of his life. {C}"),

    (160, "160_what_is_your_name.jpg",
     "The man asked — what is your name?",
     f"Cinematic two-shot in the pre-dawn gray: the mysterious figure and {JACOB}, "
     f"the question hanging between them with all its weight, "
     f"ancient riverbank, first light. {C}"),

    (161, "161_jacob_answered.jpg",
     "Jacob answered. And the man said — your name will no longer be Jacob.",
     f"Close-up: {JACOB}'s face as he speaks his name — and then receives a new one — "
     f"the transformation written on his face, ancient riverbank dawn. {C}"),

    (162, "162_name_is_israel.jpg",
     "It will be Israel — for you have striven with God and with men — and you have prevailed.",
     f"Wide cinematic dawn shot: {JACOB} — now limping — "
     f"standing alone at the Jabbok river as the sun rises, "
     f"transformed, wounded, renamed, the light of a new day falling on a new man. {C}"),

    # ─── STORY 12: JOSEPH AND HIS BROTHERS ──────────────────────────────────

    (163, "163_jacob_settled_canaan.jpg",
     "Jacob settled in the land of Canaan.",
     f"Wide cinematic shot of the ancient Canaanite landscape: "
     f"rolling hills, ancient tents and simple stone dwellings, "
     f"the settled pastoral life of the family of Israel. {C}"),

    (164, "164_twelve_sons.jpg",
     "He had twelve sons. But one he loved more than all the others.",
     f"Cinematic group shot: {JACOB_OLD} with his large family around him, "
     f"sons of various ages, one younger son standing out near his father, "
     f"ancient Canaanite pastoral setting. {C}"),

    (165, "165_his_name_was_joseph.jpg",
     "His name was Joseph.",
     f"Close-up portrait of {JOSEPH_YOUNG}: "
     f"handsome dark-haired face, bright intelligent eyes, olive skin, "
     f"a young man of about seventeen, ancient Canaanite setting. {C}"),

    (166, "166_coat_of_many_colors.jpg",
     "Jacob made him a beautiful robe — a coat of many colors.",
     f"{JOSEPH_YOUNG} wearing an elaborate ancient coat — "
     f"richly colored stripes in deep reds, blues, and golds, woven fine cloth — "
     f"the garment of special favor, ancient Canaanite setting. {C}"),

    (167, "167_brothers_hated_him.jpg",
     "When Joseph's brothers saw that their father loved him more, they hated him.",
     f"Cinematic group shot: {BROTHERS} watching {JOSEPH_YOUNG} from a distance, "
     f"their faces dark with jealousy and resentment, "
     f"the destructive power of favoritism. {C}"),

    (168, "168_could_not_speak.jpg",
     "They could not speak a kind word to him.",
     f"Cinematic scene: {JOSEPH_YOUNG} approaching a group of his {BROTHERS}, "
     f"who turn away or look at him with cold contempt, "
     f"the isolation of the favored child, ancient pastoral setting. {C}"),

    (169, "169_joseph_dreamed.jpg",
     "Joseph dreamed a dream and told his brothers.",
     f"{JOSEPH_YOUNG} speaking animatedly to his {BROTHERS}, "
     f"who are listening with growing displeasure, "
     f"a young man who cannot read the room. {C}"),

    (170, "170_sheaves_bowing.jpg",
     "We were binding sheaves in the field. My sheaf rose and stood upright. And your sheaves gathered around and bowed down to mine.",
     f"Cinematic dream scene: an ancient grain field, "
     f"eleven sheaves of grain bowing toward a central upright sheaf, "
     f"the golden light of dream logic, symbolic and vivid. {C}"),

    (171, "171_do_you_intend_to_reign.jpg",
     "His brothers said — do you intend to reign over us?",
     f"Close-up of the {BROTHERS}' faces: anger, mockery, and contempt "
     f"directed at {JOSEPH_YOUNG}, the question a challenge and a threat. {C}"),

    (172, "172_second_dream.jpg",
     "He dreamed again. The sun and moon and eleven stars were bowing down to me.",
     f"Cinematic night dream scene: an ancient sky with the sun, moon, "
     f"and eleven bright stars arranged in a semi-circle, all bowing toward one star, "
     f"the second prophetic dream, ancient night sky. {C}"),

    (173, "173_even_father_rebuked.jpg",
     "Even his father rebuked him — what is this dream? Shall I and your mother and brothers all bow down to you?",
     f"{JACOB_OLD} looking sternly at {JOSEPH_YOUNG}, "
     f"the rare rebuke from a father who usually shows only favor, "
     f"the {BROTHERS} watching with vindicated satisfaction. {C}"),

    (174, "174_jacob_sent_joseph.jpg",
     "One day, the brothers were tending flocks far from home. Jacob sent Joseph to check on them.",
     f"Wide cinematic shot: {JOSEPH_YOUNG} walking alone across an open ancient landscape, "
     f"his colorful coat visible from a distance, heading toward the hills, "
     f"ancient Canaanite pastoral setting. {C}"),

    (175, "175_here_comes_the_dreamer.jpg",
     "They saw him coming from a distance. They said — here comes the dreamer.",
     f"The {BROTHERS} standing on a hill watching a distant figure approaching, "
     f"their expressions shifting from indifference to dark intent, "
     f"the dangerous gathering of conspirators. {C}"),

    (176, "176_lets_kill_him.jpg",
     "Let's kill him and throw him into a pit.",
     f"Close-up of the {BROTHERS}' faces in a huddle, "
     f"voices low, the conspiracy forming on their faces, "
     f"the cold decision of men who have let jealousy rot to murderous intent. {C}"),

    (177, "177_reuben_said_no.jpg",
     "Reuben — the oldest — said no. Throw him in the pit but do not kill him. He planned to rescue Joseph later.",
     f"The eldest among the {BROTHERS} speaking with urgency, "
     f"restraining the others, his face torn between family loyalty and moral courage. {C}"),

    (178, "178_stripped_and_pit.jpg",
     "They stripped Joseph of his beautiful coat. They threw him in the pit.",
     f"Dramatic cinematic scene: {JOSEPH_YOUNG}'s coat of many colors "
     f"lying on the rocky ground beside a dark pit, "
     f"the silence of a terrible act just done, ancient Canaanite landscape. {C}"),

    (179, "179_sold_to_traders.jpg",
     "A caravan of Ishmaelite traders passed by. The brothers sold Joseph for twenty pieces of silver.",
     f"Wide cinematic shot: traders with camels on an ancient trade route, "
     f"{JOSEPH_YOUNG} being handed over, silver coins changing hands, "
     f"his {BROTHERS} watching from a distance, ancient Canaanite landscape. {C}"),

    (180, "180_jacob_wept.jpg",
     "They dipped his coat in goat's blood and took it back to their father. Jacob wept for years.",
     f"{JACOB_OLD} holding the bloodied coat of many colors, "
     f"his face destroyed by grief, his sons around him, "
     f"the cruelty of calculated deception, ancient tent interior. {C}"),

    # ─── STORY 13: JOSEPH IN EGYPT ──────────────────────────────────────────

    (181, "181_traders_to_egypt.jpg",
     "The traders brought Joseph down to Egypt.",
     f"Wide cinematic shot: the Ishmaelite caravan approaching ancient Egypt — "
     f"the Nile valley visible, palm trees, the flat Egyptian landscape, "
     f"the great delta at horizon. {C}"),

    (182, "182_sold_to_potiphar.jpg",
     "He was sold to Potiphar — an officer of Pharaoh, captain of the guard.",
     f"Cinematic scene in an ancient Egyptian courtyard: "
     f"{JOSEPH_YOUNG} being presented to a powerful Egyptian official, "
     f"the fine Egyptian architecture around them, ancient Egyptian setting. {C}"),

    (183, "183_lord_with_joseph.jpg",
     "The Lord was with Joseph. Everything he touched prospered.",
     f"{JOSEPH_EGYPT} in an Egyptian household: "
     f"managing accounts on papyrus, overseeing servants, "
     f"an aura of competence and favor about him, ancient Egyptian interior. {C}"),

    (184, "184_potiphar_noticed.jpg",
     "Potiphar noticed — this Hebrew's god is with him.",
     f"Potiphar — an Egyptian official in fine linen — watching {JOSEPH_EGYPT} "
     f"with an expression of respect and recognition, "
     f"ancient Egyptian courtyard setting. {C}"),

    (185, "185_put_joseph_in_charge.jpg",
     "He put Joseph in charge of his entire household.",
     f"{JOSEPH_EGYPT} overseeing a large Egyptian estate — "
     f"servants, grain stores, accounts — "
     f"the authority of a trusted steward, ancient Egyptian setting. {C}"),

    (186, "186_potiphars_wife.jpg",
     "But Potiphar's wife noticed Joseph. He was handsome and well-built.",
     f"Cinematic scene in an Egyptian interior: "
     f"a wealthy Egyptian woman watching {JOSEPH_EGYPT} from across a colonnaded courtyard, "
     f"her intent unmistakable, ancient Egyptian palace setting. {C}"),

    (187, "187_come_to_bed.jpg",
     "She said — come to bed with me.",
     f"Close-up: an Egyptian woman speaking to {JOSEPH_EGYPT} with bold confidence, "
     f"the request hanging between them in a fine ancient Egyptian room. {C}"),

    (188, "188_joseph_refused.jpg",
     "Joseph refused. Day after day. He would not sin against his master. He would not sin against God.",
     f"Close-up portrait: {JOSEPH_EGYPT}'s face — firm, dignified, resolute — "
     f"turning away, the moral courage of a man who knows what he owes to God. {C}"),

    (189, "189_she_grabbed_cloak.jpg",
     "One day she grabbed his cloak. He fled and left his cloak in her hand.",
     f"Dramatic cinematic moment: an ancient Egyptian room, "
     f"a woman's hand holding a piece of fine linen cloth, "
     f"a running figure disappearing through the doorway, "
     f"the cloak left behind. {C}"),

    (190, "190_she_lied.jpg",
     "She told her husband — the Hebrew slave tried to attack me.",
     f"Egyptian woman with the cloak in her hand, "
     f"speaking to Potiphar with false distress, "
     f"the lie perfectly constructed, ancient Egyptian interior. {C}"),

    (191, "191_thrown_in_prison.jpg",
     "Potiphar was furious. He threw Joseph in prison.",
     f"Cinematic shot: the entrance to an ancient Egyptian prison — "
     f"heavy stone walls, a door closing, "
     f"the darkness of confinement, {JOSEPH_EGYPT} led inside. {C}"),

    (192, "192_lord_with_joseph_prison.jpg",
     "But the Lord was with Joseph — even in prison. The warden put Joseph in charge of everything.",
     f"{JOSEPH_EGYPT} in an ancient Egyptian prison interior: "
     f"organizing other prisoners, a look of quiet dignity and purpose, "
     f"divine favor in an unlikely place. {C}"),

    (193, "193_cupbearer_baker.jpg",
     "Two of Pharaoh's servants were thrown into prison — the cupbearer and the baker.",
     f"Cinematic scene: two finely dressed Egyptian officials being escorted "
     f"into the ancient prison, their fine garments incongruous with the setting, "
     f"ancient Egyptian prison. {C}"),

    (194, "194_each_had_a_dream.jpg",
     "Each of them had a dream the same night. Each dream had a meaning.",
     f"Interior of an ancient Egyptian prison at night: "
     f"two men lying on stone floors, their troubled faces illuminated "
     f"by a shaft of moonlight, dreaming. {C}"),

    (195, "195_joseph_interpreted.jpg",
     "Joseph interpreted their dreams. To the cupbearer — in three days you will be restored. Remember me.",
     f"{JOSEPH_EGYPT} speaking earnestly to the cupbearer in the prison, "
     f"the interpretation given with confidence and a desperate plea, "
     f"ancient Egyptian prison interior. {C}"),

    (196, "196_cupbearer_forgot.jpg",
     "The cupbearer was restored. But he forgot Joseph. Joseph remained in prison for two more years.",
     f"Cinematic contrast: the restored Egyptian cupbearer presenting a golden cup to {PHARAOH_EGYPT} "
     f"in the splendor of the palace — cut to: {JOSEPH_EGYPT} alone in the prison, "
     f"forgotten, waiting. {C}"),

    # ─── STORY 14: PHARAOH'S DREAMS ─────────────────────────────────────────

    (197, "197_pharaoh_had_a_dream.jpg",
     "Then Pharaoh had a dream.",
     f"Wide cinematic establishing shot of ancient Egypt at night: "
     f"the Nile under moonlight, the royal palace on the bank, "
     f"a great king within, sleeping, dreaming. {C}"),

    (198, "198_seven_fat_cows.jpg",
     "Seven fat cows rose from the Nile. Seven thin cows devoured them.",
     f"Dream-sequence cinematic shot: seven healthy cattle standing at the Nile's edge "
     f"in lush reeds, and seven gaunt cattle visible behind them, "
     f"the surreal quality of a prophetic dream, ancient Egyptian Nile setting. {C}"),

    (199, "199_seven_heads_of_grain.jpg",
     "Seven healthy heads of grain. Seven scorched heads swallowed them.",
     f"Dream-sequence cinematic shot: seven full golden grain heads on a stalk, "
     f"seven withered scorched heads beside them, "
     f"ancient Egyptian grain field in the prophetic dream. {C}"),

    (200, "200_none_could_interpret.jpg",
     "None of Egypt's wise men could interpret the dreams.",
     f"Wide shot of {PHARAOH_EGYPT} on his throne, "
     f"surrounded by a circle of Egyptian wise men and magicians — "
     f"all bowing their heads in failure, the king's distress evident. {C}"),

    (201, "201_cupbearer_remembered.jpg",
     "The cupbearer remembered — there is a Hebrew in the prison who interprets dreams.",
     f"The Egyptian cupbearer standing before {PHARAOH_EGYPT}, "
     f"memory and guilt crossing his face, "
     f"the long-delayed memory of Joseph finally spoken aloud. {C}"),

    (202, "202_joseph_brought_out.jpg",
     "They brought Joseph out. He was shaved and given clean clothes.",
     f"{JOSEPH_EGYPT} — shaved, in clean fine Egyptian linen — "
     f"being led through the palace corridors toward the throne room, "
     f"the transformation from prisoner to dignitary. {C}"),

    (203, "203_stood_before_pharaoh.jpg",
     "He stood before Pharaoh.",
     f"Wide cinematic throne room shot: {JOSEPH_EGYPT} standing before "
     f"{PHARAOH_EGYPT} on his throne, the vast Egyptian hall around them, "
     f"columns and courtiers, ancient Egyptian palace setting. {C}"),

    (204, "204_god_will_give_answer.jpg",
     "Joseph said — it is not I who interprets. God will give Pharaoh the answer.",
     f"Close-up portrait: {JOSEPH_EGYPT} standing before Pharaoh, "
     f"his face humble but confident, the boldness of a man who gives credit to God "
     f"before the most powerful ruler in the world. {C}"),

    (205, "205_seven_years_abundance.jpg",
     "Seven years of great abundance are coming. Followed by seven years of terrible famine.",
     f"Cinematic split composition: one side — golden Egyptian fields, full granaries, "
     f"the Nile in flood; other side — cracked dry earth, empty storehouses, "
     f"the contrast of plenty and famine. {C}"),

    (206, "206_appoint_wise_man.jpg",
     "Let Pharaoh appoint a wise man and set him over the land of Egypt.",
     f"{JOSEPH_EGYPT} speaking to {PHARAOH_EGYPT} with calm authority, "
     f"the advice freely given, the solution clear, "
     f"ancient Egyptian throne room. {C}"),

    (207, "207_spirit_of_god.jpg",
     "Pharaoh said — can we find anyone like this man, in whom is the spirit of God?",
     f"{PHARAOH_EGYPT} on his throne, turning to his officials with wide eyes, "
     f"the recognition of something holy in the young Hebrew standing before him, "
     f"ancient Egyptian court. {C}"),

    (208, "208_signet_ring.jpg",
     "He placed his signet ring on Joseph's finger. He gave him gold and fine linen.",
     f"Close-up cinematic detail: {PHARAOH_EGYPT}'s hand placing a heavy gold ring "
     f"onto {JOSEPH_EGYPT}'s finger, the moment of elevation, "
     f"ancient Egyptian ceremonial garments. {C}"),

    (209, "209_joseph_thirty.jpg",
     "Joseph was thirty years old when he stood before Pharaoh.",
     f"Portrait of {JOSEPH_EGYPT} in Egyptian robes and gold chain, "
     f"strong and dignified at thirty, the transformation from slave to ruler, "
     f"ancient Egyptian setting. {C}"),

    (210, "210_seven_years_abundance.jpg",
     "Seven years of abundance came. Joseph stored grain beyond counting.",
     f"Wide cinematic shot: vast Egyptian grain stores being filled, "
     f"workers carrying enormous loads, storehouses bulging, "
     f"the organized preparation for disaster, ancient Egyptian granary. {C}"),

    (211, "211_famine_began.jpg",
     "Then the famine began. It spread over the whole world.",
     f"Wide cinematic shot: a dry cracked ancient landscape, "
     f"withered crops, parched earth, emaciated cattle, "
     f"the bleached emptiness of famine, ancient Near Eastern setting. {C}"),

    (212, "212_jacob_sent_sons.jpg",
     "Jacob heard there was grain in Egypt and sent his sons.",
     f"{JACOB_OLD} — very old now — speaking urgently to his {BROTHERS}, "
     f"sending them on a journey, ancient Canaanite famine setting. {C}"),

    (213, "213_brothers_bowed.jpg",
     "Joseph's brothers came and bowed down before him with their faces to the ground.",
     f"Wide cinematic throne room shot: the {BROTHERS} — dusty from the journey — "
     f"bowing with their faces to the ground before {JOSEPH_EGYPT} on his elevated seat, "
     f"the dream fulfilled exactly as dreamed. {C}"),

    (214, "214_joseph_recognized.jpg",
     "Joseph recognized them. They did not recognize him. He wept in secret.",
     f"Close-up of {JOSEPH_EGYPT}'s face: recognition blazing in his eyes "
     f"as he sees his brothers — but controlled, masked, "
     f"the emotion held back by an act of will, ancient Egyptian setting. {C}"),

    (215, "215_he_tested_them.jpg",
     "He tested them. He accused them. He watched their hearts.",
     f"{JOSEPH_EGYPT} — stern and unrecognized — speaking harshly to the {BROTHERS}, "
     f"their confused and frightened faces, "
     f"a test they don't know they're taking. {C}"),

    (216, "216_could_not_control.jpg",
     "Finally — he could not control himself. He wept so loudly the Egyptians heard.",
     f"Dramatic cinematic scene: {JOSEPH_EGYPT} turning away from the court, "
     f"his body shaking with uncontrollable weeping, "
     f"the emotional dam breaking after years of separation. {C}"),

    (217, "217_i_am_joseph.jpg",
     "I am Joseph. Is my father still alive?",
     f"Close-up of {JOSEPH_EGYPT}'s face, tear-streaked, turning to his {BROTHERS} "
     f"with the words that change everything, "
     f"and the {BROTHERS}' stunned, terrified faces behind him. {C}"),

    (218, "218_jacob_comes_to_egypt.jpg",
     "Jacob came to Egypt. Joseph rode out to meet him. He held his father and wept.",
     f"Wide cinematic reunion scene: {JOSEPH_EGYPT} in his Egyptian chariot "
     f"riding out to meet {JACOB_OLD} — who is walking slowly — "
     f"and then the embrace, father and son, after more than twenty years, "
     f"the Nile delta landscape around them, ancient setting. {C}"),

]

# ── API helpers ────────────────────────────────────────────────────────────────

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
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
        f"?key={key}",
        json={"contents": [{"parts": [{"text": prompt}]}],
              "generationConfig": {"responseModalities": ["image"]}},
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
    for attempt in range(3):
        try:
            data = _imagen_predict("imagen-4.0-ultra-generate-001", prompt, key)
            out_path.write_bytes(data)
            return
        except RuntimeError as e:
            if "RATE_LIMIT" not in str(e):
                if attempt < 2:
                    time.sleep(8)
            else:
                break

    for attempt in range(5):
        try:
            data = _nano_banana(prompt, key)
            out_path.write_bytes(data)
            return
        except RuntimeError as e:
            wait = min(60, 15 * (attempt + 1))
            print(f"      Nano Banana attempt {attempt+1} failed ({str(e)[:60]}), waiting {wait}s...")
            time.sleep(wait)

    raise RuntimeError("All models failed after retries")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start",   type=int, default=1,   help="Resume from scene N")
    parser.add_argument("--end",     type=int, default=218, help="Stop at scene N")
    parser.add_argument("--dry-run", action="store_true",   help="Print prompts only")
    args = parser.parse_args()

    env = load_env()
    key = env.get("GOOGLE_AI_STUDIO_KEY", "")
    if not key and not args.dry_run:
        sys.exit("GOOGLE_AI_STUDIO_KEY not in .env")

    scenes = [s for s in SCENES if args.start <= s[0] <= args.end]
    total  = len(scenes)
    done   = sum(1 for s in scenes if (OUT_DIR / s[1]).exists())
    print(f"\nGenesis Patriarchs — generating images {args.start}-{args.end}")
    print(f"Output: {OUT_DIR}")
    print(f"Total: {total} | Done: {done} | Remaining: {total - done}\n")

    for scene_num, filename, narration, prompt in scenes:
        out_path = OUT_DIR / filename
        print(f"[{scene_num:03d}] {narration[:65]}{'…' if len(narration)>65 else ''}")

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
            print(f"       ✓ {size_kb} KB ({elapsed:.1f}s)")
        except Exception as e:
            print(f"       ✗ FAILED: {e}")

    existing = sum(1 for s in SCENES if (OUT_DIR / s[1]).exists())
    print(f"\nDone. {existing}/{len(SCENES)} images in {OUT_DIR}/")

if __name__ == "__main__":
    main()
