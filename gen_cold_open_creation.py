"""
Ultra-detailed story image generator for:
  - Cold Open (scenes 1-55, Chapter 1)
  - The Creation (scenes 56-110, Chapter 1)

Each scene gets a hand-crafted, ultra-specific prompt ensuring perfect visual-to-narration alignment.
Images saved to: project/stories/ch01_cold_open/ and project/stories/ch01_the_creation/

Usage:
    python gen_cold_open_creation.py                    # uses Replicate by default
    python gen_cold_open_creation.py --api google       # uses Google AI Studio Imagen 4 Fast
    python gen_cold_open_creation.py --start 56         # resume from scene 56
    python gen_cold_open_creation.py --dry-run          # show prompts, no generation
"""

import os
import sys
import time
import base64
import argparse
import urllib.request
from pathlib import Path

# ── Output dirs ────────────────────────────────────────────────────────────────
COLD_OPEN_DIR = Path("project/stories/ch01_cold_open")
CREATION_DIR  = Path("project/stories/ch01_the_creation")
COLD_OPEN_DIR.mkdir(parents=True, exist_ok=True)
CREATION_DIR.mkdir(parents=True, exist_ok=True)

# ── Base style suffix appended to every prompt ─────────────────────────────────
CINEMATIC = (
    "Ultra photorealistic, 8K cinema camera, IMAX cinematic quality, "
    "dramatic lighting, no text overlays, no watermarks, no subtitles, "
    "film grain, anamorphic lens flare, movie still frame"
)

# ═══════════════════════════════════════════════════════════════════════════════
# SCENE DEFINITIONS
# Each entry: (scene_number, output_dir_key, filename, narration, prompt)
# output_dir_key: "cold_open" or "creation"
# ═══════════════════════════════════════════════════════════════════════════════

SCENES = [

    # ── COLD OPEN ──────────────────────────────────────────────────────────────
    # Scenes 1-4 are title cards — use a deep cosmic void background
    (1, "cold_open", "001_title_ot_documentary.jpg",
     "The Old Testament. A cinematic documentary.",
     "Infinite cosmos, deep space, swirling nebula of gold and deep violet, "
     "ancient starlight piercing primordial darkness, no planets yet formed, "
     "vast emptiness stretching in every direction, pure cosmic majesty before time began. "
     "Extreme wide shot of the void, no horizon, no planets, no galaxies yet — only the first stirring of light. "
     + CINEMATIC),

    (2, "cold_open", "002_part_1.jpg",
     "Part 1.",
     "Deep interstellar void, absolute darkness broken only by faint wisps of golden cosmic dust, "
     "like the first breath before creation, the universe holding still before the beginning, "
     "a single point of faint warm light at the center of infinite blackness, "
     "vast cosmic silence, cinematic wide shot of pre-creation nothingness. "
     + CINEMATIC),

    (3, "cold_open", "003_book_of_genesis.jpg",
     "The Book of Genesis. Creation to Babel.",
     "Ancient worn stone tablets partially buried in desert sand, carved Hebrew letters glowing faintly with golden light, "
     "the words 'In the beginning' barely visible in ancient script, "
     "warm desert sunset behind low dunes, cinematic close-up of weathered stone, "
     "sacred and ancient atmosphere, dust particles floating in amber light. "
     + CINEMATIC),

    (4, "cold_open", "004_cold_open_title.jpg",
     "Cold Open.",
     "Extreme close-up of a single drop of water falling into a perfectly still, mirror-black primordial ocean, "
     "ripples spreading outward in slow motion, the reflection showing only darkness above, "
     "no sky yet visible, deep blue-black water, absolute silence captured in a single frozen moment. "
     + CINEMATIC),

    (5, "cold_open", "005_before_kingdoms.jpg",
     "Before kingdoms,",
     "Sweeping aerial shot over an endless, barren pre-history landscape — no roads, no buildings, no signs of human civilization, "
     "only raw untouched ancient earth: vast rocky plains under a turbulent amber sky, "
     "no crops, no cities, no fences, just primal land before any human hand touched it, "
     "moody overcast light with shafts of sun piercing heavy clouds. "
     + CINEMATIC),

    (6, "cold_open", "006_before_nations.jpg",
     "before nations, before the first whisper of human breath,",
     "Vast primordial wilderness, untouched ancient Earth before humanity — "
     "towering ancient forests of enormous trees stretching to the horizon, "
     "no paths, no clearings made by man, no smoke, no fires, "
     "only wild nature in its most raw and original state, "
     "morning mist rising between ancient trees, golden light filtering through dense canopy. "
     + CINEMATIC),

    (7, "cold_open", "007_before_egypt.jpg",
     "before the rise of Egypt,",
     "The Nile valley seen from far above as raw, untouched desert and river — "
     "no pyramids, no cities, no irrigation channels, no roads, "
     "just the raw ancient river cutting through endless sand and rock "
     "under a blazing sun, completely wild and empty, before any civilization existed. "
     + CINEMATIC),

    (8, "cold_open", "008_before_mesopotamia.jpg",
     "before the cities of Mesopotamia,",
     "The fertile crescent as raw, untouched land — "
     "the Tigris and Euphrates rivers flowing through wild marshland and open plains, "
     "no Babylon, no Ur, no Nineveh, no ziggurats — just wide rivers cutting through "
     "untouched ancient earth, reeds and wild palms, no human structures anywhere, "
     "aerial wide shot at golden hour before civilization rose. "
     + CINEMATIC),

    (9, "cold_open", "009_before_stars_had_names.jpg",
     "before the stars had names,",
     "Spectacular wide-angle shot of the night sky over an empty ancient landscape — "
     "the Milky Way blazing in its full glory, thousands of stars in the sky, "
     "no artificial lights on the ground below, no campfires, no torches, "
     "just pure ancient darkness and starlight, the universe unnamed and unnamed, "
     "wide shot of stars reflecting in a still primordial lake. "
     + CINEMATIC),

    (10, "cold_open", "010_the_deep.jpg",
     "there was only the deep,",
     "The primordial ocean before creation — a vast, dark, perfectly still body of infinite water "
     "stretching in every direction to the horizon with no land visible anywhere, "
     "deep blue-black water surface, no waves, no wind, no life, "
     "heavy dark clouds above touching the water, absolute stillness, "
     "the formless void of Genesis 1:2, cinematic wide shot. "
     + CINEMATIC),

    (11, "cold_open", "011_vast_silent.jpg",
     "vast, silent,",
     "Extreme wide aerial shot over the face of the primordial deep — "
     "an endless black ocean stretching to every horizon with no land, "
     "perfectly calm, mirror-like surface reflecting infinite darkness above, "
     "not a single ripple, not a single sound implied in the stillness, "
     "pre-creation void, deep blue-black, absolute quiet captured visually. "
     + CINEMATIC),

    (12, "cold_open", "012_formless_silence.jpg",
     "formless, and into that silence,",
     "Abstract cosmic visualization of formless void — "
     "swirling dark matter and faint wisps of primordial gas barely visible in absolute blackness, "
     "no defined shapes, no structure, pure raw chaos of pre-creation, "
     "a faint golden warmth at the very center of the frame hinting at what is about to come, "
     "extreme atmospheric abstract cinematic space photography. "
     + CINEMATIC),

    (13, "cold_open", "013_came_a_voice.jpg",
     "came a voice. This is the story of how everything began,",
     "A single pulse of divine golden light emanating outward from absolute center of darkness — "
     "like the very first sound wave rippling through the void, "
     "rings of warm golden light expanding in concentric circles into infinite black space, "
     "no source visible, only the effect of a voice that shook the universe, "
     "cinematic slow-motion freeze-frame of the very first moment. "
     + CINEMATIC),

    (14, "cold_open", "014_first_light_first_betrayal.jpg",
     "of the first light, the first betrayal,",
     "Split-tone cinematic composite: on the left, warm golden divine light flooding through darkness; "
     "on the right, the deep shadows of a lush garden at dusk with a hint of a serpent's iridescent scales visible in dark foliage — "
     "the contrast between light and shadow, creation and corruption, "
     "wide cinematic frame, no people visible, atmospheric and symbolic. "
     + CINEMATIC),

    (15, "cold_open", "015_first_murder_first_flood.jpg",
     "the first murder, the first flood,",
     "Turbulent dark storm clouds gathering over a windswept desolate plain, "
     "lightning splitting the sky, rain beginning to hammer barren earth, "
     "the horizon darkening with a wall of approaching floodwaters in the distance, "
     "apocalyptic atmosphere, dramatic side-lighting, no human figures visible, "
     "wide cinematic landscape of judgment approaching. "
     + CINEMATIC),

    (16, "cold_open", "016_world_born_perfect.jpg",
     "of a world that was born perfect and broken almost as quickly, of a family",
     "The lush paradise garden of Eden in its full glory at golden hour — "
     "towering ancient trees heavy with fruit, rivers glittering with clean water, "
     "flowers in every color, animals living peacefully together, "
     "warm golden light flooding every corner of paradise, "
     "and yet at the very edge of frame, a shadow begins to fall. "
     "Extreme wide cinematic establishing shot of Eden, no people. "
     + CINEMATIC),

    (17, "cold_open", "017_fall_and_rise.jpg",
     "that would fall and rise and fall again,",
     "Ancient desert landscape with a single weathered stone altar in the middle distance, "
     "surrounded by the remnants of a camp — scattered possessions, cold fire embers, "
     "a path leading away into harsh wilderness under a vast sky, "
     "the light is dawn, suggesting a new beginning after hardship, "
     "no people visible, atmosphere of human endurance and resilience. "
     + CINEMATIC),

    (18, "cold_open", "018_creator_who.jpg",
     "and of a creator who,",
     "Overwhelming column of divine golden-white light descending from above the clouds, "
     "piercing downward through heavy storm clouds to touch the earth below, "
     "the light is warm, powerful, and alive — not lightning but divine presence, "
     "no human form visible, only the effect of God's presence on the landscape, "
     "awe-inspiring wide shot from below looking up into the divine light. "
     + CINEMATIC),

    (19, "cold_open", "019_world_turned_against.jpg",
     "even when his world turned against him,",
     "Vast desolate post-flood landscape — a world exhausted and emptied, "
     "muddy floodwaters receding from barren hillsides, dead trees, grey sky, "
     "the earth stripped of its former beauty, but a single ray of golden light "
     "breaking through the clouds in the distance, suggesting hope remains. "
     "Wide cinematic shot, no people visible. "
     + CINEMATIC),

    (20, "cold_open", "020_refused_to_walk_away.jpg",
     "refused to walk away. This is the Book of Genesis,",
     "A vast rainbow arching over a stormy ancient landscape after the flood — "
     "vivid colors cutting across dark storm clouds, reflected in flood puddles below, "
     "the earth wet and devastated but the rainbow blazing with color and promise, "
     "the visual covenant between God and earth, wide dramatic cinematic shot. "
     + CINEMATIC),

    (21, "cold_open", "021_this_is_where_it_begins.jpg",
     "and this is where it all begins.",
     "The universe at the moment before the first word — "
     "absolute primordial darkness with a single point of impossibly bright white-gold light "
     "beginning to expand outward from the center, "
     "the Big Bang as a divine act, rings of light pushing back the void, "
     "the very first moment of creation, cinematic extreme wide shot. "
     + CINEMATIC),

    # Scenes 22-25 are chapter headings — use cosmic/ancient visuals
    (22, "cold_open", "022_book_of_genesis_header.jpg",
     "Book of Genesis.",
     "Ancient stone wall in golden desert light with carved Hebrew text, "
     "the words worn smooth by millennia, amber and ochre tones, "
     "shafts of desert sunlight falling across carved letters, "
     "desert sand shifting at the base, atmospheric and sacred, "
     "macro cinematic close-up of ancient carved stone scripture. "
     + CINEMATIC),

    (23, "cold_open", "023_genesis_1.jpg",
     "Genesis 1.",
     "Looking up at the night sky from ancient desert, "
     "the Milky Way blazing overhead, every star crisp and brilliant, "
     "the horizon a deep blue-black meeting the black sky, "
     "the universe vast and unnamed, before time was measured, "
     "ultra-wide cinematic shot, no light pollution, pure starfield. "
     + CINEMATIC),

    (24, "cold_open", "024_creation_of_the_world.jpg",
     "The Creation of the World.",
     "The Earth as seen from space in its primal state — "
     "swirling clouds covering a young planet, oceans forming, "
     "landmasses just beginning to solidify through volcanic activity, "
     "glowing red-orange lava veins visible through cloud breaks, "
     "the planet raw and new, creation in process, wide cinematic space view. "
     + CINEMATIC),

    (25, "cold_open", "025_before_recorded_history.jpg",
     "Approximately before recorded history.",
     "Ancient starfield stretching to infinity, "
     "time itself seeming to stretch backwards through light years, "
     "stars blurring into streaks as if traveling back through time, "
     "warm golden tones in the deep cosmos, no planets, only light and dark, "
     "cinematic time-lapse of cosmic depth. "
     + CINEMATIC),

    (26, "cold_open", "026_in_the_beginning_nothing.jpg",
     "In the beginning, there was nothing.",
     "Pure absolute void — the most complete darkness imaginable, "
     "not a single photon of light, not a dust particle, not a molecule of gas, "
     "infinite empty nothingness stretching in every direction, "
     "yet with a subtle texture suggesting the potential for something, "
     "the cinematic representation of pre-creation emptiness before Genesis 1:1. "
     + CINEMATIC),

    (27, "cold_open", "027_no_earth_no_sun.jpg",
     "No earth, no sun,",
     "Swirling cosmic gas clouds in deep space, the raw materials of a future solar system "
     "suspended in chaos — hydrogen and helium clouds slowly spiraling, "
     "not yet compressed into stars or planets, just formless cosmic matter, "
     "faint wisps of gold and purple nebula gas in absolute black space, "
     "pre-stellar formation, wide cinematic space photography. "
     + CINEMATIC),

    (28, "cold_open", "028_no_sky_no_time.jpg",
     "no sky, no measure of time, because time itself had not yet begun.",
     "Abstract visualization of pre-time — all motion frozen, "
     "a cosmic clock with no hands, light rays suspended mid-travel, "
     "a universe paused at absolute zero on the timeline, "
     "deep space with frozen light rays and dust particles suspended in void, "
     "no movement, no direction, time has no meaning here, cinematic and philosophical. "
     + CINEMATIC),

    (29, "cold_open", "029_only_god_and_then.jpg",
     "Only God. And then,",
     "The void holding still — and then the very first stirring of divine intention: "
     "a single luminous point of perfect white-gold light appearing at the center of infinite darkness, "
     "so small and yet so certain, it changes everything, "
     "the first moment of God's active presence in creation, "
     "extreme cinematic close-up of the single point of light against absolute black. "
     + CINEMATIC),

    (30, "cold_open", "030_a_word_first_sound.jpg",
     "a word. The first sound the universe had ever known,",
     "Sound waves visualized as visible ripples expanding outward through space — "
     "golden concentric rings spreading from a single divine source, "
     "pushing back the darkness like a pebble dropped in still water, "
     "the very first vibration in the history of the cosmos, "
     "wide cinematic shot of light-rings expanding through space. "
     + CINEMATIC),

    (31, "cold_open", "031_voice_over_darkness.jpg",
     "a voice moving over the darkness,",
     "The face of the deep — a vast, utterly dark primordial ocean in absolute stillness, "
     "and then a gentle wind beginning to stir the surface, "
     "ripples moving across the darkness as if a breath passed over the water, "
     "the Spirit of God moving over the waters as in Genesis 1:2, "
     "cinematic low shot over dark water, light beginning at the horizon. "
     + CINEMATIC),

    (32, "cold_open", "032_breath_stirring_deep.jpg",
     "a breath stirring across the deep,",
     "Macro close-up of the surface of a primordial ocean — "
     "the black water surface breaking into tiny ripples as if touched by an invisible breath, "
     "the first movement in the void, the first disruption of perfect stillness, "
     "a warm golden light just beginning to glow beneath the horizon, "
     "cinematic extreme close-up, shallow depth of field, ethereal atmosphere. "
     + CINEMATIC),

    (33, "cold_open", "033_first_command.jpg",
     "and from that voice came the first command spoken into the voice,",
     "Abstract cosmic visualization of a divine command: "
     "a pulse of golden energy radiating outward from a central point in the void, "
     "the sound wave of a voice reshaping the fabric of emptiness, "
     "reality itself bending in response to the first spoken word, "
     "warm gold and white energy lines spreading through infinite blackness, "
     "cinematic abstract representation of God speaking into void. "
     + CINEMATIC),

    (34, "cold_open", "034_let_there_be_light.jpg",
     "let there be light,",
     "The first creation of light — not from a sun or star, "
     "but divine light flooding through the void from everywhere at once, "
     "pure white-gold radiance tearing through absolute primordial darkness, "
     "the darkness itself pulling back as light advances, "
     "dramatic sharp edge between light and darkness, "
     "cinematic extreme wide shot of the very first moment light existed. "
     + CINEMATIC),

    (35, "cold_open", "035_darkness_obeyed.jpg",
     "and the darkness obeyed.",
     "The darkness receding before the first divine light — "
     "blackness rolling back like a curtain being pulled away, "
     "warm golden light flooding the frame from top-left as darkness retreats to bottom-right, "
     "the border between light and dark shifting across the frame, "
     "the universe's first obedience, cinematic wide dramatic shot. "
     + CINEMATIC),

    (36, "cold_open", "036_light_tore_through.jpg",
     "Light tore through the emptiness,",
     "Explosive divine light bursting outward in every direction through cosmic void — "
     "not an explosion but a revelation, white-gold radiance piercing through the darkest corners of space, "
     "rays of pure light cutting through absolute darkness like swords, "
     "the universe being illuminated for the first time, "
     "dramatic cinematic shot of light expanding through emptiness. "
     + CINEMATIC),

    (37, "cold_open", "037_not_from_a_star.jpg",
     "not from a star, not from a sun,",
     "Deep space showing no stars, no sun, no celestial bodies of any kind — "
     "just pure divine light filling the cosmos from no identifiable source, "
     "the light itself the source, uncreated and sovereign, "
     "illuminating nothing but the void, warm golden radiance with no origin point, "
     "wide cinematic shot of sourceless divine light in empty space. "
     + CINEMATIC),

    (38, "cold_open", "038_from_the_will.jpg",
     "because neither yet existed, but from the will of the one who spoke.",
     "A single blazing point of divine intelligence at the center of the cosmos — "
     "pure white-gold light emanating from the intersection of all things, "
     "the universe arranged around this single sovereign point of will, "
     "cosmic rays spreading outward in perfect symmetry, "
     "cinematic extreme wide shot showing the ordered expansion of light from a single divine source. "
     + CINEMATIC),

    (39, "cold_open", "039_light_spread.jpg",
     "And as the light spread,",
     "Light expanding across the cosmos like a sunrise on an infinite scale — "
     "a warm golden line of illumination moving across the darkness, "
     "gradually revealing the raw, unformed early universe: gas clouds, cosmic dust, "
     "the skeleton of what will become creation slowly coming into view, "
     "cinematic wide shot of early light spreading across the face of the deep. "
     + CINEMATIC),

    (40, "cold_open", "040_universe_took_shape.jpg",
     "the universe began to take shape.",
     "Time-lapse of cosmic formation: swirling gas clouds beginning to condense, "
     "matter organizing itself, galaxies forming in their first spiral arms, "
     "the raw chaos of creation finding its first structure, "
     "warm gold and orange nebula clouds taking form in golden light, "
     "wide cinematic space shot of early cosmic structure emerging from chaos. "
     + CINEMATIC),

    (41, "cold_open", "041_second_day.jpg",
     "On the second day,",
     "The expanse of sky on Day Two of creation — "
     "a vast dome of pure deep blue atmosphere just formed, "
     "stretching from horizon to horizon over a still dark ocean below, "
     "the first sky, clouds beginning to form, "
     "the boundary between water and sky just established, "
     "ultra-wide cinematic shot looking across the first sky and sea. "
     + CINEMATIC),

    (42, "cold_open", "042_heavens_opened.jpg",
     "the heavens opened. The sky stretched out like a vast canopy above the waters.",
     "The sky on Day Two — a blazing blue atmosphere stretching like a tent over dark primordial waters, "
     "the very first clouds forming white and pure, "
     "the horizon where sea meets sky razor-sharp for the first time in history, "
     "golden light from above illuminating pale blue sky and dark blue water below, "
     "cinematic ultra-wide split horizon shot of the new firmament. "
     + CINEMATIC),

    (43, "cold_open", "043_dry_land_rose.jpg",
     "On the third, dry land rose from the seas.",
     "Volcanic land mass rising from the primordial ocean — "
     "ancient rock pushing up through churning dark water, "
     "steam and mist as hot new land meets sea, "
     "the very first coastline forming in the history of the world, "
     "dramatic wide shot of new land emerging from ocean under storm clouds "
     "with divine light breaking through above. "
     + CINEMATIC),

    (44, "cold_open", "044_mountains_pushed_upward.jpg",
     "Mountains pushed upward.",
     "Dramatic aerial shot of ancient mountain ranges thrusting upward from flat earth — "
     "jagged peaks covered in fresh rock, no erosion yet, "
     "the raw geology of new mountains catching first sunlight, "
     "snowy peaks already forming at altitude, "
     "wide cinematic aerial view of mountains as they would have looked the first day they existed. "
     + CINEMATIC),

    (45, "cold_open", "045_valleys_carved.jpg",
     "Valleys carved themselves into the earth.",
     "A sweeping ancient valley cutting between dramatic mountain walls, "
     "river running along its floor, rock walls exposed and raw, "
     "no vegetation yet, just the pure geology of a freshly carved valley, "
     "dramatic side-lighting revealing the depth and scale of the carved landscape, "
     "wide cinematic aerial shot of valleys forming in new earth. "
     + CINEMATIC),

    (46, "cold_open", "046_forests_bloomed.jpg",
     "Forests bloomed where there had only been silence.",
     "The first forests of Eden-era Earth — impossibly lush, ancient, primeval forests, "
     "enormous trees covered in moss, ferns, flowering plants at their feet, "
     "golden-green light filtering through an unbroken canopy, "
     "no paths, no clearings, just pure wild ancient forest in its virgin state, "
     "every shade of green imaginable, cinematic wide shot into the ancient wood. "
     + CINEMATIC),

    (47, "cold_open", "047_fourth_day_sun.jpg",
     "On the fourth day, the sun was set to blaze in the heavens.",
     "The sun appearing for the first time — blazing, sovereign, "
     "a perfect sphere of white-gold fire hanging in a deep blue sky, "
     "no haze, no clouds obscuring it, its first light falling clean and pure "
     "across the newly formed earth below, "
     "wide cinematic shot from earth surface looking up at the blazing new sun. "
     + CINEMATIC),

    (48, "cold_open", "048_moon_took_her_place.jpg",
     "The moon took her place in the night,",
     "A full silver moon rising for the first time over a dark primordial ocean — "
     "the moon large and close, reflecting perfectly in still dark water, "
     "deep blue-black sky, stars beginning to appear, "
     "the first night of the fourth day, the moon sovereign in its orbit, "
     "cinematic wide shot of the first moonrise. "
     + CINEMATIC),

    (49, "cold_open", "049_stars_glittering_eternal.jpg",
     "and the stars, countless glittering, eternal,",
     "The first full night sky on Day Four — the Milky Way blazing in full glory, "
     "uncountable stars strewn across absolute black sky, "
     "starlight reflecting in a perfectly still primordial lake below, "
     "the moon and stars together for the first time, "
     "ultra-wide cinematic night sky photograph from ancient earth, no light pollution. "
     + CINEMATIC),

    (50, "cold_open", "050_scattered_across_dark.jpg",
     "were scattered across the dark,",
     "Extreme wide angle cosmic shot of the Milky Way galaxy from far outside — "
     "billions of stars in their spiral arms, scattered like diamonds on black velvet, "
     "the sheer number of stars overwhelming, each one placed with intention, "
     "deep space photography showing the full breadth of the star field, "
     "cinematic ultra-wide shot of the galaxy at its creation. "
     + CINEMATIC),

    (51, "cold_open", "051_pages_of_story.jpg",
     "like the pages of a story not yet written.",
     "Looking straight up into a star-filled sky from the earth — "
     "the Milky Way overhead like an open book, stars like letters waiting to be read, "
     "the ancient sky before any human was born to name a single constellation, "
     "pure untouched starfield, warm and mysterious, infinite in depth, "
     "cinematic vertical shot of stars overhead. "
     + CINEMATIC),

    (52, "cold_open", "052_fifth_day.jpg",
     "On the fifth day,",
     "Dawn of Day Five over a primal ocean — the sun rising over a vast sea "
     "that is about to fill with life, the water glittering with golden morning light, "
     "the surface still and expectant, the sky clear and brilliant, "
     "something is about to happen beneath the surface, "
     "cinematic wide shot of primordial sea at dawn before life began. "
     + CINEMATIC),

    (53, "cold_open", "053_life_began_to_move.jpg",
     "life began to move.",
     "Underwater shot of the primordial ocean floor suddenly stirring with new life — "
     "the first fish and sea creatures coming into existence, "
     "bioluminescent creatures flickering to life in deep dark water, "
     "schools of first fish catching light, "
     "the ocean floor waking from emptiness, "
     "cinematic underwater wide-angle shot of life beginning in the deep. "
     + CINEMATIC),

    (54, "cold_open", "054_oceans_creatures_stirred.jpg",
     "In the oceans, creatures stirred,",
     "Underwater view of the first ocean teeming with new life on Day Five — "
     "schools of fish catching golden light filtered from above, "
     "rays of sunlight piercing clear ancient water, "
     "every size and shape of sea creature, colorful and abundant, "
     "whale-like Leviathans visible in the deep background, "
     "cinematic wide underwater shot of the first sea life. "
     + CINEMATIC),

    (55, "cold_open", "055_fish_leviathans.jpg",
     "schools of fish, Leviathans of the deep,",
     "A massive Leviathan — a vast ancient sea creature — moving through deep dark ocean, "
     "silhouetted against filtered sunlight from above, "
     "schools of silver fish swirling around it like a living vortex, "
     "the sheer scale overwhelming, "
     "underwater cinematic wide shot showing the Leviathan in its full ancient magnificence. "
     + CINEMATIC),

    # ── THE CREATION (scenes 56-110) ──────────────────────────────────────────

    (56, "creation", "056_things_never_seen.jpg",
     "things that had never been seen before, because they had never existed before.",
     "Day Five and Six: a chaotic, exhilarating montage of new life — "
     "birds exploding from a treeline in a burst of wings, "
     "mammals racing across open savanna, reptiles lifting their heads in new sunlight, "
     "creatures of every kind appearing as if from nothing, "
     "wide cinematic shot of animals gathered in their first moments of existence. "
     + CINEMATIC),

    (57, "creation", "057_wings_unfurled.jpg",
     "In the skies, wings unfurled.",
     "Thousands of birds taking flight simultaneously on Day Five — "
     "every species: eagles, herons, colorful tropical birds, doves, swallows — "
     "all rising together from ancient trees in a spectacular explosion of wings, "
     "golden morning light backlighting their outstretched wings as they climb into new sky, "
     "cinematic wide shot looking up as birds fill the heavens for the first time. "
     + CINEMATIC),

    (58, "creation", "058_birds_rose.jpg",
     "Birds rose into the air,",
     "A flock of birds in perfect formation rising into a blazing golden sky — "
     "their wings catching sunlight, individual feathers backlit and glowing, "
     "the blue sky behind them pure and bright, no clouds, "
     "the sheer joy and freedom of the first flight in history, "
     "cinematic slow-motion-style close shot of birds ascending. "
     + CINEMATIC),

    (59, "creation", "059_calling_across_new_world.jpg",
     "calling to one another across the new world.",
     "A single magnificent bird — a large eagle or phoenix-like creature — "
     "perched on the highest branch of an ancient tree overlooking a vast pristine landscape, "
     "head back, calling across the new world for the first time, "
     "golden light illuminating its feathers, the landscape stretching endlessly below, "
     "cinematic wide shot establishing the new world with bird as foreground. "
     + CINEMATIC),

    (60, "creation", "060_sixth_day_land_alive.jpg",
     "And on the sixth day, the land itself came alive.",
     "Dawn of Day Six — the land trembling with new life appearing everywhere at once: "
     "animals walking out of mist across open plains, "
     "herds of elephants, lions, horses, cattle all present in the same vast landscape, "
     "the ground covered in lush green grass and wildflowers, "
     "dramatic golden hour light, cinematic extreme wide shot of the sixth day creation. "
     + CINEMATIC),

    (61, "creation", "061_cattle_on_hills.jpg",
     "Cattle on the hills,",
     "Rolling green hills covered with cattle of every kind — "
     "ancient wild aurochs grazing peacefully, the hills lush and green, "
     "morning mist still in the valleys, golden sunrise behind the hills, "
     "the cattle calm and content in their first moments of existence, "
     "cinematic pastoral wide shot of the sixth day. "
     + CINEMATIC),

    (62, "creation", "062_wild_beasts_forests.jpg",
     "wild beasts in the forests,",
     "Inside a magnificent ancient forest — lions and tigers moving between enormous trees, "
     "a massive bear resting against ancient bark, wolves watching from the shadows, "
     "yet none predatory, all peaceful, as God made them on Day Six, "
     "dappled forest light, golden shafts through the canopy, "
     "cinematic wide forest shot with wild animals. "
     + CINEMATIC),

    (63, "creation", "063_creeping_things.jpg",
     "creeping things in the grass.",
     "Macro close-up of lush grass teeming with the first insects and creeping creatures — "
     "a magnificent beetle with iridescent shell, a colorful butterfly landing on a flower, "
     "a lizard catching sunlight, a frog perched on a leaf, "
     "all impossibly detailed and beautiful, the small wonders of Day Six creation, "
     "macro cinematic photography of creatures in the grass. "
     + CINEMATIC),

    (64, "creation", "064_shaped_with_intention.jpg",
     "Every creature shaped with intention,",
     "A majestic lion lying regally in tall grass, perfectly framed in golden light — "
     "every detail of its form showing intentional design: mane, musculature, regal bearing, "
     "its amber eyes looking directly forward, commanding, "
     "the embodiment of designed magnificence, "
     "cinematic portrait of the lion as a masterwork of creation. "
     + CINEMATIC),

    (65, "creation", "065_every_detail.jpg",
     "every detail considered,",
     "Extreme close-up of a single peacock feather — "
     "the iridescent eye in the center blazing with blue, green, and gold, "
     "every microscopic barb perfectly ordered, a masterpiece of natural engineering, "
     "backlit by warm light, the colors shimmering, "
     "macro cinematic close-up showing the impossible complexity of a single feather. "
     + CINEMATIC),

    (66, "creation", "066_reflection_of_maker.jpg",
     "every form or reflection of the one who made them.",
     "A family of animals together in perfect harmony — "
     "a wolf, a deer, a lion cub, and an eagle all visible in the same frame, "
     "each one impossibly perfect in form, each reflecting a different facet of their creator's nature: "
     "power, grace, speed, majesty, "
     "golden light bathing them all, "
     "wide cinematic shot of animals in peaceful coexistence. "
     + CINEMATIC),

    (67, "creation", "067_at_the_very_end.jpg",
     "And then, at the very end,",
     "The Garden of Eden at golden hour on Day Six — all creation visible in one frame: "
     "animals grazing peacefully, birds in the sky, fish in crystal rivers, "
     "perfect lush landscape, and then in the center of the frame, "
     "a patch of bare earth where nothing yet stands — waiting, "
     "the space where something new is about to happen, "
     "cinematic wide establishing shot of the last moment before man. "
     + CINEMATIC),

    (68, "creation", "068_god_paused.jpg",
     "God paused. Because he was about to do something different.",
     "Abstract visualization of divine contemplation — "
     "a column of golden-white light hovering motionless above the bare earth of Eden, "
     "all creation around it perfectly still, animals paused, birds frozen mid-flight, "
     "the wind stopped, the whole world holding its breath, "
     "the moment of divine pause before the most important act of creation, "
     "cinematic wide shot, everything still except the glowing light. "
     + CINEMATIC),

    (69, "creation", "069_reached_into_dust.jpg",
     "He reached down into the dust of the earth he had just made.",
     "Close-up of golden-red earth on the floor of Eden — "
     "the bare soil of paradise, fine and warm, "
     "a subtle golden divine light beginning to concentrate on this patch of ground, "
     "the dust particles beginning to stir as if called, "
     "macro cinematic close-up of the earth that will become man, "
     "warm amber and gold tones. "
     + CINEMATIC),

    (70, "creation", "070_gathered_in_hands.jpg",
     "He gathered it in his hands.",
     "Extreme close-up of a handful of rich red-gold earth, soil and dust, "
     "held in invisible divine hands — the earth luminous, warm, glowing faintly, "
     "particles of dust suspended in a halo of golden light around it, "
     "the raw material of humanity about to become something more, "
     "cinematic macro close-up with shallow depth of field and warm light. "
     + CINEMATIC),

    (71, "creation", "071_shaped_not_animal.jpg",
     "And he shaped it, not into another animal,",
     "The dust of Eden beginning to take form — "
     "a swirling golden shape emerging from bare earth in a column of divine light, "
     "vaguely human but not yet complete, raw and unfinished, "
     "surrounded by other animals watching curiously from a distance, "
     "showing the difference: this creation is not like the others, "
     "cinematic medium shot of the formation process. "
     + CINEMATIC),

    (72, "creation", "072_carry_his_own_image.jpg",
     "not into another beast, but into something that would carry his own image.",
     "The silhouette of a man forming in golden light — "
     "still not complete, still glowing with divine energy, "
     "the shape distinctly human: upright, two-armed, head raised toward the sky, "
     "surrounded by animals but standing apart from them, "
     "the first image-bearer of God taking form, "
     "dramatic cinematic shot with divine light glowing through the forming figure. "
     + CINEMATIC),

    (73, "creation", "073_breathed_into_it.jpg",
     "He breathed into it,",
     "The divine breath: a column of golden-white divine light bending down toward the newly formed man, "
     "the breath of God as a visible stream of warm golden energy flowing from above, "
     "about to enter the figure of Adam, still not yet alive, "
     "the most intimate act of creation, "
     "cinematic close-up, warm golden light, the breath visible as a golden mist. "
     + CINEMATIC),

    (74, "creation", "074_dust_became_man.jpg",
     "and dust became man.",
     "Adam's chest heaving with his first breath — "
     "a powerfully built young Middle Eastern man, dark bronze skin, dark curly hair, "
     "early 30s, lying on his back on the lush grass of Eden, eyes just opening, "
     "his first breath filling his lungs, the golden light of God still fading around him, "
     "cinematic close-up of the first man taking his first breath, face and chest visible. "
     + CINEMATIC),

    (75, "creation", "075_first_time_universe.jpg",
     "For the first time in the history of the universe,",
     "Adam sitting up in Eden, looking around at the world for the first time — "
     "a powerfully built young Middle Eastern man with dark curly hair and bronze skin, "
     "sitting on lush green grass in the paradise garden, "
     "animals nearby watching curiously, golden light all around him, "
     "his expression: pure wonder and awareness, seeing the world for the first time, "
     "medium cinematic shot showing Adam amid the garden he just woke into. "
     + CINEMATIC),

    (76, "creation", "076_stood_upright_face_of_maker.jpg",
     "a creature stood upright and looked into the face of his maker.",
     "Adam standing tall in Eden for the first time — "
     "a powerfully built young Middle Eastern man, dark tanned skin, strong jaw, dark curly hair, "
     "standing fully upright in the center of the paradise garden, "
     "looking upward toward an overwhelming golden divine light above him, "
     "his expression: awe, reverence, the recognition of being known, "
     "cinematic medium-wide shot, divine light from above, garden all around. "
     + CINEMATIC),

    (77, "creation", "077_his_name_was_adam.jpg",
     "His name was Adam,",
     "Portrait of Adam — a powerful young Middle Eastern man in his early 30s, "
     "dark bronze skin, dark curly hair, strong jaw, deep brown eyes, "
     "standing in the paradise garden of Eden, serene and kingly, "
     "golden afternoon light illuminating his face, "
     "close-up portrait, looking directly at camera, "
     "completely natural, no shame, pure unfallen humanity. "
     + CINEMATIC),

    (78, "creation", "078_seventh_day.jpg",
     "and on the seventh day,",
     "The Garden of Eden at absolute peace on the seventh day — "
     "everything completed and perfect, golden light bathing every corner of paradise, "
     "animals resting contentedly, birds settled in trees, "
     "rivers glittering, fruit trees heavy with abundance, "
     "a profound and beautiful stillness, the first Sabbath, "
     "cinematic wide shot of Eden in perfect rest. "
     + CINEMATIC),

    (79, "creation", "079_creator_rested.jpg",
     "the creator rested. Not because he was tired, but because the work was",
     "A symbolic representation of rest: "
     "the divine golden light over Eden softening to a gentle warm glow, "
     "as if the light itself is resting, "
     "the garden in perfect stillness, every creature settled, "
     "the first Sabbath peace — complete, full, good, "
     "cinematic wide shot of Eden bathed in warm sabbath-afternoon light. "
     + CINEMATIC),

    (80, "creation", "080_finished_perfect.jpg",
     "finished, the world was perfect.",
     "Eden in its ultimate glory — the most beautiful landscape imaginable: "
     "lush beyond description, towering ancient trees, crystal rivers, every flower, "
     "every animal present and peaceful, the sky perfect blue, "
     "a world at the peak of its perfection before anything went wrong, "
     "cinematic extreme wide establishing shot of paradise at its finest. "
     + CINEMATIC),

    (81, "creation", "081_would_not_stay.jpg",
     "It would not stay that way for long.",
     "Eden in its glory — but a single shadow falling across the frame: "
     "a serpent visible in the deep background, coiled in the branches of a tree, "
     "barely visible, barely threatening yet, "
     "the first hint of darkness in paradise, "
     "the garden still beautiful but the shadow unmistakably there, "
     "cinematic wide shot with dramatic shadow cutting across the perfect garden. "
     + CINEMATIC),

    # Genesis 2-3 section header scenes
    (82, "creation", "082_genesis_2_3.jpg",
     "Genesis 2 -3.",
     "The Tree of Knowledge of Good and Evil — "
     "a magnificent ancient tree standing alone in a clearing in Eden, "
     "its bark dark and textured, its fruit red and impossibly perfect, "
     "dappled sunlight falling through the canopy, a subtle ominous atmosphere, "
     "no people visible, the tree itself the entire subject, "
     "cinematic portrait of the forbidden tree. "
     + CINEMATIC),

    (83, "creation", "083_adam.jpg",
     "Adam,",
     "Adam walking through Eden — "
     "a powerfully built young Middle Eastern man with dark curly hair and bronze skin, "
     "moving through the lush garden with confident stride, animals following him, "
     "morning light filtering through the canopy, "
     "medium cinematic shot, no other humans visible, "
     "the first man in his paradise home. "
     + CINEMATIC),

    (84, "creation", "084_eve_fall_of_man.jpg",
     "Eve, and the fall of man.",
     "The Tree of Knowledge with the serpent visible in its branches — "
     "the tree's fruit hanging heavy and red, the serpent barely visible coiled above, "
     "a sense of inevitability and foreboding, "
     "the tree catching last golden light before something changes, "
     "cinematic medium shot of the tree, dark and beautiful. "
     + CINEMATIC),

    (85, "creation", "085_dawn_of_humanity.jpg",
     "The dawn of humanity,",
     "Adam standing at the edge of a cliff in Eden, looking out over the vast paradise below — "
     "rolling green hills, rivers catching morning light, animals in the distance, "
     "the first human surveying his world at dawn, "
     "he stands upright, dark-haired, bronze-skinned, "
     "cinematic wide shot from behind showing Adam overlooking all of creation. "
     + CINEMATIC),

    (86, "creation", "086_god_planted_a_garden.jpg",
     "in the east, God planted a garden,",
     "Eden from above at the moment of its fullest beauty — "
     "four rivers flowing outward from the center of the garden like arms reaching to the world, "
     "lush beyond anything seen before or since, "
     "the garden radiating outward from a central glowing heart of divine light, "
     "aerial cinematic wide shot of the entire Garden of Eden. "
     + CINEMATIC),

    (87, "creation", "087_place_called_eden.jpg",
     "a place called Eden, a paradise unlike anything the earth would ever see again.",
     "The full grandeur of Eden — "
     "a panoramic view of paradise: towering ancient trees larger than anything modern, "
     "fruit of every kind, flowers, rivers, waterfalls, and every animal, "
     "golden afternoon light making everything glow, "
     "the most beautiful place that ever existed on earth, "
     "extreme wide cinematic establishing shot of the full Garden of Eden. "
     + CINEMATIC),

    (88, "creation", "088_rivers_flowed.jpg",
     "Rivers flowed through it,",
     "A crystal-clear river in Eden — "
     "impossibly clear water flowing over smooth colorful stones, "
     "flanked by lush tropical vegetation, flowers on the banks, "
     "fish visible through the glass-clear water, "
     "golden light reflecting in the ripples, "
     "cinematic wide shot following the river into the heart of paradise. "
     + CINEMATIC),

    (89, "creation", "089_trees_heavy_fruit.jpg",
     "trees heavy with fruit lined its paths,",
     "A pathway through Eden lined on both sides with ancient fruit trees — "
     "every type of fruit hanging in abundance: pomegranates, figs, dates, grapes, apples, "
     "branches bending under the weight of impossibly large, perfect fruit, "
     "golden light filtering through the laden branches, "
     "cinematic medium shot looking down the lush fruit-lined garden path. "
     + CINEMATIC),

    (90, "creation", "090_animals_no_fear.jpg",
     "animals roamed without fear.",
     "Animals living together in perfect harmony in Eden — "
     "a lion lying beside a lamb, a wolf beside a deer, an eagle beside a dove, "
     "all at rest together, no predators, no prey, "
     "just creatures in the paradise for which they were made, "
     "cinematic wide shot of multiple species sharing the same peaceful space. "
     + CINEMATIC),

    (91, "creation", "091_no_death.jpg",
     "There was no death here,",
     "Eden in absolute golden-hour perfection — "
     "every living thing vibrant and healthy, not a dead leaf or wilted flower visible, "
     "the Tree of Life glowing softly in the center of the garden, "
     "its golden light touching everything, keeping it alive, "
     "cinematic wide shot of paradise utterly without death or decay. "
     + CINEMATIC),

    (92, "creation", "092_no_sickness_sorrow.jpg",
     "no sickness, no sorrow,",
     "Two animals — a young deer and a lion — resting together in warm afternoon light, "
     "neither wounded, neither afraid, neither sick, "
     "the complete peace of paradise before the fall, "
     "dappled golden light through the canopy, "
     "cinematic close-up of the two animals at peace. "
     + CINEMATIC),

    (93, "creation", "093_no_hunger_no_shame.jpg",
     "no hunger, no shame,",
     "Adam surrounded by abundance in Eden — "
     "fruit trees bending toward him, wild berries at his feet, every provision made, "
     "a powerfully built young Middle Eastern man with dark curly hair, "
     "sitting at ease among the trees of paradise, "
     "no anxiety, no want, complete provision, "
     "cinematic medium shot of Adam at home in paradise. "
     + CINEMATIC),

    (94, "creation", "094_center_two_trees.jpg",
     "and in the center of the garden stood two trees,",
     "Two magnificent trees standing apart from all others at the center of Eden — "
     "one glowing with warm golden light (Tree of Life), "
     "one beautiful but darker in tone, its fruit deep red (Tree of Knowledge), "
     "both enormous and ancient, standing close together yet distinct, "
     "all other trees bowing away from them slightly, "
     "cinematic wide shot of the two central trees of Eden. "
     + CINEMATIC),

    (95, "creation", "095_tree_of_life.jpg",
     "the tree of life,",
     "The Tree of Life in Eden — "
     "a magnificent ancient tree with bark that glows with golden-white light, "
     "its leaves shimmering gold, its fruit luminous and radiant, "
     "small golden lights drifting from its branches like embers rising, "
     "the most beautiful tree imaginable, radiating warmth and life, "
     "cinematic wide portrait of the Tree of Life. "
     + CINEMATIC),

    (96, "creation", "096_tree_of_knowledge.jpg",
     "and the tree of the knowledge of good and evil.",
     "The Tree of Knowledge of Good and Evil — "
     "a strikingly beautiful but subtly ominous tree: "
     "deep mahogany bark, heavy branches laden with perfect deep-red fruit, "
     "a darker aura surrounding it compared to the rest of the garden, "
     "beautiful but with a sense of weight and consequence, "
     "cinematic medium shot of the forbidden tree alone. "
     + CINEMATIC),

    (97, "creation", "097_placed_adam_one_rule.jpg",
     "God placed Adam in the garden and gave him only one rule.",
     "Adam standing alone before the Tree of Knowledge — "
     "a powerfully built young Middle Eastern man with dark curly hair, "
     "looking up at the tree with expression of serious attention, "
     "the golden divine light beside him fading slightly, as if God has just spoken, "
     "the moment of receiving the one commandment, "
     "cinematic medium shot of Adam and the Tree of Knowledge. "
     + CINEMATIC),

    (98, "creation", "098_eat_from_any_tree.jpg",
     "He could eat from any tree.",
     "The abundance of Eden's fruit trees stretching in every direction — "
     "hundreds of different fruit trees visible, every kind of fruit imaginable, "
     "the sheer overwhelming generosity of God's provision for Adam, "
     "golden light making every fruit glow with color, "
     "cinematic wide shot showing the endless abundance available to Adam. "
     + CINEMATIC),

    (99, "creation", "099_any_tree_at_all.jpg",
     "Any tree at all,",
     "Adam reaching up to pluck a perfect piece of fruit from a tree in Eden — "
     "a fig or pomegranate, large and ripe, "
     "surrounded by abundance on every side, "
     "the ease and joy of life in the garden before the fall, "
     "cinematic close-up of Adam's hand and the fruit he is permitted to eat. "
     + CINEMATIC),

    (100, "creation", "100_except_one.jpg",
     "except one. Do not eat from the tree of the knowledge of good and evil.",
     "Close-up on the Tree of Knowledge — "
     "looking up at the red fruit hanging heavy, a single piece at the forefront, "
     "perfect, beautiful, deeply red, glistening, irresistible, "
     "yet the shadow on it darker than the rest of the garden, "
     "the ONE exception to paradise's freedom, "
     "macro cinematic close-up of the forbidden fruit. "
     + CINEMATIC),

    (101, "creation", "101_in_the_day_you_eat.jpg",
     "For in the day you eat of it,",
     "Adam standing before the Tree of Knowledge, face serious and attentive — "
     "a young Middle Eastern man with dark curly hair and bronze skin, "
     "looking at the tree with a mix of understanding and gravity, "
     "the divine golden light touching his face as he receives the warning, "
     "cinematic medium close-up of Adam receiving the commandment. "
     + CINEMATIC),

    (102, "creation", "102_surely_die.jpg",
     "you will surely die. It was a single command,",
     "The Tree of Knowledge seen from a distance — "
     "standing alone in a small clearing, "
     "the rest of the garden stretching beautifully in every direction, "
     "a visual sense of the single boundary in a world of freedom, "
     "one dark tree among hundreds of light-filled ones, "
     "cinematic wide shot showing the single exception in paradise. "
     + CINEMATIC),

    (103, "creation", "103_single_boundary.jpg",
     "a single boundary, in a world overflowing with abundance.",
     "Looking out from inside Eden — fruit trees and flowers stretching to the horizon, "
     "rivers, animals, beauty in every direction, total abundance, "
     "and in the far background, barely visible, the one forbidden tree, "
     "showing the proportion: one boundary, infinite freedom, "
     "cinematic wide establishing shot of Eden's overwhelming abundance. "
     + CINEMATIC),

    (104, "creation", "104_adam_was_alone.jpg",
     "But Adam was alone,",
     "Adam sitting alone on a mossy rock beside a crystal river in Eden — "
     "a powerfully built young Middle Eastern man with dark curly hair, early 30s, "
     "surrounded by animals but none is his companion, "
     "his expression: quiet, searching, a longing for something he cannot name, "
     "animals nearby but none beside him as equal, "
     "cinematic medium shot, warm dusk light, solitary Adam in paradise. "
     + CINEMATIC),

    (105, "creation", "105_not_good_to_be_alone.jpg",
     "and God said it was not good for man to be alone.",
     "Adam standing alone against the sunset sky of Eden — "
     "silhouetted against blazing orange-gold sky, "
     "all the beauty of paradise around him, yet the loneliness palpable, "
     "the divine golden light beside him warm and empathetic, "
     "cinematic wide shot of Adam alone at sunset, about to change. "
     + CINEMATIC),

    (106, "creation", "106_adam_slept.jpg",
     "So as Adam slept, God formed a companion for him,",
     "Adam lying in a deep supernatural sleep on the soft grass of Eden — "
     "a powerfully built young Middle Eastern man, face peaceful and still, "
     "a divine ethereal golden-white glow hovering over his side, "
     "the beginning of something miraculous happening as he sleeps, "
     "cinematic overhead medium shot, warm golden light on sleeping Adam. "
     + CINEMATIC),

    (107, "creation", "107_bone_of_his_bone.jpg",
     "bone of his bone,",
     "Close-up of the golden divine light drawing a rib from Adam's side — "
     "the rib glowing as it is separated, surrounded by a soft luminous mist, "
     "no blood, no pain — only the miraculous gentle process of creation from within creation, "
     "the rib beginning to transform in the divine light, "
     "macro cinematic close-up of the miraculous moment. "
     + CINEMATIC),

    (108, "creation", "108_flesh_of_his_flesh.jpg",
     "flesh of his flesh.",
     "The silhouette of a woman forming in swirling golden divine light — "
     "the shape distinctly feminine, beautiful, "
     "still forming, still emerging from the golden mist, "
     "Adam still sleeping in the background, "
     "the companion taking shape from his very substance, "
     "cinematic medium shot of Eve forming in divine light. "
     + CINEMATIC),

    (109, "creation", "109_her_name_was_eve.jpg",
     "Her name was Eve.",
     "Portrait of Eve — "
     "a strikingly beautiful young Middle Eastern woman, early 20s, "
     "long dark wavy hair, olive skin, deep dark almond-shaped eyes, "
     "standing in the soft golden light of Eden's morning, "
     "an expression of wonder and awakening, newly created and alive, "
     "close-up portrait, looking directly at camera, natural and radiant. "
     + CINEMATIC),

    (110, "creation", "110_for_a_time.jpg",
     "And for a time, for how long we do not know,",
     "Adam and Eve walking hand-in-hand through the paradise garden of Eden — "
     "he is tall and dark-haired with bronze skin; she has long dark wavy hair, olive skin, serene joy, "
     "the lush garden surrounding them in all its glory: fruit trees, rivers, animals at peace, "
     "golden afternoon light falling across the perfect couple in their perfect world, "
     "cinematic wide shot of Adam and Eve together in paradise before the fall. "
     + CINEMATIC),
]

# ── API functions ──────────────────────────────────────────────────────────────

def load_env():
    env = {}
    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def generate_replicate(prompt, out_path, attempt=0):
    import replicate
    output = replicate.run(
        "google/nano-banana-2",
        input={"prompt": prompt, "aspect_ratio": "16:9", "output_format": "jpg"}
    )
    url = str(output[0]) if isinstance(output, list) else str(output)
    urllib.request.urlretrieve(url, out_path)


def generate_google(prompt, out_path, key, attempt=0):
    import requests, base64
    resp = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-fast-generate-001:predict?key={key}",
        json={
            "instances": [{"prompt": prompt}],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9",
                "safetyFilterLevel": "block_only_high",
                "personGeneration": "allow_adult"
            }
        },
        timeout=90
    )
    if resp.status_code != 200:
        raise RuntimeError(resp.json().get("error", {}).get("message", resp.text[:200]))
    data = resp.json()
    predictions = data.get("predictions", [])
    if not predictions or "bytesBase64Encoded" not in predictions[0]:
        raise RuntimeError(f"Unexpected response: {str(data)[:200]}")
    img_bytes = base64.b64decode(predictions[0]["bytesBase64Encoded"])
    out_path.write_bytes(img_bytes)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--api", choices=["replicate", "google"], default="replicate")
    parser.add_argument("--start", type=int, default=1, help="Start from scene number")
    parser.add_argument("--end", type=int, default=9999)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    env = load_env()

    if args.api == "replicate":
        api_key = env.get("REPLICATE_API_KEY") or env.get("REPLICATE_API_TOKEN", "")
        if not api_key:
            raise RuntimeError("REPLICATE_API_KEY not set in .env")
        os.environ["REPLICATE_API_TOKEN"] = api_key
        import replicate
        gen_fn = generate_replicate
        key = None
        cost_per_image = 0.0325
    else:
        key = env.get("GOOGLE_AI_STUDIO_KEY", "")
        if not key:
            raise RuntimeError("GOOGLE_AI_STUDIO_KEY not set in .env")
        gen_fn = None
        cost_per_image = 0.02

    dirs = {"cold_open": COLD_OPEN_DIR, "creation": CREATION_DIR}

    scenes_to_run = [s for s in SCENES if args.start <= s[0] <= args.end]
    total = len(scenes_to_run)
    already_done = sum(1 for s in scenes_to_run if (dirs[s[1]] / s[2]).exists())

    print(f"\nStory Image Generator — Cold Open + The Creation")
    print(f"API: {args.api.upper()} | ~${cost_per_image:.4f}/image")
    print(f"Scenes {args.start}-{min(args.end, 110)}: {total} total | {already_done} cached | {total - already_done} to generate")
    print(f"Estimated cost: ~${(total - already_done) * cost_per_image:.2f}")
    print()

    if args.dry_run:
        print("=== DRY RUN — prompts only ===\n")
        for scene_num, dir_key, filename, narration, prompt in scenes_to_run:
            out = dirs[dir_key] / filename
            status = "CACHED" if out.exists() else "WILL GENERATE"
            print(f"[{scene_num:03d}] {status} — {filename}")
            print(f"  Narration: {narration}")
            print(f"  Prompt: {prompt[:120]}...")
            print()
        return

    generated = 0
    failed = 0
    cost_spent = 0.0

    for i, (scene_num, dir_key, filename, narration, prompt) in enumerate(scenes_to_run, 1):
        out = dirs[dir_key] / filename
        if out.exists():
            print(f"[{scene_num:03d}/{max(s[0] for s in scenes_to_run):03d}] {filename} — cached")
            continue

        print(f"[{scene_num:03d}] Generating: {filename}")
        print(f"  Narration: \"{narration}\"")

        for attempt in range(5):
            try:
                if args.api == "replicate":
                    generate_replicate(prompt, out)
                else:
                    generate_google(prompt, out, key)
                cost_spent += cost_per_image
                generated += 1
                print(f"  → saved ({out.stat().st_size // 1024}KB) | total cost: ~${cost_spent:.2f}")
                break
            except Exception as exc:
                msg = str(exc)
                if "402" in msg or "insufficient" in msg.lower() or "credit" in msg.lower():
                    print(f"  CREDITS EXHAUSTED. Add credits and restart.")
                    sys.exit(1)
                if "429" in msg or "throttled" in msg.lower() or "rate" in msg.lower() or "quota" in msg.lower():
                    wait = 15 * (2 ** attempt)
                    print(f"  Rate-limited (attempt {attempt+1}/5) — sleeping {wait}s")
                    time.sleep(wait)
                    continue
                if attempt < 4:
                    wait = 5 * (2 ** attempt)
                    print(f"  Error (attempt {attempt+1}/5): {msg[:80]} — retrying in {wait}s")
                    time.sleep(wait)
                else:
                    print(f"  FAILED after 5 attempts: {msg[:120]}")
                    failed += 1

    print(f"\nDone: {generated} generated, {failed} failed")
    print(f"Total spend: ~${cost_spent:.2f}")
    print(f"Output: {COLD_OPEN_DIR} and {CREATION_DIR}")


if __name__ == "__main__":
    main()
