"""
Old Testament documentary visual style guide.
Provides section-specific image prompt templates, negative prompts,
and cinematic style instructions for each of the 15 chapters.

Implements a Level 1-6 lore database:
  Level 1 — Major recurring characters (Moses, David, Abraham, etc.)
  Level 2 — Secondary named characters (Lot, Rebekah, Goliath, etc.)
  Level 3 — Supernatural entities (Angels, Cherubim, Seraphim)
  Level 4 — Nation/culture profiles (Israelites, Egyptians, Philistines, etc.)
  Level 5 — Geographic locations (Garden of Eden, Egypt, Sinai, etc.)
  Level 6 — Section-level scene descriptions
"""

# ── Base cinematic style for all OT prompts ────────────────────────────────────
OT_BASE_STYLE = (
    "ultra photorealistic cinematic film still, high-budget biblical historical documentary, "
    "ancient Middle Eastern setting, historically grounded Bronze Age and Iron Age details, "
    "warm desert lighting, natural materials only (hand-woven wool robes, rough linen, "
    "leather sandals, bronze tools, hewn stone, weathered wood), "
    "dramatic but realistic lighting, highly detailed faces and environments, "
    "consistent warm cinematic color grading, film grain, anamorphic lens, "
    "16:9 widescreen composition, no text, no watermarks"
)

OT_NEGATIVE = (
    "avoid: medieval European castle aesthetics, fantasy armor, European Renaissance art style, "
    "anime, cartoon, illustration, CGI uncanny valley look, plastic skin texture, "
    "modern clothing, modern buildings, modern hairstyles, whitewashed European facial features, "
    "oversaturated colors, flat lighting, clean studio lighting, "
    "science fiction elements, unrealistic weapons, generic AI fantasy imagery, "
    "text, watermark, logo, distorted anatomy, nudity"
)

# ── Inline negative guidance appended to every Flux prompt ────────────────────
OT_INLINE_NEGATIVE = (
    "cinematic realism only, no fantasy elements, no European medieval aesthetics, "
    "no modern elements, no anime or illustration style, authentic ancient Middle Eastern appearance"
)

# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 1 — MAJOR RECURRING CHARACTERS
# Full physical appearance for every prompt that includes these figures.
# ══════════════════════════════════════════════════════════════════════════════
CHARACTER_APPEARANCE: dict[str, str] = {

    # ── Primordial Era ────────────────────────────────────────────────────────
    "Adam": (
        "first man, lean muscular Bronze Age build, medium-dark olive skin, short dark hair, "
        "simple primitive woven cloth wrap, barefoot in garden setting, innocent direct gaze, "
        "no beard in early scenes"
    ),
    "Eve": (
        "first woman, dark olive skin, long dark wavy hair loose to her waist, "
        "simple leaf and natural cloth covering, barefoot, ancient Semitic beauty, "
        "wide dark eyes, graceful bearing"
    ),
    "Noah": (
        "very elderly patriarch, enormously long grey-white beard and flowing grey hair, "
        "deeply sun-weathered and wrinkled bronze skin, rough undyed wool robes, "
        "calloused carpenter's hands, determined wise eyes, commanding presence"
    ),

    # ── Patriarchs ────────────────────────────────────────────────────────────
    "Abraham": (
        "elderly Semitic patriarch, long flowing grey-white beard, deeply tanned weathered olive skin, "
        "dark brown eyes, earth-toned nomadic wool robes belted with leather, "
        "dignified composed bearing, wise and kind expression"
    ),
    "Abram": (
        "middle-aged Semitic man, dark beard beginning to grey at edges, bronze-olive skin, "
        "wealthy Mesopotamian-style fine wool robes, confident desert nomad bearing, "
        "strong hands, alert intelligent eyes"
    ),
    "Sarah": (
        "elderly Semitic woman, silver hair, deeply kind weathered face, "
        "earth-toned linen head covering and robes, graceful dignified bearing, "
        "eyes that hold both sorrow and joy"
    ),
    "Isaac": (
        "middle-aged Semitic man, dark beard, bronze-olive skin, "
        "plain Canaanite shepherd's robes of undyed wool, quiet gentle expression, "
        "calm and meditative bearing"
    ),
    "Jacob": (
        "strong Semitic man in his prime, thick dark curly beard, bronze olive skin, "
        "multi-layered wool traveling robes in earth tones, shepherd's staff, "
        "intense determined dark eyes, shrewd and purposeful expression"
    ),
    "Esau": (
        "rugged stocky Semitic man, reddish-brown skin complexion, thick wild reddish-brown beard, "
        "rough hunter's leather garments, carrying bow or game animals, "
        "coarse dark reddish hair on arms, direct bold expression"
    ),
    "Joseph": (
        "young handsome Semitic man, smooth bronze-olive skin, dark eyes, high cheekbones, "
        "ornate multi-colored striped robe in early Canaan scenes, "
        "fine white Egyptian linen in Egyptian court scenes, "
        "dignified intelligent bearing, natural leadership presence"
    ),

    # ── Moses and the Exodus Era ──────────────────────────────────────────────
    "Moses": (
        "elderly Hebrew prophet, long dark-gray beard (dark grey with streaks, not white), "
        "sun-worn olive skin, deep brown eyes that burn with fire, "
        "rough undyed wool desert robes, worn leather sandals, heavy wooden staff, "
        "commanding towering presence, radiates authority — "
        "NOTE: in Egyptian palace scenes he is younger, clean-shaven, wearing fine Egyptian linen"
    ),
    "Aaron": (
        "elderly Hebrew priest, long white beard, bronze-olive skin, "
        "elaborate embroidered priestly robes (blue, purple, scarlet, gold) with breastplate in Temple scenes, "
        "plain undyed wool robes in wilderness scenes, gold incense censer in hand"
    ),
    "Miriam": (
        "elderly Hebrew prophetess, grey hair under simple cloth head covering, bronze-olive skin, "
        "simple earth-toned linen robes, tambourine in celebration scenes, "
        "strong face with prophetic authority"
    ),
    "Pharaoh": (
        "Egyptian king, clean-shaven face, dark kohl-lined eyes, "
        "crisp white linen shendyt kilt, ornate gold pectoral collar, "
        "blue-and-gold nemes headdress with uraeus cobra, bronze-toned Egyptian complexion, "
        "commanding imperial bearing, seated on gold throne in court scenes"
    ),

    # ── Joshua and Judges Era ─────────────────────────────────────────────────
    "Joshua": (
        "strong middle-aged Hebrew warrior, bronze-olive skin, dark beard, "
        "Bronze Age Israelite leather and linen battle armor, bronze-tipped spear, "
        "sword at belt, commanding military presence, confident steady gaze"
    ),
    "Deborah": (
        "middle-aged Hebrew prophetess, olive skin, dark hair with simple cloth head covering, "
        "plain Israelite robes, seated beneath large date palm with authority, "
        "wise and calm expression, scroll in hand"
    ),
    "Gideon": (
        "young Hebrew man, olive skin, dark hair, strong farmer's build, "
        "plain rough linen farmer's clothing, initially fearful and uncertain expression, "
        "later resolute warrior bearing"
    ),
    "Samson": (
        "enormously muscular Hebrew man, very bronze tanned skin, "
        "very long thick dark hair (his power — seven braids or loose), "
        "simple rough undyed Israelite cloth wrap, bare chest in battle scenes, "
        "overwhelming physical presence"
    ),
    "Ruth": (
        "young Moabite woman, olive-bronze skin, dark hair tied back, "
        "simple earth-toned rural field robes, gleaning basket on her arm, "
        "loyal devoted expression, quiet inner strength"
    ),

    # ── Samuel and the Kingdom Era ────────────────────────────────────────────
    "Samuel": (
        "elderly Hebrew prophet-judge, long flowing grey beard, bronze-olive skin, "
        "simple undyed prophet's wool robes, animal horn of oil in hand, "
        "stern wise expression, the last judge and first kingmaker"
    ),
    "Hannah": (
        "Hebrew woman in her 30s, dark hair under simple cloth head covering, "
        "modest plain wool robes, tearful anguished expression in Temple scenes, "
        "radiant joyful expression in later scenes holding her child"
    ),
    "Saul": (
        "very tall Hebrew king — stands head and shoulders above others, "
        "bronze-olive skin, dark beard, early scenes: plain Israelite shepherd's clothes, "
        "later: Bronze Age leather and bronze royal armor, purple-trimmed robes, "
        "initially humble, later haunted and tormented expression"
    ),
    "David": (
        "young David: ruddy olive complexion, auburn-brown wavy hair, shepherd's simple rough robes, "
        "sling at belt, bright intense eyes, youthful vitality — "
        "King David: dark beard, bronze-olive skin, royal blue and gold robes, "
        "simple gold crown, lyre in some scenes"
    ),
    "Jonathan": (
        "young Hebrew warrior, bronze-olive skin, dark hair, "
        "Israelite Bronze Age armor and royal robes (king's son), "
        "loyal warm expression, genuine brotherly love in his bearing"
    ),
    "Bathsheba": (
        "beautiful Hebrew woman, olive skin, long dark hair, "
        "fine linen robes in palace scenes, modest clothing in private scenes, "
        "composed expression that holds both beauty and sorrow"
    ),
    "Absalom": (
        "strikingly handsome young Hebrew man, bronze-olive skin, "
        "famously very long thick dark hair (the most beautiful man in Israel), "
        "fine elaborate robes, proud and charismatic bearing"
    ),
    "Solomon": (
        "young Solomon: clean-shaven handsome Hebrew king, bronze-olive skin, dark eyes, "
        "increasingly elaborate gold and purple royal robes — "
        "old Solomon: white beard, world-weary expression, still opulent clothing, "
        "eyes that have seen everything and found it empty"
    ),

    # ── Prophets ──────────────────────────────────────────────────────────────
    "Elijah": (
        "wild-looking Hebrew prophet, lean and deeply sun-weathered, dark bronze skin, "
        "rough coarse camel-hair outer garment, wide leather belt around his waist, "
        "intense burning eyes, no elaborate robes — he looks like a desert wanderer, "
        "wild dark-grey hair and beard"
    ),
    "Elisha": (
        "middle-aged Hebrew prophet, dark beard going grey, bronze-olive skin, "
        "plain wool prophet's mantle over simple robes, "
        "carrying Elijah's cloak after Elijah departs, calm purposeful expression"
    ),
    "Isaiah": (
        "Hebrew prophet, middle-aged, olive skin, dark beard, "
        "fine Jerusalem wool robes with embroidered borders (he was an educated urban court prophet), "
        "ancient scroll in hand, intense prophetic gaze"
    ),
    "Jeremiah": (
        "Hebrew prophet, initially young (smooth-faced early scenes), later middle-aged with short beard, "
        "worn simple rough robes, tear-stained face, scroll or clay tablet, "
        "grief-stricken bearing — the weeping prophet — "
        "yoke around neck in enacted prophecy scenes"
    ),
    "Ezekiel": (
        "Hebrew priest-prophet, middle-aged, bronze-olive skin, dark beard, "
        "priestly linen robes in vision scenes, intense visionary expression, "
        "eyes wide with what he has witnessed, scroll in hand"
    ),
    "Daniel": (
        "young Hebrew noble, bronze-olive skin, clean-shaven or very light beard (Babylonian court style), "
        "fine Babylonian court clothing (lapis lazuli blue and gold), "
        "dignified intelligent bearing, unbroken inner calm — "
        "old Daniel: neat white beard, still dignified, eyes full of wisdom"
    ),
    "Shadrach": (
        "young Hebrew man, bronze-olive skin, short dark beard, "
        "fine Babylonian court clothing, courageous calm expression, "
        "standing with Meshach and Abednego"
    ),
    "Meshach": (
        "young Hebrew man, bronze-olive skin, short dark beard, "
        "fine Babylonian court clothing, courageous calm expression"
    ),
    "Abednego": (
        "young Hebrew man, bronze-olive skin, short dark beard, "
        "fine Babylonian court clothing, courageous calm expression"
    ),

    # ── Foreign Rulers ────────────────────────────────────────────────────────
    "Nebuchadnezzar": (
        "Babylonian emperor, full black beard oiled and tightly curled in Babylonian style, "
        "elaborate gold and lapis lazuli embroidered robes, tall ornate Babylonian conical crown, "
        "bronze-olive complexion, powerful intimidating presence, commanding authority"
    ),
    "Cyrus": (
        "Persian king, full dark beard trimmed neatly, elaborate Persian embroidered robes, "
        "Persian-style tiara crown, slightly lighter complexion than Babylonians, "
        "dignified benevolent bearing, the king who lets Israel go free"
    ),
    "Esther": (
        "young Jewish woman of exceptional beauty, olive-bronze skin, dark lustrous hair, "
        "elaborate Persian royal robes with gold embroidery and jewelry in court scenes, "
        "modest plain Jewish clothing in private scenes, "
        "graceful bearing that blends both worlds"
    ),
    "Mordecai": (
        "middle-aged Jewish man, dark beard going grey, "
        "plain undyed Jewish robes in early scenes, "
        "official Persian court clothing with gold chain in later scenes"
    ),

    # ── Return Era ────────────────────────────────────────────────────────────
    "Ezra": (
        "Jewish scribe-priest, middle-aged, neat dark beard, "
        "white priestly linen robes, ancient Torah scroll cradled in his arms, "
        "scholarly reverent bearing"
    ),
    "Nehemiah": (
        "Jewish official, middle-aged, dark beard, "
        "fine Persian court clothing in palace scenes, "
        "work clothes and sword at hip during Jerusalem wall-building"
    ),
    "Zerubbabel": (
        "Jewish governor, middle-aged, dark beard, bronze-olive skin, "
        "plain post-exilic Jewish robes, builder's leadership bearing"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 2 — SECONDARY NAMED CHARACTERS
# ══════════════════════════════════════════════════════════════════════════════
SECONDARY_CHARACTERS: dict[str, str] = {
    "Lot": (
        "middle-aged Semitic man, dark beard, bronze skin, "
        "plain nomadic wool robes, Abraham's nephew, torn between two worlds"
    ),
    "Rebekah": (
        "young Semitic woman, olive skin, dark hair, beautiful and strong-willed, "
        "simple Aramean village robes, water jar on her shoulder"
    ),
    "Rachel": (
        "young beautiful Aramean woman, olive skin, dark hair, graceful, "
        "simple shepherd girl's robes, sheep around her"
    ),
    "Leah": (
        "young Aramean woman, olive skin, dark hair, kind face, "
        "simple robes, tender expression"
    ),
    "Potiphar": (
        "Egyptian official, clean-shaven, dark kohl eyes, "
        "white linen robes with gold collar, commanding Egyptian bearing"
    ),
    "Jochebed": (
        "Hebrew mother, olive skin, dark hair, plain slave robes, "
        "desperate protective love in her expression, Moses' mother"
    ),
    "Caleb": (
        "middle-aged Hebrew warrior, bronze skin, dark beard, "
        "battle-worn Israelite armor, confident fearless expression"
    ),
    "Rahab": (
        "Canaanite woman, olive skin, dark hair, "
        "colorful Canaanite robes, crimson cord in her window"
    ),
    "Boaz": (
        "prosperous middle-aged Hebrew landowner, dark beard going grey, "
        "fine quality wool robes, generous dignified bearing, Bethlehem farmer"
    ),
    "Naomi": (
        "elderly Israelite woman, grey hair, deeply weathered face, "
        "plain travel-worn robes, grief and resilience in equal measure"
    ),
    "Eli": (
        "very elderly Hebrew high priest, white beard, failing eyesight, "
        "elaborate priestly robes, large frame, sitting in the gate"
    ),
    "Goliath": (
        "enormous Philistine warrior standing over nine feet tall, "
        "full bronze scale armor from head to foot, bronze helmet, "
        "massive iron spear, bronze javelin, towering over everyone, "
        "Philistine warrior markings, terrifying physical presence"
    ),
    "Jezebel": (
        "Phoenician queen, bold and striking beauty, olive skin, dark kohl-painted eyes, "
        "elaborate Phoenician robes in purple and crimson, heavy gold jewelry, "
        "calculating dangerous expression, Baal devotee — "
        "never subdued-looking, always commanding and threatening"
    ),
    "Elijah_young": (
        "young Hebrew man before his prophetic calling, plain Israelite robes"
    ),
    "Naaman": (
        "Syrian army commander, strong military bearing, fine Aramean armor, "
        "skin marred by leprosy in early scenes, cleansed skin in Jordan scenes"
    ),
    "Hezekiah": (
        "Judean king, middle-aged, dark beard, royal robes and crown, "
        "pious expression, kneeling in prayer"
    ),
    "Josiah": (
        "young Judean king — crowned at age eight, very young in early scenes, "
        "teen in reform scenes, bronze-olive skin, earnest pious expression"
    ),
    "Job": (
        "prosperous middle-aged man of Uz, dark beard, wealthy robes in early scenes, "
        "same man reduced to sitting in ash heap, torn robes, skin covered in sores, "
        "but dignified and resolute even in suffering"
    ),
    "Jonah": (
        "Hebrew prophet, middle-aged, dark beard, olive skin, "
        "plain prophet's robes, stubborn expression giving way to wonder, "
        "dripping wet and pale after the great fish"
    ),
    "Balaam": (
        "Aramean diviner, middle-aged, dark beard, non-Israelite robes, "
        "riding a donkey, staff in hand, conflicted expression"
    ),
    "Tamar_Judah": (
        "young Canaanite woman, olive skin, dark hair, "
        "simple robes, then disguised with veil at crossroads"
    ),
    "Jael": (
        "Kenite woman, olive skin, dark hair, simple tent-dwelling robes, "
        "determined fierce expression"
    ),
    "Delilah": (
        "Philistine woman, olive skin, dark hair, "
        "fine Philistine robes, beautiful but scheming expression"
    ),
    "Nathan": (
        "Hebrew prophet, middle-aged, dark beard, simple prophet's robes, "
        "standing before kings with calm authority"
    ),
    "Joab": (
        "veteran Hebrew military commander, dark beard, weathered bronze skin, "
        "battle-hardened Israelite armor, calculating loyal expression"
    ),
    "Hiram": (
        "Phoenician king of Tyre, dark beard, fine Phoenician robes, "
        "seafaring cosmopolitan bearing, trade partner of Solomon"
    ),
    "Queen_of_Sheba": (
        "African queen of extraordinary beauty, very dark rich skin, "
        "elaborate gold and jeweled robes from southern Arabia/Africa, "
        "gold crown, highly intelligent assessing gaze"
    ),
    "Rehoboam": (
        "young Hebrew king, early 40s, bronze-olive skin, dark beard, "
        "royal robes, arrogant and foolish expression"
    ),
    "Jeroboam": (
        "northern Israelite leader, dark beard, bronze skin, "
        "Israelite robes, ambitious determined bearing"
    ),
    "Ahab": (
        "Israelite king, dark beard, royal northern Israelite armor and robes, "
        "bronze-olive skin, weak and indecisive expression dominated by Jezebel"
    ),
    "Sennacherib": (
        "Assyrian king, full black oiled beard in tight Assyrian curls, "
        "elaborate Assyrian armor and royal robes, pointed war helmet, "
        "arrogant conquering expression"
    ),
    "Manasseh": (
        "Judean king crowned at twelve — boy king in early scenes, "
        "adult in later scenes, dark beard, royal robes, "
        "idolatrous darkened expression"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 3 — SUPERNATURAL ENTITIES
# ══════════════════════════════════════════════════════════════════════════════
SUPERNATURAL_ENTITIES: dict[str, str] = {
    "Angel": (
        "luminous figure in dazzlingly white robes, face almost too bright to look at directly, "
        "tall imposing presence, warm golden-white radiance emanating from within, "
        "no cartoon wings — subtle light suggests divine nature, "
        "ancient Middle Eastern human form but unmistakably otherworldly"
    ),
    "Angel_warrior": (
        "massive warrior figure in white and light armor, drawn blazing sword, "
        "overwhelming physical presence, golden-white light, guardian stance, "
        "no fantasy armor — ancient divine warrior aesthetic"
    ),
    "Cherubim": (
        "monumental supernatural creatures with four faces (human, lion, ox, eagle), "
        "four wings spread wide, gleaming bronze bodies, wheels within wheels of fire beside them, "
        "unearthly amber and white glow, Ezekiel's vision aesthetic, "
        "ancient Near Eastern throne guardian imagery"
    ),
    "Seraphim": (
        "magnificent six-winged creatures above the divine throne, "
        "two wings covering face, two covering feet, two in flight, "
        "blazing brilliant white-gold, voices that shake the foundations, "
        "Isaiah's Temple vision aesthetic"
    ),
    "Burning_Bush": (
        "single thorn bush fully engulfed in pure golden-white fire, "
        "fire burning but not consuming — leaves intact within the flames, "
        "supernatural light pouring from within the bush, "
        "rocky Sinai wilderness, late afternoon, sacred ground, "
        "pair of sandals on ground before it"
    ),
    "Pillar_of_Fire": (
        "towering column of supernatural fire ascending from earth to sky at night, "
        "enormous scale dwarfing the camp below, amber-orange base transitioning to pure white above, "
        "two million Israelites in its light, desert night sky, stars behind"
    ),
    "Pillar_of_Cloud": (
        "towering column of dense luminous white cloud descending from sky to earth by day, "
        "dazzling white top, dark thunderous base, "
        "leading two million Israelites across desert, massive scale"
    ),
    "Glory_of_God": (
        "blinding golden-white cloud filling interior of temple or tabernacle, "
        "priests unable to stand, prostrate on floor, "
        "no visible form — only overwhelming radiant light and thick cloud, "
        "smoke and fire at the edges"
    ),
    "Angel_of_Death": (
        "unseen presence moving through Egyptian darkness at midnight, "
        "no literal figure shown — only doorposts with dark lamb's blood, "
        "lights going out in Egyptian homes, pale death in the air, "
        "Hebrew homes glowing with lamplight from within, protected"
    ),
    "Divine_Throne": (
        "ancient of days seated on high exalted throne, vast heavenly court, "
        "ten thousand times ten thousand serving him, "
        "throne blazing with fire, wheels of fire, river of fire flowing, "
        "Daniel's vision aesthetic — no face of God shown, only overwhelming radiant presence"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 4 — NATION AND CULTURE PROFILES
# ══════════════════════════════════════════════════════════════════════════════
NATION_STYLE: dict[str, str] = {
    "Israelites": (
        "ancient Semitic people, olive to bronze skin tones, dark hair, dark eyes, "
        "men in undyed or earth-toned rough wool and linen robes with fringed edges (tzitzit), "
        "leather sandals, men typically bearded, women with hair covered, "
        "plain functional clothing — no gold embroidery except priests and royalty, "
        "Bronze Age to Iron Age tools, clay pottery, goatskin water bags, "
        "simple stone and mud-brick homes in hill country, olive groves and vineyards, "
        "architecture: rough hewn limestone, no dressed stone except Jerusalem"
    ),
    "Egyptians": (
        "ancient North African Mediterranean people, warm bronze-copper skin tones, dark eyes, "
        "men: clean-shaven (or small neat kohl-lined beards for officials), white linen kilts (shendyt), "
        "gold pectoral collars for officials, blue-and-gold nemes headdresses for royalty, "
        "women: white linen sheath dresses, heavy kohl eye makeup, elaborate wigs and gold jewelry, "
        "massive sandstone and granite architecture, colonnaded temples covered in hieroglyphs, "
        "painted statuary, obelisks, sphinx, Nile river setting, palm trees, papyrus, "
        "New Kingdom 18th-19th dynasty aesthetic"
    ),
    "Philistines": (
        "Sea Peoples of Aegean origin settled in Canaan coastal plain, "
        "slightly lighter Mediterranean complexion than Israelites, "
        "distinctive armor: bronze scale armor, feathered or ridged helmets (no horns), "
        "iron weapons — iron swords, spears, chariots (technological advantage), "
        "fine Mycenaean-influenced pottery and architecture, "
        "five city-states: Gaza, Ashdod, Ashkelon, Gath, Ekron, "
        "more urban and cosmopolitan than Israelites"
    ),
    "Babylonians": (
        "Mesopotamian people, olive-bronze skin, dark hair, "
        "men: full beards oiled and tightly curled in rings, "
        "elaborate embroidered robes in deep blues, reds, and golds, "
        "tall conical or tiara-shaped headdresses for officials, "
        "women: elaborate hairstyles with gold pins, layered robes, heavy jewelry, "
        "massive ziggurat architecture, blue-glazed Ishtar Gate tiles, "
        "hanging gardens, processional ways lined with lions and dragons (mushhushshu), "
        "cuneiform clay tablets, lapis lazuli and gold decoration everywhere, "
        "Neo-Babylonian empire aesthetic (605-539 BC)"
    ),
    "Assyrians": (
        "northern Mesopotamian empire, bronze-olive skin, dark hair, "
        "men: thick full beards tightly curled, "
        "heavy scale armor, pointed iron helmets, large decorated shields, "
        "iron weapons and war machines (siege towers, battering rams), "
        "elaborate bas-relief palace walls carved with battle scenes, "
        "human-headed winged bull guardians (lamassu) at palace gates, "
        "brutal efficient military machine aesthetic, "
        "robes in earthy tones with fringe, royal robes in purple and gold, "
        "Neo-Assyrian empire aesthetic (900-600 BC)"
    ),
    "Persians": (
        "Iranian plateau people, olive to medium-tan skin, dark hair, "
        "men: neatly trimmed full beards (not tightly curled like Babylonians), "
        "elaborate embroidered court robes in cream, crimson, and purple, "
        "tall cidaris crown for king, tiara hats for nobles, "
        "Persian-style columns with bull-headed capitals at Persepolis, "
        "marble palace floors, gold and silver vessels, "
        "notably tolerant and cosmopolitan compared to Assyria/Babylon, "
        "Achaemenid Persian empire aesthetic (550-330 BC)"
    ),
    "Canaanites": (
        "original inhabitants of the land, closely related Semitic people to Israelites, "
        "olive-bronze skin, dark hair, similar basic clothing to Israelites but more colorful, "
        "walled city-states on hilltops with mudbrick walls, "
        "Baal and Asherah worship — standing stones (masseboth), wooden poles (asherah poles), "
        "bronze and iron tools, "
        "Canaanite cities: Jericho, Ai, Gibeon, Hazor, Megiddo, "
        "Late Bronze Age to Iron Age I aesthetic"
    ),
    "Arameans": (
        "Semitic people north and northeast of Israel (modern Syria), "
        "olive skin, dark hair, similar to Israelites but distinct culture, "
        "Damascus as major city, frequent conflict and trade with Israel, "
        "Iron Age city-state culture, chariots and cavalry"
    ),
    "Moabites": (
        "Semitic people east of Dead Sea, closely related to Israelites, "
        "olive-bronze skin, dark hair, simple pastoral culture, "
        "Mesa Stele writing, similar clothing to Israelites"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 5 — GEOGRAPHIC LOCATION BIBLE
# ══════════════════════════════════════════════════════════════════════════════
LOCATION_BIBLE: dict[str, str] = {
    "Garden_of_Eden": (
        "impossibly lush primordial garden, towering ancient trees with golden fruit, "
        "crystal clear river branching four ways, flowers in every color, "
        "soft eternal golden light filtering through canopy, "
        "no thorns, no imperfection — paradise before the fall, "
        "warm amber light, glowing in perpetual golden hour"
    ),
    "Ancient_Mesopotamia": (
        "flat alluvial plain between great rivers Tigris and Euphrates, "
        "mud-brick cities with massive ziggurats rising from flat horizon, "
        "palm trees lining canals, irrigated fields, "
        "Ur and Haran — prosperous Bronze Age Mesopotamian city-states, "
        "dense urban life, merchants, temples, cuneiform inscriptions everywhere"
    ),
    "Canaan_Hill_Country": (
        "undulating limestone hill country, ancient olive groves on terraced hillsides, "
        "scattered sheep grazing on dry grass, stone walls, "
        "small village clusters of mudbrick houses, ancient wells, "
        "dry and rocky terrain softened by scrub vegetation, "
        "warm Mediterranean light, dust in the air"
    ),
    "Negev_Desert": (
        "vast arid desert, cracked earth and scattered stones, "
        "occasional dry riverbed (wadi), sparse thorn bushes, "
        "enormous sky, heat shimmer on the horizon, "
        "nomadic tent camps with goat-hair black tents, camels resting"
    ),
    "Egypt_Nile_Valley": (
        "lush green Nile flood plain cutting through desert, "
        "black fertile soil, papyrus reeds, date palms, "
        "massive temple complexes of New Kingdom Egypt — Karnak, Luxor, "
        "colossal stone statues and obelisks, Nile barges, "
        "mud-brick slave quarters beside stone temple walls"
    ),
    "Sinai_Wilderness": (
        "dramatic red-brown granite mountain wilderness, "
        "Mount Sinai — towering dark peak wreathed in cloud, "
        "vast rocky plains, narrow canyons, "
        "no vegetation except sparse thorns, "
        "overwhelming silence and scale, "
        "bleached bone color with deep red-ochre rock"
    ),
    "Tabernacle": (
        "portable sacred tent complex at center of desert camp, "
        "white linen curtain enclosure, bronze altar of burnt offering at entrance, "
        "inner golden lampstand and table of showbread visible through parted curtain, "
        "ark of the covenant in the inner Holy of Holies, "
        "incense smoke rising, cloud of glory above"
    ),
    "Jordan_River": (
        "wide muddy spring-flooded Jordan River cutting through green valley, "
        "willow and tamarisk trees on banks, "
        "east bank: dry hills of Moab and Gilead, "
        "west bank: green Canaan hill country, "
        "crossing point — the threshold between wilderness and promise"
    ),
    "Jericho": (
        "ancient walled city on oasis in Jordan Valley, "
        "impressive mudbrick defensive walls, spring of water, "
        "oldest city in the world — flat desert plain all around, "
        "palm trees within the walls, fragile beauty before the fall"
    ),
    "Jerusalem": (
        "ancient city of Jerusalem on hilltop, "
        "City of David: compact stone buildings on narrow ridge above Kidron Valley, "
        "Temple Mount: massive hewn limestone platform, "
        "Solomon's Temple: white limestone and gold cedar-lined interior, "
        "city walls of cut stone, Eastern Gate, Pool of Siloam, "
        "Kidron Valley below, Mount of Olives to east, "
        "Hinnom Valley to west and south"
    ),
    "Solomon_Temple": (
        "magnificent First Temple of Jerusalem, "
        "white limestone exterior with gold-leafed cedar interior, "
        "two great bronze pillars (Jachin and Boaz) at entrance, "
        "ten bronze basins, sea of cast bronze, "
        "inner Holy of Holies overlaid in pure gold, "
        "two golden cherubim with wings spanning the room, "
        "incense smoke, golden lampstands glowing"
    ),
    "Philistia_Coast": (
        "Mediterranean coastal plain of ancient Philistia, "
        "sandy coastline, olive groves, vineyards, "
        "five fortified city-states, Philistine-style mudbrick and stone architecture, "
        "Greek-influenced pottery and culture, iron weapons"
    ),
    "Northern_Kingdom_Samaria": (
        "rolling hills of Ephraim and Manasseh, "
        "capital city of Samaria on hilltop, "
        "fertile agricultural land, vineyards, olive groves, "
        "mixed Israelite and Canaanite culture, Baal worship sites, "
        "Phoenician-influenced architecture in royal Samaria"
    ),
    "Babylon": (
        "massive ancient city of Babylon on Euphrates River, "
        "triple-walled defensive circuit, "
        "Ishtar Gate with blue-glazed tiles and golden dragons (mushhushshu), "
        "Processional Way lined with lion bas-reliefs, "
        "massive Esagila ziggurat (Tower of Babel), "
        "hanging gardens, royal palace of Nebuchadnezzar, "
        "enormous scale — largest city in the ancient world"
    ),
    "Exile_Chebar_River": (
        "flat Babylonian plain beside canal (Chebar River), "
        "Hebrew exile community: reed huts and small mudbrick homes, "
        "date palms, distant ziggurat visible on horizon, "
        "grey-blue sky, foreign land, the weight of displacement, "
        "cooking fires, children playing in foreign dust"
    ),
    "Persian_Susa": (
        "magnificent Persian palace of Susa (Apadana), "
        "towering columns with bull-headed capitals, "
        "polished marble floors, gold and silver vessels, "
        "hanging purple and linen drapes, "
        "vast reception halls, gardens with exotic trees, "
        "opulent wealth beyond any city of Israel"
    ),
    "Second_Temple": (
        "rebuilt Jerusalem Temple on same Mount Moriah foundation, "
        "smaller and less ornate than Solomon's First Temple — visibly humbler, "
        "plain hewn limestone, no gold overlay, "
        "same site but the glory has not yet returned, "
        "surrounded by rubble and rebuilding Jerusalem"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# SUPPORTING STYLE TABLES
# ══════════════════════════════════════════════════════════════════════════════

EMOTION_STYLE: dict[str, str] = {
    "awe":            "divine golden light breaking through darkness, volumetric rays, vast scale",
    "dark_and_tense": "deep shadow and smoke, storm clouds, blood-red sky at horizon, high contrast",
    "dramatic":       "high contrast directional light, deep shadow, intense focal moment, shallow DOF",
    "hopeful":        "warm sunrise light, soft golden hour glow, open horizon, optimistic framing",
    "solemn":         "muted warm tones, single torch or fire light, heavy atmosphere, still composition",
    "mysterious":     "deep shadow, flickering torchlight, desert night, starlit sky, hidden forms",
    "triumphant":     "golden light, wide epic scope, raised banners, crowds, warm triumphant palette",
    "epic_grandeur":  "sweeping aerial perspective, monumental architecture, vast landscape, awe-inspiring scale",
    "grief":          "grey cold tones, hunched figures, ash and smoke, tears visible, broken forms",
    "supernatural":   "unearthly amber and white light, impossible radiance, reality bending at edges",
}

CHAPTER_ENVIRONMENT: dict[int, str] = {
    1:  "primordial ancient earth, Garden of Eden, pre-flood wilderness, early human settlements",
    2:  "post-flood new world, ancient Mesopotamian city-state, Canaan rolling hills, desert trade routes",
    3:  "Canaan hill country, Haran in Mesopotamia, trade caravans, Nile delta Egypt grain stores",
    4:  "New Kingdom Egypt, mud-brick slave quarters, Nile River valley, Sinai peninsula desert",
    5:  "Sinai wilderness, desert canyons, stone mountains, Tabernacle tent complex, plains of Moab",
    6:  "Canaan hill country, Jordan River valley, walled ancient cities, wheat fields, Philistine coast",
    7:  "Shiloh Tabernacle, Philistine cities, Judean wilderness caves, early Jerusalem fortifications",
    8:  "Jerusalem city of David, David's palace, Temple Mount preparation, Israelite capital at its height",
    9:  "Jerusalem at peak glory, massive hewn stone Temple, Phoenician-influenced architecture, Solomon's palace",
    10: "Northern Israelite hill towns, Samaria, Mount Carmel, Sinai wilderness, Zarephath coastal town",
    11: "Assyrian siege warfare, Babylon approaching, Jerusalem walls, burning ancient cities, Judean hills",
    12: "Neo-Babylonian empire, massive ziggurat city, plain of Dura, Persian palace architecture",
    13: "Chebar River exile community, Babylonian streets, vision of ruined Jerusalem, heavenly throne room",
    14: "Persian palace of Susa, road from Babylon to Jerusalem, Jerusalem ruins, Second Temple construction",
    15: "post-exilic Jerusalem, Second Temple precinct, rebuilt city walls, Bethlehem road at night",
}

CHAPTER_COLOR_GRADE: dict[int, str] = {
    1:  "deep navy and gold for cold open, expanding to warm golden full colour for creation, "
        "saturated greens and soft golden hour for Eden, colour draining to muted tones for the fall, "
        "storm grey and churning brown for the flood",
    2:  "fresh post-flood greens giving way to sun-bleached desert ochres, "
        "deep midnight blues with brilliant white starlight for Abraham's covenant, "
        "red-orange hellfire for Sodom, warm intimate lamplight for Isaac and Rebekah",
    3:  "warm Canaan golds for Jacob's journey, deep midnight blue for Jabbok wrestling, "
        "rich Egyptian linen whites and painted gold for Joseph's rise, "
        "earthy ochre for the caravan scenes",
    4:  "bleached oranges and browns for Egyptian slavery, deep Nile blues for Moses' birth, "
        "Egyptian palace gold and lapis lazuli, blood red for the plagues, "
        "turquoise and white for the Red Sea crossing",
    5:  "sun-bleached desert tones darkening as Sinai approaches, "
        "smoky blacks and deep storm blues with sudden orange-red fire for the theophany, "
        "warm gold and linen white for Tabernacle interiors, dusty muted for forty years",
    6:  "harder, more weathered — Bronze Age to early Iron Age palette, "
        "warm harvest gold for Ruth, dark oppressive tones for the dark end of Judges",
    7:  "late Iron Age village settings — lamplight yellows for Samuel's calling, "
        "deep cave shadows for David's wilderness years, dark Philistine battlefield at Mount Gilboa",
    8:  "triumphant warm gold for David's coronation and the Ark, "
        "rooftop moonlit blue for Bathsheba, dark interior shadows for Absalom's rebellion",
    9:  "richest and most opulent — Solomon's court in deep gold and crimson, "
        "Temple interior in blinding white-gold, Queen of Sheba in exotic jewel tones, "
        "darkening as Solomon falls and the kingdom splits",
    10: "northern kingdom in cooler Phoenician blues and greys, "
        "bleached desert tones for Elijah's wilderness, storm-grey and fire-orange for Mount Carmel, "
        "intimate cave darkness for the still small voice",
    11: "progressively darkening — Elisha's pastoral warmth giving way to harsh Assyrian conquest, "
        "gathering shadow of Babylonian siege, ending in ash grey and smoke black",
    12: "Babylon is beautiful in dangerous colours — lapis lazuli blue tiles, gold leaf, deep purples, "
        "the furnace in blinding white-orange, Persian palace in cool marble whites and gold",
    13: "Chebar River in muted exile browns and blues, vision sequences in unearthly amber and white, "
        "the dry bones valley in bleached bone-white under grey sky",
    14: "Persian palace in opulent gold-crimson, road to Jerusalem in dusty warm ochre, "
        "Jerusalem ruins in grey rubble, new altar in warm firelight against the ruins",
    15: "muted, domestic, human-scale — fragile warmth of post-exilic community, "
        "Second Temple in humble grey stone, Esther's court in opulent gold-crimson, "
        "closing in deep silent blue before the star rises over Bethlehem",
}

# ══════════════════════════════════════════════════════════════════════════════
# LEVEL 6 — SECTION-LEVEL SCENE DESCRIPTIONS
# ══════════════════════════════════════════════════════════════════════════════
SECTION_VISUAL: dict[str, str] = {

    # ── Chapter 1: Creation to the Flood ──────────────────────────────────────
    "Cold Open": (
        "vast cosmic void, infinite black space with faintest blue mist, "
        "single beam of warm golden light beginning to pierce the darkness, "
        "volumetric light rays, infinite darkness before creation, "
        "deep navy to gold gradient, cinematic wide shot"
    ),
    "The Creation": (
        "first light of creation bursting through cosmic darkness, divine golden radiance, "
        "waters separating from sky, mountains rising from primordial sea, "
        "sun rising for the first time, stars being set in place, "
        "silhouette of man being formed from red desert clay and dust, no visible face of God, "
        "radiant golden-white light pouring from unseen divine presence"
    ),
    "Adam and Eve": (
        "lush primordial Garden of Eden at eternal golden hour, "
        "towering ancient trees heavy with glowing fruit, "
        "two silhouettes walking hand in hand through tall grass, "
        "river flowing crystal clear, every flower in bloom, paradise before the fall"
    ),
    "The Fall": (
        "coiled serpent on bark of ancient tree, iridescent scales, intelligent gleaming eye, "
        "woman's hand reaching toward glowing forbidden fruit, "
        "golden light filtering through leaves, "
        "two figures crouched hidden among large leaves, ashamed and afraid, "
        "dramatic shadows as golden garden light dims"
    ),
    "Cain and Abel": (
        "two stone altars side by side in barren field at dusk, "
        "one altar with smoke rising straight to heaven, "
        "other smoke blowing sideways in wind, "
        "two brothers — one kneeling in prayer, one standing in silent rage, "
        "shadow of violence in the air"
    ),
    "Corruption of Mankind": (
        "aerial shot of ancient sprawling city at dusk, smoke rising from many fires, "
        "vaguely Mesopotamian mud-brick architecture, figures in corruption and violence, "
        "crumbling civilization, foreboding darkness gathering on horizon"
    ),
    "Noah and the Flood": (
        "elderly patriarch with enormous grey-white beard on hillside, "
        "gazing at sky as first dark storm clouds gather, "
        "enormous wooden ark on mountain slope, animals approaching in pairs, "
        "rain beginning to fall, last sunlight before the deluge"
    ),
    "The Covenant with Noah": (
        "brilliant full rainbow arching across clearing sky over fresh wet landscape, "
        "golden hour after the storm, Noah kneeling at stone altar, "
        "dove returning with fresh olive branch, green world reborn after flood"
    ),
    "The Tower of Babel": (
        "vast flat plain of Shinar at dawn, "
        "massive ziggurat rising from flat horizon, thousands of workers, scaffolding, "
        "confusion breaking out below — people gesturing, unable to understand each other, "
        "the great project abandoned"
    ),
    "Closing Transition": (
        "lone elderly man standing at gate of ancient Mesopotamian city at dawn, "
        "gazing at vast desert ahead, stars still bright overhead, "
        "hopeful and mysterious, the call going out"
    ),

    # ── Chapter 2: Abraham — Father of Nations ────────────────────────────────
    "The Calling of Abraham": (
        "bustling ancient Mesopotamian marketplace of Ur, merchants, scribes, soldiers, "
        "great ziggurat temple in background, "
        "elderly man standing at edge of city gates at night, vast desert ahead, "
        "stars brilliant overhead, a single figure answering a call"
    ),
    "The Covenant": (
        "vast desert sky at night, infinite stars stretching to every horizon, "
        "single small silhouette of elderly man with head tilted back gazing upward, "
        "covenant promise of descendants as countless as stars, Canaan desert"
    ),
    "The Three Visitors": (
        "three robed travelers approaching Bedouin-style black goat-hair tent "
        "under ancient terebinth oak trees at Mamre, midday heat, "
        "heat shimmer on the plains, sacred hospitality, "
        "three mysterious luminous figures"
    ),
    "Sodom and Gomorrah": (
        "twin ancient walled cities consumed by fire and burning sulfur from sky, "
        "massive columns of black smoke rising to heaven, "
        "fleeing figures, Lot's wife looking back as pillar of salt, "
        "Abraham watching from distant hilltop, smoke of the land like a furnace"
    ),
    "The Birth of Isaac": (
        "elderly woman holding newborn baby in her arms, face streaked with tears of joy, "
        "soft warm candlelit interior of desert tent, intimate miraculous birth, "
        "Sarah's ancient face transformed by impossible joy"
    ),
    "The Binding of Isaac": (
        "elderly man with raised knife over bound young son on stone altar, "
        "ram caught by horns in thicket nearby, "
        "angel's hand reaching from above to stop the blade, "
        "Mount Moriah, dramatic golden light from above"
    ),
    "Sarah and Rebekah": (
        "aged patriarch kneeling at entrance of stone burial cave of Machpelah, "
        "head bowed in grief, mourning Sarah, "
        "young woman with water jar on shoulder approaching stone well surrounded by sheep, "
        "golden hour light, Rebekah at the well"
    ),
    "Jacob and Esau": (
        "pregnant woman kneeling in prayer, hand on swollen belly, Rebekah at prayer, "
        "two sons at tent camp — one ruddy and rough-clothed hunter returning with game, "
        "one smooth and thoughtful, holding a bowl of red stew, tense family scene"
    ),
    "Jacob's Ladder": (
        "young man sleeping on open ground with single stone as pillow, "
        "blazing stairway of light ascending from earth to heaven, "
        "angels ascending and descending, vast starry night sky, "
        "Bethel, the gate of heaven"
    ),
    "Jacob Leah Rachel": (
        "young woman approaching stone well surrounded by sheep, golden hour, "
        "man rolling great stone from well mouth with one arm, "
        "uncle Laban's household, seven years of labor for love"
    ),
    "Jacob Wrestles God": (
        "lone man at edge of moonlit Jabbok River at night, absolute isolation, "
        "two figures locked in intense struggle at river's edge in darkness, "
        "dawn light breaking on horizon, limping man at first light"
    ),
    "The Reconciliation": (
        "man limping across open plain bowing to ground repeatedly, "
        "two brothers embracing with tears in open Canaanite land, "
        "Israel and Esau reconciled"
    ),
    "Joseph and His Brothers": (
        "teenage boy in elaborate multi-colored striped robe walking through tall grass, "
        "brothers watching from distance with cold jealous expressions, "
        "young man thrown into empty stone cistern, "
        "camel caravan passing in distance toward Egypt"
    ),
    "Joseph in Egypt": (
        "young Hebrew man in fine Egyptian linen standing in colonnaded Egyptian villa, "
        "young man kneeling in Egyptian prison, hands bound, face resolute and trusting"
    ),
    "Dreams of Pharaoh": (
        "two Egyptian officials in dim prison cell, troubled expressions, "
        "young Hebrew man standing before seated Pharaoh on great gold throne, "
        "interpreting the dream of seven fat and seven thin cows"
    ),
    "The Brothers Return": (
        "ten travel-worn Hebrew brothers in dusty robes bowing low before Egyptian official "
        "on raised dais, great grain stores of Egypt around them, "
        "dramatic reunion building"
    ),
    "Jacob Comes to Egypt": (
        "vast caravan of Hebrew families, flocks, tents, and wagons "
        "moving across desert from Canaan into Egypt's eastern delta, "
        "epic wide shot, dust rising, hope and fear mixed, Goshen ahead"
    ),

    # ── Chapter 3: Moses — Deliverer of Israel ────────────────────────────────
    "The Birth of Moses": (
        "Egyptian soldiers patrolling Hebrew slave quarters at night, torches in hand, "
        "Hebrew mother placing woven papyrus basket in Nile reeds at dawn, "
        "Pharaoh's daughter walking to the riverside with her servants"
    ),
    "Moses Flees Egypt": (
        "young Egyptian-raised man in royal linen, colonnaded palace, hieroglyphs on walls, "
        "same man in rough shepherd's cloak crossing empty Sinai desert, "
        "fugitive between two worlds"
    ),
    "The Burning Bush": (
        "elderly shepherd with staff walking through rocky wilderness at foot of Sinai, "
        "solitary shepherd before single burning bush that is not consumed — "
        "fire burning but leaves intact within the flame, "
        "sandals removed, face turned away, holy ground"
    ),
    "Moses Returns": (
        "two robed Hebrew brothers walking up vast Egyptian temple staircase, "
        "dwarfed by colossal columns and statuary covered in hieroglyphs, "
        "Moses and Aaron approaching Pharaoh's throne room"
    ),
    "Let My People Go": (
        "Hebrew elder standing before enthroned Pharaoh surrounded by guards and priests, "
        "Aaron's staff becoming a serpent swallowing the magicians' serpents, "
        "battle of wills in the throne room of Egypt"
    ),
    "The Ten Plagues": (
        "Nile River running blood red from bank to bank, "
        "swarms of locusts blackening Egyptian sky over green crops, "
        "hailfire falling on Egypt while Goshen is untouched, "
        "three days of supernatural darkness over the land"
    ),
    "The Passover": (
        "young Hebrew shepherd carrying spotless white lamb at dusk, "
        "Hebrew family eating in robes with staffs ready, "
        "blood of lamb painted on doorposts with hyssop branch, "
        "dark empty Egyptian streets outside, angel of death passing over"
    ),
    "The Exodus": (
        "vast columns of Hebrews and their flocks walking through desert, "
        "towering pillar of cloud rising before them by day, "
        "two million people moving as one body, epic wide shot, dust rising"
    ),
    "The Red Sea": (
        "walls of water towering on both sides, "
        "millions of Hebrews walking across dry seabed under stars, "
        "Egyptian chariots pursuing at shore's edge, "
        "sea wall beginning to collapse on the army"
    ),
    "The Song of Moses": (
        "elderly prophet on rocky eastern shore at dawn with arms raised toward sky, "
        "Miriam with tambourine leading women in dance, "
        "triumphant celebration as Egypt lies drowned"
    ),

    # ── Chapter 4: The Law and the Wilderness ─────────────────────────────────
    "The Mountain of God": (
        "vast Hebrew camp spread across desert plain at foot of towering Mount Sinai, "
        "mountain wreathed in thick smoke and fire, lightning cracking summit, "
        "two million Israelites forbidden to approach, watching from below"
    ),
    "The Ten Commandments": (
        "vast smoking mountain seen from Hebrew camp below, sky split with lightning, "
        "stone tablets held by aged weathered hands, "
        "glowing carved divine text, mountain fire behind"
    ),
    "The Covenant in Blood": (
        "old prophet reading aloud from scroll before vast assembled crowd at mountain's foot, "
        "stone altar, blood of covenant sprinkled on assembled people"
    ),
    "The Golden Calf": (
        "golden idol gleaming in desert sun before dancing celebrating crowd, "
        "Moses descending from smoke-covered mountain above, "
        "two stone tablets in hand, righteous fury on his face"
    ),
    "The Radiant Face": (
        "aged prophet kneeling on rocky mountain summit, "
        "Moses descending with veil over radiant glowing face, "
        "Israelites drawing back in fear, glory reflecting from his skin"
    ),
    "The Tabernacle": (
        "Hebrew artisans working carefully with gold-overlaid wood and fine linen, "
        "intricate craftwork by Bezalel, "
        "portable sanctuary's golden lampstand glowing inside linen tent, "
        "cloud of glory hovering above, desert camp surrounding"
    ),
    "The Law": (
        "aged priest in elaborate embroidered priestly robes — blue, purple, scarlet, gold — "
        "breastplate of twelve stones, Aaron in full high priestly dress, "
        "Tabernacle interior, incense rising"
    ),
    "The Twelve Spies": (
        "twelve men in dust-stained robes leaving vast camp at edge of wilderness, "
        "Caleb and Joshua carrying enormous cluster of grapes on pole between two men, "
        "returning from the promised land with mixed reports"
    ),
    "Forty Years": (
        "endless desert stretching to horizon in every direction, "
        "Hebrew camp of goat-hair tents, sun beating down, "
        "same landscape year after year, a generation dying in the wilderness"
    ),
    "Death of Miriam Aaron": (
        "elderly prophetess lying still in desert tent, women mourning around her, Miriam's passing, "
        "Aaron in high priestly robes on summit of Mount Hor, peaceful death on the mountain"
    ),
    "Balak and Balaam": (
        "worried Moabite king standing on high balcony overlooking vast Hebrew camp below his walls, "
        "Aramean prophet on donkey on Moabite road, angel with drawn sword blocking the path"
    ),
    "The Farewell of Moses": (
        "aged prophet with long dark-gray beard and staff standing before vast assembly of Hebrews "
        "on plains of Moab, Jordan River valley visible in distance, Moses' final addresses to the nation"
    ),
    "The Death of Moses": (
        "aged prophet climbing steep mountain path alone at sunrise, staff in hand, final ascent to Nebo, "
        "solitary figure on summit gazing at sunlit promised land across Jordan far below, "
        "Canaan visible but unreachable"
    ),

    # ── Chapter 5: The Promised Land ──────────────────────────────────────────
    "Crossing the Jordan": (
        "spring-flooded Jordan River running powerful and brown through valley, "
        "priests carrying gold Ark of Covenant stepping into the water, "
        "river walls rising, millions crossing on dry ground"
    ),
    "The Fall of Jericho": (
        "Hebrew army marching silently around great ancient walled city of Jericho, "
        "day after day, seven circuits on the seventh day, "
        "massive stone walls collapsing in cloud of dust and rubble, trumpets sounding"
    ),
    "The Conquest": (
        "Joshua's army in battle across Canaanite hill country, "
        "cities falling one by one, Israel claiming the land, "
        "Gibeonites in deliberately worn travel-clothes with moldy bread"
    ),
    "Dividing the Land": (
        "older warrior sitting in tent with tribal elders around him, "
        "large map of Canaan drawn on ground, "
        "tribes receiving their inheritance by lot"
    ),
    "Choose This Day": (
        "aged warrior Joshua standing before assembled nation at Shechem, "
        "grey hair and deeply weathered face, "
        "final challenge: choose this day whom you will serve"
    ),
    "The Cycle of Judges": (
        "young generation of Hebrew children playing in village, oblivious to history, "
        "the cycle beginning again — sin, oppression, cry for help, deliverance, peace, repeat"
    ),
    "Deborah and Barak": (
        "prophetess sitting under large date palm tree judging Israel, "
        "Hebrew army routing Canaanite iron chariots in Kishon Valley flood, "
        "Jael with tent peg"
    ),
    "Gideon": (
        "young Hebrew man hiding inside stone wine press secretly threshing wheat, "
        "three hundred men with clay pots and torches surrounding night-time enemy camp, "
        "chaos erupting in the darkness"
    ),
    "Samson": (
        "angelic figure standing in wheat field at sunset before Hebrew woman, no clear face, "
        "giant muscular man with long dark hair pushing great stone pillars of crowded Philistine temple, "
        "roof beginning to collapse"
    ),
    "Dark End of Judges": (
        "single oil lamp burning low in empty Hebrew village street at night, "
        "tribal Israel in chaos, 'everyone did what was right in their own eyes', "
        "darkest period, no king, no prophet"
    ),
    "The Book of Ruth": (
        "woman gleaning grain in Judean barley field at golden harvest, "
        "Ruth and Naomi on dusty road, two women alone on long journey, "
        "loyal companionship, Bethlehem ahead"
    ),

    # ── Chapter 6: Samuel, Saul, and the First King ───────────────────────────
    "Hannah and Samuel": (
        "Hebrew family gathered at Shiloh Tabernacle for feast, "
        "woman sitting alone at edge not eating, Hannah weeping silently at Tabernacle entrance, "
        "lips moving in anguished prayer, oil lamps burning"
    ),
    "Samuel Called": (
        "small boy sleeping in priestly linen on low cot inside ancient sanctuary, "
        "single oil lamp burning low, boy awakening in darkness, "
        "listening to unseen voice calling his name"
    ),
    "The Ark Captured": (
        "Hebrew warriors marching with gold Ark of Covenant onto Philistine battlefield, "
        "Philistine victory, Eli falling backward from his chair at the news, "
        "Ark carried into Philistine captivity"
    ),
    "Give Us a King": (
        "aged prophet Samuel sitting before council of demanding Hebrew elders, "
        "the last judge's sorrow, Israel's demand for a king like the nations around them"
    ),
    "Saul Anointed": (
        "very tall young man in dusty travel clothes searching rocky hills for lost donkeys, "
        "Samuel privately anointing tall Saul with oil, "
        "Saul standing head and shoulders above every man around him"
    ),
    "The Fall of Saul": (
        "king impatiently standing before stone altar, smoke rising, face conflicted, "
        "unlawful sacrifice at Gilgal, Samuel's arrival and rebuke, "
        "the kingdom taken from Saul"
    ),
    "The Boy in Bethlehem": (
        "aged prophet walking with horn of oil into small Judean hill town at dawn, "
        "Samuel before Jesse's seven sons, "
        "youngest shepherd boy called in from the fields"
    ),
    "David and Goliath": (
        "wide valley of Elah between two opposing armies on hilltops, "
        "enormous Philistine warrior in full bronze armor, "
        "small young shepherd boy with only sling and five smooth stones facing him"
    ),
    "Jonathan and David": (
        "Hebrew women dancing in streets celebrating David's victory, tambourines raised, "
        "Jonathan and David swearing covenant friendship, "
        "prince giving young David his own robe and weapons"
    ),
    "The Wilderness Years": (
        "young man running across desert hills at dawn, David fleeing Saul, "
        "caves of Engedi, desert strongholds, "
        "David refusing to raise his hand against the Lord's anointed"
    ),
    "Death of Samuel": (
        "ancient prophet lying still in Hebrew home, all Israel mourning, "
        "the last era of the judges ending, the silence of his absence"
    ),
    "The Witch of Endor": (
        "king in disguise — humble cloak, hood pulled low — walking through dark hills at night, "
        "ghostly apparition of Samuel rising from the ground, Saul's terror"
    ),
    "Mount Gilboa": (
        "mountainside battle at dawn, Hebrew warriors retreating up steep slopes, "
        "King Saul and Jonathan falling in battle on Mount Gilboa, "
        "crown in the dust"
    ),
    "David Crowned King": (
        "young man being anointed by tribal elders in city of Hebron, "
        "David taking Jerusalem the Jebusite fortress, "
        "united kingdom at last established"
    ),
    "The Ark Comes Home": (
        "thirty thousand Hebrews escorting gold Ark of Covenant uphill toward Jerusalem, "
        "King David dancing before the Ark in the streets, crowd celebrating"
    ),
    "The Covenant with David": (
        "king standing in richly appointed cedar-paneled palace, "
        "Nathan bringing the eternal covenant — David's throne forever"
    ),
    "David and Bathsheba": (
        "king walking restlessly on high palace rooftop at evening, Jerusalem spread below, "
        "moonlit night, figure bathing on rooftop below, temptation and fall"
    ),
    "Nathan and the Lamb": (
        "prophet in modest robes standing alone in king's throne room, "
        "Nathan's parable of the ewe lamb, "
        "David's anguished recognition: 'You are the man'"
    ),
    "Absalom's Rebellion": (
        "young woman in torn robes weeping at door, Tamar, "
        "beautiful long-haired prince Absalom on horse fleeing through forest, "
        "hair caught in oak branches, judgment coming"
    ),
    "The Old King": (
        "aged king writing on parchment scroll by lamplight, lyre nearby, David's psalms, "
        "old David on his deathbed giving final charge to young Solomon"
    ),

    # ── Chapter 7: Solomon and the Kingdom Divided ────────────────────────────
    "The Dream at Gibeon": (
        "vast hilltop altar at twilight, smoke rising from a thousand burnt offerings, "
        "young king sleeping on stone floor beside smoking altar under open night sky full of stars"
    ),
    "The Two Mothers": (
        "two women in plain robes standing before young king Solomon on throne, "
        "both reaching toward swaddled infant on low table, Solomon's wisdom revealed"
    ),
    "The Golden Age": (
        "aerial wide shot of Jerusalem at golden hour, prosperous, surrounded by green hills, "
        "Solomon's reign at height, peace from Dan to Beersheba"
    ),
    "Building the Temple": (
        "massive cedar logs being floated down coastal river at dawn, workers guiding them, "
        "massive dressed stones being set with no iron tools heard, "
        "cedar pillars gleaming, craftsmen working under Hiram of Tyre"
    ),
    "The Temple Dedicated": (
        "Jerusalem First Temple filled with thick golden cloud of divine glory, "
        "priests prostrate on floor overwhelmed, unable to stand, "
        "Solomon kneeling before the whole assembly, fire from heaven"
    ),
    "The Queen of Sheba": (
        "vast caravan of camels laden with spices, gold, and precious stones crossing desert at sunset, "
        "Queen of Sheba at Solomon's court, breath taken away by his wisdom"
    ),
    "The Fall of Solomon": (
        "seven hundred foreign wives in elaborate robes in royal hall, "
        "foreign altars on Mount of Olives, "
        "Solomon's heart turning from God in old age"
    ),
    "The Kingdom Divided": (
        "young Rehoboam sitting on his father's throne, listening to elders, "
        "harsh foolish answer, ten northern tribes tearing away, "
        "kingdom split forever at Shechem"
    ),
    "Ahab and Jezebel": (
        "Ahab on northern throne in dark hall, Jezebel in elaborate Phoenician crimson beside him, "
        "Israel's most wicked king and his Phoenician queen, "
        "Baal worship spreading"
    ),
    "Elijah Appears": (
        "wild-looking prophet in rough camel-hair garment and leather belt "
        "walking into luxurious palace throne room, "
        "Elijah standing before Ahab, drought announced"
    ),
    "The Widow's Oil": (
        "Elijah at door of impoverished widow's mudbrick house in Zarephath, "
        "drought landscape, widow's jar of oil that never ran dry"
    ),
    "Mount Carmel": (
        "lone prophet before drenched stone altar on Mount Carmel, "
        "fire falling from clear sky consuming the sacrifice and the water, "
        "450 prophets of Baal watching"
    ),
    "The Still Small Voice": (
        "prophet Elijah collapsed in cave entrance on Mount Sinai, "
        "wind and earthquake and fire passing, then absolute stillness, "
        "the still small voice"
    ),
    "Naboth's Vineyard": (
        "green vineyard on hillside next to palace estate, Naboth's inheritance, "
        "Jezebel's false letter, Naboth stoned, "
        "Elijah meeting Ahab in the vineyard: 'Have you murdered and also taken possession?'"
    ),
    "The Chariot of Fire": (
        "Elijah and Elisha walking together along dusty road at dawn, "
        "fiery chariot of horses descending between them, whirlwind rising, "
        "Elijah taken to heaven, Elisha watching with his cloak"
    ),

    # ── Chapter 8: The Fall of the Kingdoms ──────────────────────────────────
    "Ministry of Elisha": (
        "prophet walking dusty roads through Hebrew villages, "
        "Elisha's miracles — floating axe head in Jordan, Shunammite woman's son raised, "
        "healing of Syrian commander Naaman in Jordan River"
    ),
    "The Prophets Rise": (
        "sun-darkened shepherd Amos in rough sheepskin walking into wealthy Samaria marketplace, "
        "Hosea in northern Israel, Micah in Judean hills — voices crying against injustice"
    ),
    "Fall of Samaria": (
        "massive disciplined Assyrian army marching in columns across northern plain, "
        "banners, chariots, siege towers, "
        "Assyrian siege works around Samaria's walls, northern kingdom's final days, 722 BC"
    ),
    "Isaiah in the Temple": (
        "young Isaiah in fine robes praying in Temple courtyard at dawn, "
        "then the overwhelming throne room vision — seraphim with six wings above the throne, "
        "young Isaiah prostrate: 'I am a man of unclean lips'"
    ),
    "Sennacherib at Gates": (
        "Assyrian king Sennacherib in war camp surrounded by officers, "
        "Assyrian army circling Jerusalem walls, herald shouting insults at defenders, "
        "185,000 Assyrian soldiers struck down overnight, "
        "Hezekiah's prayer answered"
    ),
    "Darkness of Manasseh": (
        "boy of twelve crowned on great throne, young Manasseh, "
        "desecrated Temple with foreign altars, child sacrifice at Hinnom Valley, "
        "Judah's darkest reign"
    ),
    "The Found Book": (
        "eight-year-old Josiah being crowned on throne, "
        "high priest Hilkiah finding ancient Torah scroll in Temple, "
        "young king Josiah tearing his robes in grief at what he hears, "
        "the greatest reform in Judah's history"
    ),
    "The Call of Jeremiah": (
        "young Hebrew man alone in small village of Anathoth at dawn, "
        "the reluctant prophet Jeremiah: 'I do not know how to speak, I am only a child'"
    ),
    "The Final Days": (
        "massive Babylonian army under Nebuchadnezzar marching south, "
        "Jerusalem under eighteen-month siege, Jeremiah imprisoned in courtyard of the guard, "
        "city near its end"
    ),
    "The Temple Burns": (
        "Jerusalem First Temple engulfed in orange fire and black smoke, "
        "Babylonian soldiers watching, weeping captives bound in chains, "
        "586 BC, the day of catastrophe"
    ),
    "The Weeping Prophet": (
        "older Jeremiah sitting alone in smoking ruins of Jerusalem at dusk, "
        "head in hands, ash and broken stone all around, "
        "Lamentations: 'Is it nothing to you, all who pass by?'"
    ),

    # ── Chapter 9: Daniel — Exile in Babylon ─────────────────────────────────
    "The Choice": (
        "line of young Hebrew nobles being inspected by Babylonian officials in palace courtyard, "
        "Daniel and friends chosen, the choice not to defile themselves"
    ),
    "The Statue Dream": (
        "troubled emperor lying awake on his bed in darkness, "
        "Daniel before Nebuchadnezzar interpreting the dream statue "
        "of gold, silver, bronze, iron, and clay"
    ),
    "The Fiery Furnace": (
        "massive golden statue ninety feet tall on vast plain of Dura, glittering in sun, "
        "three young Hebrews standing unbound and unharmed inside roaring furnace, "
        "fourth mysterious figure walking with them"
    ),
    "Madness of the King": (
        "Nebuchadnezzar driven to madness, eating grass in open field, "
        "hair grown long, nails like bird claws, "
        "later restored and testifying about the God of heaven"
    ),
    "Ezekiel's Vision": (
        "Hebrew priest Ezekiel sitting alone beside Chebar canal under vast Babylonian sky, "
        "then the overwhelming vision — four living creatures with four faces, "
        "wheels within wheels of fire, the throne of God, Ezekiel prostrate"
    ),
    "The Strange Acts": (
        "prophet Ezekiel kneeling on Babylonian street drawing Jerusalem's outline "
        "on clay tablet on ground, "
        "enacted prophecies — lying on his side, shaving his head"
    ),
    "The Glory Departs": (
        "prophet lifted in vision, Ezekiel transported in spirit, "
        "the glory of the Lord departing the Temple, "
        "rising above the Mount of Olives and departing east"
    ),
    "The Dry Bones": (
        "prophet Ezekiel standing in vast valley covered with bleached bones as far as eye can see, "
        "breath entering the bones, tendons forming, flesh covering, army rising to life"
    ),
    "The Writing on the Wall": (
        "vast Babylonian banqueting hall, thousand lords at long tables, "
        "ghostly disembodied hand writing glowing Aramaic script on white plaster wall, "
        "Belshazzar's face going pale"
    ),
    "Fall of Babylon": (
        "city of Babylon at night, walls three hundred feet high, "
        "Euphrates running through the heart of the city, "
        "Persian army of Cyrus entering, Babylon fallen in one night, 539 BC"
    ),
    "The Lions Den": (
        "aged Daniel kneeling in prayer in stone pit surrounded by calm lions, "
        "shaft of light from above, "
        "Darius at top of sealed pit calling down at dawn"
    ),
    "Visions of Daniel": (
        "aged Daniel writing by lamplight, Daniel's night visions, "
        "the Ancient of Days on his blazing throne, ten thousand times ten thousand serving him, "
        "one like a Son of Man approaching on the clouds"
    ),

    # ── Chapter 10: The Return — Ezra, Nehemiah, Esther ──────────────────────
    "The Decree of Cyrus": (
        "royal Persian scribe inscribing proclamation, "
        "Cyrus issuing the decree in grand court, "
        "Jewish elders weeping with joy as the news spreads"
    ),
    "The First Return": (
        "heads of Hebrew families gathering in Babylonian courtyard, scrolls open, "
        "great caravan of returning exiles setting out from Babylon toward Jerusalem, "
        "the long road home"
    ),
    "The Altar Rebuilt": (
        "Hebrew men carefully clearing rubble from ancient stone altar platform at dawn, "
        "new altar standing in Jerusalem ruins, "
        "first sacrifice and first Feast of Tabernacles in the ruins"
    ),
    "The Foundation Laid": (
        "Hebrew priests in white linen robes blowing trumpets at Temple foundation, "
        "old men who remembered Solomon's Temple weeping, "
        "young men shouting for joy, voices mingled"
    ),
    "The Long Pause": (
        "Samaritan elders approaching Hebrew leaders with accusations and opposition, "
        "abandoned foundation silent for fifteen years, "
        "Jerusalem ruins and quiet Temple Mount"
    ),
    "Haggai and Zechariah": (
        "older prophet Haggai addressing builders and farmers in public square, "
        "Zechariah with visions of lampstands and olive trees, "
        "the prophets renewing courage to build"
    ),
    "Second Temple Complete": (
        "completed Second Temple — visibly smaller and less ornate than Solomon's but standing, "
        "old men who saw the First Temple weeping, young men shouting for joy, "
        "voices mingled, 516 BC"
    ),
    "For Such a Time — Esther": (
        "aerial of great Persian palace at Susa — marble pillars, gold-leafed walls, gardens, "
        "young queen Esther in royal robes approaching king's throne room, "
        "golden scepter extended toward her"
    ),
    "Ezra Returns": (
        "older scholar Ezra surrounded by ancient scrolls in Babylonian study, "
        "Ezra reading the Law aloud in Jerusalem, people weeping as they hear it"
    ),
    "Walls of Jerusalem": (
        "Nehemiah serving wine to Persian king at marble table, "
        "Nehemiah surveying Jerusalem's broken walls by night on donkey, torchlight and rubble"
    ),
    "The Great Reading": (
        "vast public square inside rebuilt Jerusalem walls, people gathered at dawn, "
        "Ezra on wooden platform reading Torah scroll to thousands standing, "
        "people weeping and celebrating at the same time"
    ),
    "Malachi — Last Prophet": (
        "Hebrew priests offering blemished and sickly animals on Second Temple altar, "
        "Malachi's warning — turn back, the messenger is coming, the day of the Lord"
    ),
    "The Four Hundred Years": (
        "aerial view of Jerusalem and Temple Mount through the passing centuries, "
        "Hellenistic soldiers in Greek armor replacing Persian, then Roman legions, "
        "four hundred years of silence, waiting"
    ),
    "Closing Transition": (
        "night road to Bethlehem, single bright star rising on horizon, "
        "young couple on donkey approaching in the darkness, "
        "the long silence about to break"
    ),
}


def build_prompt(section_title: str, chapter_num: int, emotion: str,
                 setting: str | None = None, key_figures: list[str] | None = None) -> str:
    """Build a full image generation prompt for a specific section.

    Template: [Scene Description], [Character Descriptions], [Emotion/Lighting],
              [Environment Context], cinematic biblical documentary style,
              [Base Style], [Inline Negative]
    """
    env    = CHAPTER_ENVIRONMENT.get(chapter_num, "ancient biblical landscape")
    emo    = EMOTION_STYLE.get(emotion, EMOTION_STYLE["solemn"])
    visual = SECTION_VISUAL.get(section_title, setting or "ancient Near Eastern cinematic scene")

    # Inject character descriptions for visual consistency
    char_parts = []
    if key_figures:
        for fig in key_figures:
            if fig in CHARACTER_APPEARANCE:
                char_parts.append(f"{fig}: {CHARACTER_APPEARANCE[fig]}")
            elif fig in SECONDARY_CHARACTERS:
                char_parts.append(f"{fig}: {SECONDARY_CHARACTERS[fig]}")
            else:
                char_parts.append(fig)

    char_desc = ""
    if char_parts:
        char_desc = "Characters — " + "; ".join(char_parts) + ". "

    return (
        f"{visual}, "
        f"{char_desc}"
        f"{emo}, "
        f"{env}, "
        f"cinematic biblical documentary style, "
        f"{OT_BASE_STYLE}, "
        f"{OT_INLINE_NEGATIVE}"
    )


def get_nation_context(chapter_num: int) -> str:
    """Return the dominant nation style context for a chapter."""
    chapter_nations = {
        1: "Israelites",
        2: "Israelites",
        3: "Israelites",
        4: "Egyptians",
        5: "Israelites",
        6: "Israelites",
        7: "Israelites",
        8: "Israelites",
        9: "Israelites",
        10: "Israelites",
        11: "Israelites",
        12: "Babylonians",
        13: "Babylonians",
        14: "Persians",
        15: "Israelites",
    }
    nation = chapter_nations.get(chapter_num, "Israelites")
    return NATION_STYLE.get(nation, "")


def get_location_context(section_title: str) -> str:
    """Return location-specific visual context if available."""
    location_map = {
        "Adam and Eve":      "Garden_of_Eden",
        "The Fall":          "Garden_of_Eden",
        "The Burning Bush":  "Sinai_Wilderness",
        "The Mountain of God": "Sinai_Wilderness",
        "The Ten Commandments": "Sinai_Wilderness",
        "The Tabernacle":    "Tabernacle",
        "Crossing the Jordan": "Jordan_River",
        "The Fall of Jericho": "Jericho",
        "The Temple Dedicated": "Solomon_Temple",
        "Building the Temple": "Solomon_Temple",
        "Fall of Babylon":   "Babylon",
        "The Fiery Furnace": "Babylon",
        "The Lions Den":     "Babylon",
        "For Such a Time — Esther": "Persian_Susa",
        "Second Temple Complete": "Second_Temple",
    }
    loc_key = location_map.get(section_title)
    if loc_key:
        return LOCATION_BIBLE.get(loc_key, "")
    return ""


def get_negative_prompt() -> str:
    return OT_NEGATIVE


def get_color_grade(chapter_num: int) -> str:
    """Return color grading guidance for a chapter."""
    return CHAPTER_COLOR_GRADE.get(chapter_num, "natural period-accurate colour palette")
