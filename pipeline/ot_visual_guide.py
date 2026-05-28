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

# ── Per-chapter color grading guidance ────────────────────────────────────────
CHAPTER_COLOR_GRADE: dict[int, str] = {
    1:  "deep navy and gold for cold open, expanding to warm golden full colour for creation, "
        "saturated greens and soft golden hour for Eden, colour draining to muted tones for the fall",
    2:  "sun-bleached desert ochres and warm whites for Abraham's journey, "
        "deep midnight blues with brilliant white starlight for covenant, "
        "red-orange hellfire for Sodom, warm intimate lamplight for family scenes",
    3:  "bleached oranges and browns under harsh oppressive sun for slavery, "
        "deep blues of the Nile contrasted with warm interior lamplight for Moses' birth, "
        "Egyptian palace gold and lapis lazuli, blood red for the plagues, "
        "turquoise and white for the Red Sea crossing",
    4:  "sun-bleached desert tones darkening as Sinai approaches, "
        "smoky blacks and deep storm blues with sudden orange-red fire for the theophany, "
        "warm gold and linen white for Tabernacle interiors, "
        "dusty muted tones for forty years of wandering",
    5:  "harder, more weathered, grounded in war and survival — "
        "Bronze Age to early Iron Age colour palette, "
        "warm harvest gold for Ruth, dark oppressive tones for the dark end of Judges",
    6:  "late Iron Age village settings shifting through military camps "
        "into rising splendour of David's united kingdom — "
        "deep cave shadows for wilderness years, triumphant warm gold for the Ark",
    7:  "richest and most opulent in the documentary — Solomon's court in deep gold and crimson, "
        "Queen of Sheba caravan in exotic jewel tones, "
        "sharp contrast to Elijah's bleached wilderness and storm-grey Mount Carmel",
    8:  "progressively darkening — Elisha's pastoral warmth giving way to "
        "harsh desert Assyrian conquest, gathering shadow of Babylonian siege, "
        "ending in ash grey and smoke black for Jerusalem's fall",
    9:  "richest outside Solomon's Temple — Babylon is beautiful in foreign dangerous colours: "
        "lapis lazuli blue tiles, gold leaf, deep purples; "
        "the furnace in blinding white-orange; exile communities in warm earth tones",
    10: "muted, domestic, human-scale — fragile warmth of the returning community, "
        "Second Temple in humble grey stone, Esther's Persian court in opulent gold-crimson, "
        "closing in deep silent blue before the star rises over Bethlehem",
}

# ── Section-level visual overrides ────────────────────────────────────────────
SECTION_VISUAL: dict[str, str] = {

    # ── Chapter 1: Creation to Babel ──────────────────────────────────────────
    "Cold Open":
        "vast cosmic void, deep black space with faintest blue mist, single beam of warm golden light "
        "beginning to pierce the darkness, volumetric light, infinite darkness before creation",
    "The Creation":
        "first light of creation bursting through cosmic darkness, golden divine radiance illuminating "
        "a void, god rays, waters separating from sky, mountains rising from primordial sea, "
        "silhouette of man being formed from red clay and dust, no visible face of God",
    "Adam and Eve":
        "lush primordial garden at golden hour, towering ancient trees heavy with glowing fruit, "
        "two trees centered in frame, two silhouettes walking hand in hand through tall grass, ethereal warm light",
    "The Fall":
        "coiled serpent on bark of ancient tree, iridescent scales, intelligent eye glinting, "
        "woman's hand reaching toward glowing forbidden fruit, golden light filtering through leaves, "
        "two figures crouched hidden among large leafy plants, ashamed and afraid, dramatic shadows",
    "Cain and Abel":
        "two stone altars side by side in barren field at dusk, one with smoke rising straight to heaven, "
        "other smoke blowing sideways, two brothers — one kneeling in prayer, one standing in silent rage",
    "Corruption of Mankind":
        "aerial shot of ancient sprawling city at dusk, smoke rising from many fires, "
        "vaguely Mesopotamian architecture, crumbling civilization, foreboding",
    "Noah and the Flood":
        "old patriarch with flowing white beard on hillside, gazing at sky as first dark clouds gather, "
        "enormous wooden ark on mountain hillside, animals approaching in pairs, storm clouds massing",
    "The Covenant with Noah":
        "close-up of brilliant full rainbow arching across clearing sky over fresh wet landscape, "
        "golden hour, Noah on knees at stone altar, dove returning with olive branch",
    "The Tower of Babel":
        "vast flat plain of Shinar at dawn, ancient peoples migrating in caravans toward central settlement, "
        "massive ziggurat rising from flat plain, thousands of workers, scaffolding, confusion below",
    "Closing Transition":
        "lone elderly man standing at gate of ancient Mesopotamian city at dawn, gazing at horizon, "
        "vast desert ahead, stars bright overhead, hopeful and mysterious",

    # ── Chapter 2: The Patriarchs ─────────────────────────────────────────────
    "The Calling of Abraham":
        "bustling ancient Mesopotamian marketplace, merchants, scribes, soldiers, temple in background, "
        "elderly man at edge of city gates at night, vast desert ahead, stars bright overhead",
    "The Covenant":
        "vast desert sky at night, infinite stars, single small silhouette of elderly man "
        "with head tilted back gazing upward, starlit covenant in Canaan desert",
    "The Three Visitors":
        "three robed travelers approaching Bedouin-style tent under ancient oak trees in midday heat, "
        "three mysterious figures at Mamre, heat shimmer, sacred hospitality",
    "Sodom and Gomorrah":
        "wide aerial of ancient walled city at twilight, smoke from fires rising, "
        "twin ancient cities consumed by fire from sky, massive columns of smoke, fleeing figures",
    "The Birth of Isaac":
        "elderly woman holding newborn baby in her arms, face streaked with tears of joy, "
        "soft warm candlelit interior, intimate, miraculous birth",
    "The Binding of Isaac":
        "elderly man sitting alone by small fire at night, eyes haunted, "
        "elderly man with raised knife over bound young son on stone altar, ram caught in thicket",
    "Sarah and Rebekah":
        "aged patriarch kneeling at entrance of stone burial cave, head bowed, mourning, "
        "young woman with jar on shoulder approaching stone well surrounded by sheep, golden hour",
    "Jacob and Esau":
        "pregnant woman kneeling on ground in prayer, hand on swollen belly, "
        "two sons — one ruddy and rough, one smooth and thoughtful — in tent camp, tense family scene",
    "Jacob's Ladder":
        "young man sleeping outdoors on open ground, head resting on single stone, "
        "vast starry night sky above, blazing stairway of light ascending to heaven, angels moving on it",
    "Jacob Leah Rachel":
        "young woman with jar on shoulder approaching stone well surrounded by sheep, golden hour, "
        "man working in distant fields, uncle Laban's household in Haran",
    "Jacob Wrestles God":
        "lone man at edge of moonlit river at night, absolute isolation, "
        "two figures locked in struggle at river's edge in darkness, dawn light breaking at horizon",
    "The Reconciliation":
        "man limping across open plain bowing low to ground multiple times, "
        "two brothers embracing with tears in open land of Canaan",
    "Joseph and His Brothers":
        "teenage boy in elaborate multicolored robe walking through tall grass, "
        "brothers watching from distance with cold expressions, young man thrown into empty stone cistern, "
        "camel caravan passing in distance",
    "Joseph in Egypt":
        "young Hebrew man in fine Egyptian linen standing in colonnaded Egyptian villa, "
        "young man kneeling in Egyptian prison, hands chained, face resolute",
    "Dreams of Pharaoh":
        "two Egyptian officials in dim prison cell, one looking troubled, "
        "young Hebrew man standing before seated Pharaoh on great throne, interpreting dreams",
    "The Brothers Return":
        "ten travel-worn Hebrew brothers in dusty robes bowing low before Egyptian official "
        "seated on raised dais, grain stores of Egypt, dramatic reunion",
    "Jacob Comes to Egypt":
        "vast caravan of Hebrew families, tents, flocks, and wagons moving across desert "
        "from Canaan into Egypt, epic wide shot, dust rising, hope and fear mixed",

    # ── Chapter 3: Exodus ─────────────────────────────────────────────────────
    "The Birth of Moses":
        "Egyptian soldiers patrolling Hebrew slave quarters at night, torches in hand, doors closed in fear, "
        "Hebrew mother placing woven basket in Nile reeds at dawn, Pharaoh's daughter at riverside",
    "Moses Flees Egypt":
        "young man in Egyptian royal linen walking through colonnaded palace, hieroglyphs covering walls, "
        "same man in rough shepherd's cloak crossing empty Sinai desert, fugitive and free",
    "The Burning Bush":
        "elderly shepherd with long staff walking through rocky wilderness at foot of mountain, "
        "solitary shepherd before single burning bush that is not consumed, sandals off, face hidden",
    "Moses Returns":
        "two robed Hebrew brothers walking up vast Egyptian temple staircase, "
        "dwarfed by colossal columns and statuary, Moses and Aaron before Pharaoh",
    "Let My People Go":
        "Hebrew elder standing before enthroned Pharaoh surrounded by guards and priests, "
        "confrontation in throne room of Egypt, staff becoming serpent, battle of wills",
    "The Ten Plagues":
        "Nile River running red with blood, swarms of locusts blackening sky over Egyptian crops, "
        "hailfire falling on Egypt, darkness over the land, death angel passing over",
    "The Passover":
        "young Hebrew shepherd carrying perfect spotless white lamb at dusk, "
        "Hebrew family eating in robes with staffs, blood painted on doorposts, dark streets of Egypt outside",
    "The Exodus":
        "vast columns of Hebrews and their flocks walking through desert, "
        "towering pillar of cloud rising before them by day, pillar of fire by night, "
        "two million people moving as one body, epic wide shot",
    "The Red Sea":
        "walls of water towering on both sides, millions of Hebrews walking across dry seabed under stars, "
        "Egyptian chariots pursuing at the shore's edge, sea wall beginning to collapse",
    "The Song of Moses":
        "older prophet standing on rocky shore at dawn with arms raised toward sky, "
        "Miriam with tambourine leading women in dance on eastern shore, triumphant",

    # ── Chapter 4: The Law and the Wilderness ─────────────────────────────────
    "The Mountain of God":
        "vast Hebrew camp spread across desert plain at foot of towering mountain, "
        "Mount Sinai wreathed in thick smoke and fire, lightning cracking summit, two million Israelites below",
    "The Ten Commandments":
        "vast smoking mountain seen from Hebrews far below, sky split with lightning, "
        "stone tablets glowing with carved divine text, held by aged weathered hands, mountain fire behind",
    "The Covenant in Blood":
        "old prophet reading aloud from scroll before vast crowd at foot of mountain, "
        "Moses at altar, blood of covenant sprinkled on assembled people",
    "The Golden Calf":
        "golden idol gleaming before dancing crowd, "
        "Moses descending from smoke-covered mountain above, two stone tablets in hand",
    "The Radiant Face":
        "aged prophet kneeling on rocky mountain summit, head bowed, hand shielding eyes from unseen light, "
        "Moses with veil over radiant glowing face descending to the camp",
    "The Tabernacle":
        "Hebrew artisans working with hammers and chisels on gold-overlaid wood, intricate craftwork, "
        "portable sanctuary golden lampstand glowing inside linen tent, cloud of glory above, desert camp",
    "The Law":
        "aged priest in elaborate embroidered robes — blue, purple, scarlet, gold, breastplate of twelve stones — "
        "biblical high priest Aaron, sacred ceremonial dress, Tabernacle interior",
    "The Twelve Spies":
        "twelve men in dust-stained robes leaving vast camp at edge of wilderness, "
        "walking toward distant hills, Caleb and Joshua carrying enormous cluster of grapes on pole",
    "Forty Years":
        "endless desert stretching to horizon in every direction, Hebrew camp of tents, "
        "sun beating down, generation wandering — the same landscape year after year",
    "Death of Miriam Aaron":
        "elderly woman lying still in tent, surrounded by mourning women, Miriam's death, "
        "Aaron in high priest's robes on mountain summit, death on Mount Hor",
    "Balak and Balaam":
        "worried king standing on balcony looking out at vast Hebrew camp below his walls, "
        "prophet on donkey on Moabite road, angel with sword blocking the path",
    "The Farewell of Moses":
        "aged prophet with long white beard standing before vast assembly of Hebrews, "
        "plains stretching behind them, Jordan River visible in distance, Moses' final sermon",
    "The Death of Moses":
        "aged prophet climbing steep mountain path alone at sunrise, staff in hand, final ascent, "
        "solitary old man on mountain summit, gazing at sunlit promised land across Jordan far below",

    # ── Chapter 5: The Promised Land ──────────────────────────────────────────
    "Crossing the Jordan":
        "wide flooded Jordan River running brown and powerful through spring valley, "
        "priests carrying Ark into flooded Jordan, water walls rising, millions crossing dry ground",
    "The Fall of Jericho":
        "Hebrew army marching silently around great walled city, day after day, "
        "massive stone walls collapsing in cloud of dust and rubble, trumpets sounding, army outside",
    "The Conquest":
        "Gibeonites in worn travel-clothes with moldy bread and patched wineskins, Canaanite cities falling, "
        "Joshua's army in battle across hill country, Israel claiming the land",
    "Dividing the Land":
        "older Hebrew leader sitting in tent with elders around him, large map of Canaan on ground, "
        "land allotment ceremony, tribes receiving their inheritance",
    "Choose This Day":
        "aged warrior standing before assembled nation at Shechem, gray hair and weathered face, "
        "Joshua's farewell challenge: choose this day whom you will serve",
    "The Cycle of Judges":
        "young generation of Hebrew children playing in village, oblivious to the past, "
        "the cycle beginning again — sin, oppression, cry for help, deliverance, peace, repeat",
    "Deborah and Barak":
        "prophetess sitting under palm tree judging Israel, Deborah beneath palm, "
        "Hebrew army routing Canaanite chariots in Kishon Valley, Jael and tent peg",
    "Gideon":
        "young Hebrew man hiding inside wine press threshing wheat, anxious face, "
        "three hundred men with torches and clay pots surrounding night-time enemy camp, chaos erupting",
    "Samson":
        "angelic figure standing in wheat field at sunset before Hebrew woman, no clear face, "
        "giant muscular man pushing stone pillars of crowded temple, roof beginning to collapse",
    "Dark End of Judges":
        "single oil lamp burning low in empty Hebrew village street at night, "
        "tribal Israel in chaos and violence, the darkest period, 'everyone did what was right in their own eyes'",
    "The Book of Ruth":
        "woman gleaning grain in ancient Judean barley field, golden harvest light, "
        "Ruth and Naomi on dusty road, two women alone, loyal companionship across cultures",

    # ── Chapter 6: The Rise of the Kingdom ───────────────────────────────────
    "Hannah and Samuel":
        "Hebrew family gathered for feast, woman sitting alone at edge not eating, Hannah weeping, "
        "woman weeping and praying at Tabernacle entrance, lips moving silently, oil lamps burning",
    "Samuel Called":
        "small boy sleeping in priestly linen on low cot inside ancient sanctuary, "
        "single oil lamp burning low nearby, boy awaking in lamplight of Tabernacle, listening to unseen voice",
    "The Ark Captured":
        "Hebrew warriors marching with gold Ark of Covenant onto battlefield at dawn, "
        "Philistine victory, Eli falling backward from his chair at the news, Ark carried into captivity",
    "Give Us a King":
        "aged prophet sitting before council of demanding Hebrew elders, "
        "Samuel before the assembly, Israel's demand for a king, the last judge's sorrow",
    "Saul Anointed":
        "tall handsome young man in dusty travel clothes searching for lost donkeys across rocky hills, "
        "Samuel privately anointing Saul with oil, tall Israelite standing head and shoulders above the rest",
    "The Fall of Saul":
        "king impatiently standing before stone altar with smoke rising, face conflicted, "
        "Saul's unlawful sacrifice at Gilgal, Samuel's arrival and rebuke, rejection of the king",
    "The Boy in Bethlehem":
        "aged prophet walking with horn of oil into small Hebrew hill town at dawn, "
        "Samuel before Jesse's sons, the youngest shepherd boy called from the fields",
    "David and Goliath":
        "wide valley landscape between two opposing hilltops, two armies arrayed on either side, "
        "small young shepherd boy with sling facing enormous armoured warrior across valley floor",
    "Jonathan and David":
        "Hebrew women dancing in streets celebrating, tambourines raised, joyful victory, "
        "Jonathan and David swearing covenant friendship, inseparable bond",
    "The Wilderness Years":
        "young man running across desert hills at dawn, viewed from great distance, David fleeing, "
        "caves of Engedi, desert strongholds, David sparing Saul's life in cave darkness",
    "Death of Samuel":
        "ancient prophet lying still in Hebrew home, family weeping around him, "
        "all Israel mourning, the last era of the judges ending",
    "The Witch of Endor":
        "king in disguise — humble cloak, hood pulled low — walking through dark hills at night, "
        "ghostly apparition of Samuel rising from the ground, Saul's terror",
    "Mount Gilboa":
        "wide shot of mountainside battle at dawn, Hebrew warriors retreating up steep slopes, "
        "King Saul and Jonathan falling in battle, the crown in the dust",
    "David Crowned King":
        "young man being anointed by tribal elders in city of Hebron, "
        "David taking Jerusalem, the City of David established, united kingdom at last",
    "The Ark Comes Home":
        "wide shot of thirty thousand Hebrews escorting gold Ark of Covenant uphill toward city, "
        "King David dancing before golden Ark in Jerusalem streets, crowd celebrating",
    "The Covenant with David":
        "king standing in richly appointed cedar-walled palace, looking out window toward humble tent, "
        "Nathan bringing the eternal covenant promise — David's throne forever",
    "David and Bathsheba":
        "king walking restlessly on high palace rooftop at evening, Jerusalem spread below, "
        "king on palace roof at night overlooking moonlit Jerusalem, figure bathing on rooftop below",
    "Nathan and the Lamb":
        "prophet in modest robes standing alone in king's throne room, "
        "Nathan's parable of the ewe lamb, David's anguished recognition: 'You are the man'",
    "Absalom's Rebellion":
        "young woman in torn robes weeping at door of her brother's house, Tamar, "
        "beautiful long-haired prince on horse fleeing through forest, hair caught in oak branches",
    "The Old King":
        "aged king writing on parchment scroll by lamplight, lyre nearby, David's psalms, "
        "old David on his deathbed giving final charge to young Solomon",

    # ── Chapter 7: The Glory and the Fracture ────────────────────────────────
    "The Dream at Gibeon":
        "vast hilltop altar at twilight, smoke rising from thousand burnt offerings, Gibeon high place, "
        "young king sleeping on stone floor beside smoking altar under open night sky full of stars",
    "The Two Mothers":
        "two women in plain robes standing before young king on throne, "
        "both holding hands toward swaddled infant on low table between them, Solomon's wisdom",
    "The Golden Age":
        "aerial wide shot of Jerusalem at golden hour, prosperous, surrounded by green hills and cultivated fields, "
        "Solomon's reign at height, peace from Dan to Beersheba",
    "Building the Temple":
        "massive cedar logs being floated down coastal river at dawn, workers guiding them, "
        "massive dressed stones being set with no iron tools heard, cedar pillars gleaming, craftsmen working",
    "The Temple Dedicated":
        "Jerusalem Temple filled with thick golden cloud, priests prostrate on floor overwhelmed by glory, "
        "Solomon kneeling before the whole assembly, fire falling from heaven consuming the offerings",
    "The Queen of Sheba":
        "vast caravan of camels and elephants crossing desert at sunset, laden with riches, "
        "queen of Sheba at Solomon's court, her breath taken away by his wisdom and splendour",
    "The Fall of Solomon":
        "seven hundred wives in elaborate foreign robes seated in royal hall, "
        "foreign altars on the Mount of Olives, Solomon's heart turning from God in old age",
    "The Kingdom Divided":
        "young new king sitting on late father's throne, listening to demanding northern tribal elders, "
        "Rehoboam's harsh answer, ten tribes tearing away, kingdom split forever",
    "Ahab and Jezebel":
        "king in royal robes on throne in dark hall, queen in elaborate Phoenician dress beside him, "
        "Ahab and Jezebel — Israel's most wicked king and his more wicked queen",
    "Elijah Appears":
        "wild-looking prophet in rough hairy garments and leather belt walking into luxurious palace throne room, "
        "Elijah standing before Ahab, drought announced, three years of silence beginning",
    "The Widow's Oil":
        "Elijah at door of impoverished widow's house in Zarephath, drought landscape, "
        "widow's jar of oil that never ran dry, the miracle of provision in desperate times",
    "Mount Carmel":
        "lone prophet before drenched stone altar, fire falling from clear sky, "
        "450 prophets of Baal watching, the contest on Mount Carmel, God's fire consuming the sacrifice",
    "The Still Small Voice":
        "prophet collapsed in cave entrance on Mount Sinai, wind and fire passing, then utter stillness, "
        "Elijah under broom tree in wilderness, angel touching him, still small voice in the cave",
    "Naboth's Vineyard":
        "green vineyard on hillside next to palace estate, Naboth's inheritance, "
        "Jezebel's letter of false accusation, Naboth stoned, Elijah meeting Ahab in the vineyard",
    "The Chariot of Fire":
        "two prophets walking together along dusty road at dawn, older and younger, "
        "fiery chariot of horses descending between them, whirlwind rising, Elijah taken to heaven",

    # ── Chapter 8: The Fall of the Kingdoms ──────────────────────────────────
    "Ministry of Elisha":
        "young prophet walking dusty roads through Hebrew villages, people watching from doorways, "
        "Elisha's miracles — floating axe head, Shunammite woman's son, healing of Naaman",
    "The Prophets Rise":
        "sun-darkened shepherd in rough sheepskin walking into wealthy northern marketplace, Amos in Samaria, "
        "Hosea in the north, Micah in the Judean hills — voices crying in the wilderness",
    "Fall of Samaria":
        "massive disciplined Assyrian army marching in columns across plain, banners raised, chariots, "
        "Assyrian siege works around Samaria's walls, the northern kingdom's final days",
    "Isaiah in the Temple":
        "young man in fine robes praying in Temple courtyard at dawn, young Isaiah, "
        "then the throne room vision — seraphim with six wings flying above throne of fire and smoke, "
        "young man prostrate on Temple floor overwhelmed",
    "Sennacherib at Gates":
        "Assyrian king Sennacherib enthroned in war camp, surrounded by officers, "
        "Assyrian army camp circling Jerusalem walls, herald shouting insults at defenders on rampart, "
        "185,000 Assyrians struck down overnight, Hezekiah's prayer answered",
    "Darkness of Manasseh":
        "boy of twelve being crowned on great throne, young Manasseh, "
        "Manasseh's desecrated Temple, child sacrifice at Hinnom Valley, darkest reign in Judah's history",
    "The Found Book":
        "eight-year-old boy being crowned on throne, young Josiah, "
        "high priest Hilkiah finding ancient scroll in Temple, Josiah tearing his robes in grief, "
        "the greatest reform in Judah's history",
    "The Call of Jeremiah":
        "young Hebrew man in modest robes alone in small village at dawn, Jeremiah in Anathoth, "
        "the reluctant prophet, 'I do not know how to speak, I am only a child'",
    "The Final Days":
        "massive Babylonian army marching south from great river, Nebuchadnezzar's forces, "
        "Jerusalem under eighteen-month siege, Jeremiah imprisoned, city near its end",
    "The Temple Burns":
        "Babylonian siege works towering around walls of Jerusalem, "
        "Jerusalem Temple engulfed in orange fire and black smoke, Babylonian soldiers watching, weeping captives",
    "The Weeping Prophet":
        "older prophet sitting alone in smoking ruins of city at dusk, head in hands, Jeremiah's lament, "
        "solitary old prophet in smoking ruins of Jerusalem, ash and broken stone all around",

    # ── Chapter 9: The Exile ──────────────────────────────────────────────────
    "The Choice":
        "line of young Hebrew nobles in their teens being inspected by Babylonian officials in palace courtyard, "
        "Daniel and friends selected, the choice not to defile themselves with the king's food",
    "The Statue Dream":
        "troubled emperor sitting awake on his bed in the dark, Nebuchadnezzar's troubled dream, "
        "Daniel before the king interpreting the statue of gold, silver, bronze, iron, and clay",
    "The Fiery Furnace":
        "massive golden statue ninety feet tall standing on vast plain, glittering in sun, image of Dura, "
        "three young men standing unbound and unharmed inside roaring furnace, fourth mysterious figure with them",
    "Madness of the King":
        "emperor sitting on throne dictating personal decree to scribes, Nebuchadnezzar's testimony, "
        "king driven to madness, eating grass like an ox, hair grown long, nails like bird claws",
    "Ezekiel's Vision":
        "solitary Hebrew priest in his thirties sitting alone beside foreign river under vast sky, "
        "Ezekiel by the Chebar, then the overwhelming vision — four living creatures, wheels within wheels, "
        "the throne of God, Ezekiel prostrate on his face",
    "The Strange Acts":
        "prophet kneeling on Babylonian street drawing outline of city on clay tablet on ground, "
        "Ezekiel's enacted prophecies — lying on his side, cooking over dung, shaving his head",
    "The Glory Departs":
        "prophet being lifted in vision, dust rising around his feet, Ezekiel transported in vision, "
        "the glory of the Lord departing from the Temple, rising above the Mount of Olives",
    "The Dry Bones":
        "prophet standing in vast valley covered with bleached bones, breath entering them, army rising, "
        "the valley of dry bones coming to life, tendons forming, flesh covering, breath entering",
    "The Writing on the Wall":
        "vast Babylonian banqueting hall lit by hundreds of torches, thousand lords reclining at long tables, "
        "ghostly disembodied hand writing glowing script on white plaster wall of crowded feast hall",
    "Fall of Babylon":
        "wide aerial view of great city of Babylon at night, walls three hundred feet high, "
        "Euphrates flowing through the heart of the city, Persian army entering, Cyrus victorious",
    "The Lions Den":
        "new Persian emperor on throne with two advisors, aged Hebrew man standing dignified to one side, "
        "old man kneeling in prayer in stone pit surrounded by calm lions, shaft of light from above",
    "Visions of Daniel":
        "aged prophet writing on scroll by lamplight in private chamber, Daniel's visions, "
        "the Ancient of Days on his throne, ten thousand times ten thousand serving him, "
        "one like a Son of Man approaching on the clouds",

    # ── Chapter 10: The Return ────────────────────────────────────────────────
    "The Decree of Cyrus":
        "royal scribe at marble table inscribing long scroll with cuneiform, Cyrus's decree, "
        "Persian king issuing proclamation in grand court, Jewish elders weeping with joy as they hear it",
    "The First Return":
        "heads of Hebrew families gathering in Babylonian house, scrolls open before them, the call to return, "
        "great caravan of returning exiles setting out from Babylon toward Jerusalem",
    "The Altar Rebuilt":
        "Hebrew men carefully clearing rubble from stone platform at dawn, the altar site, "
        "new altar standing in Jerusalem ruins, first sacrifice on the rebuilt altar amid the rubble",
    "The Foundation Laid":
        "Hebrew priests in linen robes blowing trumpets at Temple foundation, old men weeping, "
        "young men shouting for joy simultaneously over new Temple foundation stones",
    "The Long Pause":
        "Samaritan elders approaching Hebrew leaders at foundation site, opposition scrolls, "
        "abandoned foundation lying quiet for fifteen years, Jerusalem ruins and silent Temple Mount",
    "Haggai and Zechariah":
        "older Hebrew prophet standing in small public square addressing builders and farmers, Haggai, "
        "Zechariah with visions of lampstands and olive trees, the prophets renewing courage",
    "Second Temple Complete":
        "wide shot of completed Second Temple — visibly smaller and less ornate than Solomon's, but standing, "
        "old men who remembered Solomon's Temple weeping, young men shouting for joy, voices mingled",
    "For Such a Time — Esther":
        "wide aerial of great Persian palace at Susa — marble pillars, gold-leafed walls, gardens, "
        "young queen in royal robes approaching king's throne room, heart pounding, golden scepter extended",
    "Ezra Returns":
        "older Hebrew scholar surrounded by ancient scrolls in Babylonian study, Ezra the scribe, "
        "Ezra reading the Law in Jerusalem, people weeping as they hear it",
    "Walls of Jerusalem":
        "Hebrew official in elegant Persian court dress serving king at marble banquet table, Nehemiah the cupbearer, "
        "Nehemiah surveying Jerusalem's broken walls by night on a donkey, torchlight and rubble",
    "The Great Reading":
        "vast public square inside rebuilt walls of Jerusalem at dawn, people gathered, the great assembly, "
        "Ezra on wooden platform reading scroll aloud to thousands standing in Jerusalem square",
    "Malachi — Last Prophet":
        "Hebrew priests offering blemished and sickly animals on altar of Second Temple, corrupt offerings, "
        "Malachi's final warning — turn back, the messenger is coming, the day of the Lord",
    "The Four Hundred Years":
        "long aerial view of Jerusalem and Temple Mount, sun rising and setting through the centuries, "
        "four hundred years of prophetic silence, Hellenistic Jerusalem, Roman occupation beginning",
    "Closing Transition":
        "night road to Bethlehem, single bright star rising on horizon, young couple on donkey approaching, "
        "the long silence breaking, the voice in the wilderness preparing the way",
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


def get_color_grade(chapter_num: int) -> str:
    """Return color grading guidance for a chapter (informational metadata)."""
    return CHAPTER_COLOR_GRADE.get(chapter_num, "natural period-accurate colour palette")
