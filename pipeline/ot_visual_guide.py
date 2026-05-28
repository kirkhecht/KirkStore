"""
Old Testament documentary visual style guide.
Provides section-specific image prompt templates, negative prompts,
and cinematic style instructions for each of the 10 chapters.
"""

# ── Base cinematic style for all OT prompts ────────────────────────────────────
OT_BASE_STYLE = (
    "ultra photorealistic cinematic film still, dramatic chiaroscuro lighting, "
    "ancient Near Eastern setting, historically grounded, deep rich colours, "
    "film grain, anamorphic lens bokeh, 16:9 widescreen composition, "
    "no text, no watermarks, no modern elements"
)

OT_NEGATIVE = (
    "cartoon, anime, illustration, painting, watercolour, religious iconography style, "
    "European Renaissance art, modern clothing, modern buildings, "
    "CGI uncanny valley, plastic texture, flat lighting, "
    "text, watermark, logo, distorted anatomy"
)

# ── Per-emotion lighting/colour modifiers ─────────────────────────────────────
EMOTION_STYLE: dict[str, str] = {
    "awe":           "divine golden light breaking through darkness, volumetric rays, vast scale",
    "dark_and_tense":"deep shadow and smoke, storm clouds, blood-red sky at horizon, high contrast",
    "dramatic":      "high contrast directional light, deep shadow, intense focal moment, shallow DOF",
    "hopeful":       "warm sunrise light, soft golden hour glow, open horizon, optimistic framing",
    "solemn":        "muted warm tones, single torch or fire light, heavy atmosphere, still composition",
    "mysterious":    "deep shadow, flickering torchlight, desert night, starlit sky, hidden forms",
    "triumphant":    "golden light, wide epic scope, raised banners, crowds, warm triumphant palette",
    "epic_grandeur": "sweeping aerial perspective, monumental architecture, vast landscape, awe-inspiring scale",
}

# ── Per-chapter environment descriptions ──────────────────────────────────────
CHAPTER_ENVIRONMENT: dict[int, str] = {
    1:  "primordial ancient earth, pre-historic wilderness, desert plains, early human settlements",
    2:  "ancient Mesopotamian city-state, Canaan rolling hills, desert trade routes, Nile delta Egypt",
    3:  "New Kingdom Egypt, mud-brick slave quarters, Nile River valley, Sinai peninsula desert",
    4:  "Sinai wilderness, desert canyons, stone mountains, Tabernacle tent complex",
    5:  "Canaan hill country, Jordan River valley, walled ancient cities, wheat fields",
    6:  "ancient Israelite hill towns, Philistine coastal cities, Jerusalem early fortifications",
    7:  "Jerusalem at peak glory, massive hewn stone Temple, Phoenician-influenced architecture, Mount Carmel",
    8:  "Assyrian siege warfare, Babylon approaching, Jerusalem walls, burning ancient cities",
    9:  "Neo-Babylonian empire, massive ziggurat city, Persian palace architecture, exile communities",
    10: "Persian palace of Susa, ruined Jerusalem, Second Temple construction, Hellenistic period",
}

# ── Section-level visual overrides ────────────────────────────────────────────
SECTION_VISUAL: dict[str, str] = {
    # Chapter 1
    "Cold Open":               "absolute void of space, primordial darkness, first photon of light emerging from infinite black",
    "The Creation":            "God's light splitting darkness over formless waters, earth taking shape, stars being placed in black sky",
    "Adam and Eve":            "lush Garden of Eden untouched by sin, ancient paradise, towering fruit trees, crystal rivers",
    "The Fall":                "Eve reaching for forbidden fruit in garden, serpent coiled in tree, golden light fading",
    "Cain and Abel":           "two men at stone altar in open field, one kneeling in prayer, one standing in silent rage",
    "Corruption of Mankind":   "ancient city streets filled with violence, dark smoke, crumbling civilization",
    "Noah and the Flood":      "enormous wooden ark on mountain hillside, animals approaching in pairs, storm clouds gathering",
    "The Covenant with Noah":  "rainbow arcing over flooded plain, Noah on knees at stone altar, dove returning with olive branch",
    "The Tower of Babel":      "massive ziggurat rising from flat plain of Shinar, thousands of workers, scaffolding, confusion below",

    # Chapter 2
    "The Calling of Abraham":  "elderly man standing at edge of city gates at night, vast desert ahead, stars bright overhead",
    "The Three Visitors":      "three mysterious figures approaching a Bedouin tent under ancient oaks, heat shimmer, midday",
    "Sodom and Gomorrah":      "twin ancient cities consumed by fire from sky, massive columns of smoke rising, fleeing figures",
    "The Binding of Isaac":    "elderly man with raised knife over bound young son on stone altar, ram caught in thicket",
    "Jacob's Ladder":          "sleeping man with stone pillow, blazing stairway of light ascending to heaven, angels moving on it",
    "Jacob Wrestles God":      "two figures locked in struggle at river's edge in darkness, dawn light breaking at horizon",
    "David and Goliath":       "small young shepherd boy with sling facing enormous armoured warrior across valley floor",
    "Joseph and His Brothers": "young man thrown into empty stone cistern by group of brothers, camel caravan passing in distance",

    # Chapter 3
    "The Burning Bush":        "solitary shepherd before single burning bush that is not consumed, sandals off, face hidden",
    "The Ten Plagues":         "Nile River running red with blood, swarms of locusts blackening sky over Egyptian crops",
    "The Passover":            "Hebrew family eating in robes with staffs, blood painted on doorposts, dark streets of Egypt outside",
    "The Red Sea":             "walls of water towering on both sides, millions of Hebrews walking across dry seabed under stars",

    # Chapter 4
    "The Mountain of God":     "Mount Sinai wreathed in thick smoke and fire, lightning cracking summit, two million Israelites below",
    "The Ten Commandments":    "stone tablets glowing with carved divine text, held by aged weathered hands, mountain fire behind",
    "The Golden Calf":         "golden idol gleaming before dancing crowd, Moses descending from smoke-covered mountain above",
    "The Tabernacle":          "portable sanctuary golden lampstand glowing inside linen tent, cloud of glory above, desert camp",
    "The Death of Moses":      "solitary old man on mountain summit, gazing at sunlit promised land across Jordan far below",

    # Chapter 5
    "Crossing the Jordan":     "priests carrying ark into flooded Jordan river, water walls rising, millions crossing dry ground",
    "The Fall of Jericho":     "massive stone walls collapsing in cloud of dust and rubble, trumpets sounding, army outside",
    "Gideon":                  "three hundred men with torches and clay pots surrounding night-time enemy camp, chaos erupting",
    "Samson":                  "giant muscular man pushing stone pillars of crowded temple, roof beginning to collapse",
    "The Book of Ruth":        "woman gleaning grain in ancient Judean barley field, golden harvest light, male overseer watching kindly",

    # Chapter 6
    "Hannah and Samuel":       "woman weeping and praying at Tabernacle entrance, lips moving silently, oil lamps burning",
    "Samuel Called":           "boy awaking in lamplight of Tabernacle at night, listening to unseen voice, ancient sanctuary",
    "David and Goliath":       "teenage shepherd running toward armoured giant in wide valley, stone in sling, two armies watching",
    "The Ark Comes Home":      "King David dancing before golden Ark of Covenant in Jerusalem streets, crowd celebrating",
    "David and Bathsheba":     "king on palace roof at night overlooking moonlit Jerusalem, figure bathing on rooftop below",
    "Absalom's Rebellion":     "beautiful long-haired prince on horse fleeing through forest, hair caught in oak branches",

    # Chapter 7
    "The Dream at Gibeon":     "young king sleeping on stone floor beside smoking altar under open night sky full of stars",
    "Building the Temple":     "massive dressed stones being set with no iron tools heard, cedar pillars gleaming, craftsmen working",
    "The Temple Dedicated":    "Jerusalem Temple filled with thick golden cloud, priests prostrate on floor overwhelmed by glory",
    "Mount Carmel":            "lone prophet before drenched stone altar, fire falling from clear sky, 450 prophets of Baal watching",
    "The Still Small Voice":   "prophet collapsed in cave entrance on Mount Sinai, wind and fire passing, then utter stillness",
    "The Chariot of Fire":     "two prophets walking in field, fiery chariot of horses descending between them, whirlwind rising",

    # Chapter 8
    "Isaiah in the Temple":    "young man prostrate on Temple floor, seraphim with six wings flying above throne of fire and smoke",
    "Sennacherib at Gates":    "Assyrian army camp circling Jerusalem walls, herald shouting insults at defenders on rampart",
    "The Temple Burns":        "Jerusalem Temple engulfed in orange fire and black smoke, Babylonian soldiers watching, weeping captives",
    "The Weeping Prophet":     "solitary old prophet sitting in smoking ruins of Jerusalem, ash and broken stone all around",

    # Chapter 9
    "The Fiery Furnace":       "three young men standing unbound and unharmed inside roaring furnace, fourth mysterious figure with them",
    "The Writing on the Wall": "ghostly disembodied hand writing glowing script on white plaster wall of crowded feast hall",
    "The Dry Bones":           "prophet standing in vast valley covered with bleached bones, breath entering them, army rising",
    "The Lions Den":           "old man kneeling in prayer in stone pit surrounded by calm lions, shaft of light from above",

    # Chapter 10
    "The Decree of Cyrus":     "Persian king issuing proclamation in grand court, Jewish elders weeping with joy as they hear it",
    "The Foundation Laid":     "old men weeping and young men shouting for joy simultaneously over new Temple foundation stones",
    "For Such a Time — Esther":"young queen in royal robes approaching king's throne room, heart pounding, golden scepter extended",
    "The Great Reading":       "Ezra on wooden platform reading scroll aloud to thousands standing in Jerusalem square at dawn",
    "Closing Transition":      "night road to Bethlehem, single bright star rising on horizon, young couple on donkey approaching",
}


def build_prompt(section_title: str, chapter_num: int, emotion: str,
                 setting: str | None = None, key_figures: list[str] | None = None) -> str:
    """Build a full image generation prompt for a specific section."""
    env    = CHAPTER_ENVIRONMENT.get(chapter_num, "ancient biblical landscape")
    emo    = EMOTION_STYLE.get(emotion, EMOTION_STYLE["solemn"])
    visual = SECTION_VISUAL.get(section_title, setting or "ancient Near Eastern scene")

    figures = ""
    if key_figures:
        figures = f"featuring {', '.join(key_figures)}, "

    return (
        f"{visual}, {figures}"
        f"{emo}, "
        f"{env}, "
        f"{OT_BASE_STYLE}"
    )


def get_negative_prompt() -> str:
    return OT_NEGATIVE
