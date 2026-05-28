"""
Old Testament Documentary — Master Visual Reference Bible
=========================================================
Single source of truth for all character, location, object, and atmospheric
visualization across the Old Testament Documentary.

Aesthetic target: @TheBibleWalkReal — ultra-photorealistic cinematic photography,
indistinguishable from a real high-budget film set photograph. NOT painterly,
NOT illustrated. Looks like actual DSLR/cinema camera footage of real actors
in real Levantine landscapes with dramatic natural lighting.

Quality references: The Chosen (TV series), Risen (2016 film),
Kingdom of Heaven (Ridley Scott) — all treated as if photographed in real locations.
"""

# ══════════════════════════════════════════════════════════════════════════════
# PART 1 — UNIVERSAL STYLE (appended to every prompt)
# ══════════════════════════════════════════════════════════════════════════════

OT_BASE_STYLE = (
    "ultra photorealistic, hyperrealistic cinematic photograph, "
    "sharp focus, 8K resolution, real film photography quality, "
    "shot on cinema camera, photographic depth of field, "
    "real Levantine rocky limestone landscape, authentic Israeli hill country, "
    "ancient stone terraced hillsides, scattered scrub vegetation, "
    "dramatic natural lighting, warm golden hour sun, "
    "visible fabric texture (rough linen weave, coarse wool, frayed edges), "
    "realistic weathered skin with visible pores, slightly oily sun-darkened skin, "
    "dust on clothing and sandals, authentic period-accurate Middle Eastern, "
    "foreground subject sharp, background atmospheric haze, "
    "wide angle cinematic composition, no text, no watermarks"
)

# Comprehensive negative prompt (Part 11 of the Visual Bible)
OT_NEGATIVE = (
    "painterly, oil painting, illustration, painting, artistic rendering, watercolor, "
    "digital painting, concept art, stylized, painted style, brush strokes, "
    "modern clothing, modern technology, smartphones, watches, glasses, plastic, metal eyewear, "
    "neon, anime, cartoon, comic-style, 3D render, video game graphics, low quality, blurry, "
    "deformed, extra limbs, bad anatomy, twisted hands, melted faces, six fingers, "
    "blonde Hebrews, white European Jesus, European white people as ancient Israelites, "
    "Renaissance art style, Baroque, neoclassical, Victorian, art nouveau, "
    "oversharpened, modern photograph, HDR, "
    "modern hairstyle, modern haircut, modern beard styling, beard fade, "
    "modern makeup, glossy lipstick, eyeshadow palette, "
    "fantasy armor, sci-fi armor, plate armor, full plate, medieval European armor, knight, "
    "crucifix, cross necklace, Christmas, Easter decorations, "
    "modern footwear, sneakers, boots, modern leather goods, "
    "zippers, buttons, snaps, modern fasteners, "
    "electric lighting, lamp post, street light, neon sign, "
    "modern buildings, glass, concrete, steel, "
    "modern weapons, gun, rifle, pistol, firearm, "
    "text overlays, watermark, signature, logo, copyright, "
    "nudity, sexual content, explicit, graphic violence, gore"
)

# Inline style anchor appended inside every Flux prompt
OT_INLINE_NEGATIVE = (
    "ultra photorealistic photography only, not painterly, not illustrated, not painted, "
    "no fantasy elements, no European medieval aesthetics, "
    "no modern elements, no anime or illustration style, authentic ancient Middle Eastern appearance, "
    "Middle Eastern Levantine features on all Hebrew characters, not European"
)

# ══════════════════════════════════════════════════════════════════════════════
# PART 2 — CHARACTER VISUAL KEYS
# Exact prompt fragments — copy directly into image prompts for consistency.
# ══════════════════════════════════════════════════════════════════════════════

CHARACTER_APPEARANCE: dict[str, str] = {

    # ── Genesis: Primeval ─────────────────────────────────────────────────────
    "Adam": (
        "young Middle Eastern man, strong build, shoulder-length dark hair, dark beard, "
        "olive skin, warm brown eyes, weathered features, simple animal-skin garment around waist, "
        "biblical Adam, photorealistic"
    ),
    "Eve": (
        "young Middle Eastern woman, long flowing dark hair, olive skin, deep brown eyes, "
        "gentle expression, simple natural covering, "
        "biblical Eve, photorealistic"
    ),
    "Cain": (
        "strong Middle Eastern farmer, dark hair, dark beard, brooding intense expression, "
        "dusty rough linen tunic, leather sandals, simple sash, "
        "biblical Cain, photorealistic"
    ),
    "Abel": (
        "young Middle Eastern shepherd, slim build, dark hair, gentle face, "
        "holding a white lamb, simple shepherd's wrap, "
        "biblical Abel, photorealistic"
    ),
    "Noah": (
        "aged patriarch, long gray-white beard, weathered face, strong calloused hands, "
        "simple aged tunic, leather belt, often carrying a tool or staff, "
        "biblical Noah, photorealistic"
    ),

    # ── Genesis: Patriarchs ───────────────────────────────────────────────────
    "Abraham": (
        "aged Hebrew patriarch, long flowing white beard, weathered tan skin, deep wise eyes, "
        "layered linen and wool robes with embroidered borders, striped mantle, leather sandals, "
        "staff in hand, biblical Abraham, photorealistic"
    ),
    "Abram": (
        "older Middle Eastern man of means, long flowing white beard, weathered tan skin, "
        "deep wise eyes, layered linen and wool robes, striped mantle, leather sandals, "
        "biblical Abram, photorealistic"
    ),
    "Sarah": (
        "remarkably beautiful aged Hebrew woman, dignified bearing, "
        "long dark hair with silver streaks under headcovering, refined Middle Eastern features, "
        "layered fine robes, biblical Sarah, photorealistic"
    ),
    "Lot": (
        "middle-aged Hebrew townsman, dark beard, weathered face, "
        "townsman robes finer than nomadic Abraham, biblical Lot, photorealistic"
    ),
    "Hagar": (
        "young Egyptian woman, bronze skin slightly darker than Sarah, dark hair, "
        "beautiful but with worn dignity of a servant, Egyptian-influenced dress with simpler servant robes, "
        "biblical Hagar, photorealistic"
    ),
    "Isaac": (
        "Hebrew patriarch, gentle pensive features, dark hair and beard, "
        "layered wool robes, finer in older age, biblical Isaac, photorealistic"
    ),
    "Rebekah": (
        "beautiful young Hebrew woman at a well, water jar on shoulder, "
        "dark hair, kind determined eyes, simple young woman's robe, "
        "biblical Rebekah, photorealistic"
    ),
    "Esau": (
        "powerfully built hairy Hebrew hunter, reddish-brown body hair, thick red-brown beard, "
        "ruddy complexion, animal skin clothing, bow and quiver on back, "
        "biblical Esau, photorealistic"
    ),
    "Jacob": (
        "Hebrew shepherd, smooth-faced contrast to hairy brother, thoughtful dark eyes, "
        "layered shepherd's wool robes, staff in hand, slight limp after Peniel, "
        "biblical Jacob, photorealistic"
    ),
    "Laban": (
        "older Mesopotamian man, gray-flecked dark beard, calculating eyes, "
        "prosperous Mesopotamian-style robes, biblical Laban, photorealistic"
    ),
    "Leah": (
        "plain kind Hebrew woman, dark hair under headcovering, gentle but weak eyes, "
        "simple matron's robes, biblical Leah, photorealistic"
    ),
    "Rachel": (
        "strikingly beautiful young Hebrew shepherdess, dark flowing hair, "
        "vivid expressive eyes, biblical Rachel, photorealistic"
    ),
    "Joseph": (
        "handsome young Hebrew man, dark wavy hair, intelligent expressive eyes, "
        "wearing an ornate many-colored long-sleeved tunic with embroidered borders, "
        "biblical young Joseph, photorealistic"
    ),
    "Joseph_vizier": (
        "Hebrew man in elaborate Egyptian vizier dress, white linen kilt, gold collar of office, "
        "kohl-lined eyes, distinctly Middle Eastern Hebrew features under Egyptian dress, "
        "biblical Joseph as vizier of Egypt, photorealistic"
    ),
    "Benjamin": (
        "young Hebrew teenager, smaller slim build, sensitive features, dark hair, "
        "simple tunic, biblical Benjamin, photorealistic"
    ),
    "Potiphar": (
        "Egyptian noble captain of the guard, bronze skin, shaved head, kohl-lined eyes, "
        "white linen kilt, gold pectoral, leather belt with sword, "
        "biblical Potiphar, photorealistic"
    ),

    # ── Exodus ────────────────────────────────────────────────────────────────
    "Moses": (
        "aged Hebrew prophet, long flowing white beard reaching chest, weathered face, "
        "intense piercing eyes, long mantle pulled over head, gnarled wooden staff — "
        "NOTE: as Egyptian prince he is young athletic shaved beardless in Egyptian linen kilt and gold collar; "
        "as Midianite shepherd bearded sun-darkened in rough wool tunic, "
        "biblical Moses, photorealistic"
    ),
    "Aaron": (
        "Hebrew high priest, older Hebrew man, dignified full white-streaked beard, "
        "kind authoritative face, white linen ephod, blue robe with golden bells and pomegranates on hem, "
        "ornate gold breastplate set with 12 colored stones, gold turban with engraved plate, "
        "biblical Aaron, photorealistic"
    ),
    "Miriam": (
        "aged Hebrew prophetess, dignified bearing, dark hair under headcovering, "
        "simple robes, tambourine in hand, biblical Miriam, photorealistic"
    ),
    "Pharaoh": (
        "Egyptian pharaoh of the Exodus, hard-eyed regal ruler, "
        "striped Nemes headdress, false ceremonial beard, "
        "ornate gold and lapis pectoral, white linen, "
        "biblical pharaoh of the Exodus, photorealistic"
    ),
    "Jochebed": (
        "Hebrew slave mother, weathered dignified face, simple worn robes, "
        "dust-stained slave clothing, biblical Jochebed, photorealistic"
    ),
    "Jethro": (
        "older Midianite priest, white beard, nomadic robes with cloth wrappings, "
        "dignified bearing, biblical Jethro, photorealistic"
    ),
    "Zipporah": (
        "Midianite woman, dark complexion, intense eyes, "
        "Bedouin-style robes and headscarf, biblical Zipporah, photorealistic"
    ),

    # ── Wilderness and Judges ─────────────────────────────────────────────────
    "Joshua": (
        "Hebrew warrior commander, dark beard, intense battle-hardened face, "
        "leather armor over tunic, bronze helmet, sword at side, "
        "biblical Joshua, photorealistic"
    ),
    "Caleb": (
        "aged Hebrew warrior, white-streaked beard, weathered determined face, "
        "leather armor, biblical Caleb, photorealistic"
    ),
    "Rahab": (
        "beautiful Canaanite woman, dark flowing hair, vibrant eyes, "
        "layered colorful Canaanite robes, scarlet cord in window, "
        "biblical Rahab, restrained, photorealistic"
    ),
    "Deborah": (
        "strong-featured Hebrew prophetess, dignified matron, "
        "layered robes with headcovering, seated beneath a large palm tree, "
        "biblical Deborah, photorealistic"
    ),
    "Barak": (
        "Hebrew warrior general, dark beard, leather armor, "
        "biblical Barak, photorealistic"
    ),
    "Jael": (
        "decisive Kenite tent-dwelling woman, Bedouin-style dress, dark hair, "
        "tent peg and mallet in hand, biblical Jael, restrained, photorealistic"
    ),
    "Gideon": (
        "Hebrew farmer-warrior, dark beard, average build, leather armor over tunic, "
        "holding trumpet and clay jar with torch inside, "
        "biblical Gideon, photorealistic"
    ),
    "Jephthah": (
        "lean weathered Hebrew warrior, complex tortured face, "
        "outlaw-warrior dress, leather armor, biblical Jephthah, photorealistic"
    ),
    "Samson": (
        "immensely muscled Hebrew warrior, tall, long uncut dark hair prominently displayed, "
        "full beard, sun-darkened skin, simple tunic and leather belt, "
        "biblical Samson, photorealistic"
    ),
    "Delilah": (
        "beautiful Philistine woman, dark hair, calculating eyes, "
        "layered colorful Philistine robes, biblical Delilah, restrained, photorealistic"
    ),
    "Ruth": (
        "young Moabite widow, dark hair, gentle determined expression, "
        "simple modest robes, gleaning barley sheaves, "
        "biblical Ruth, photorealistic"
    ),
    "Naomi": (
        "aged Hebrew widow, gray hair under headcovering, weathered grieving face, "
        "dark widow's robes, biblical Naomi, photorealistic"
    ),
    "Boaz": (
        "prosperous older Hebrew landowner, dignified beard, kind eyes, "
        "fine robes with embroidered borders, biblical Boaz, photorealistic"
    ),

    # ── Samuel's Era ──────────────────────────────────────────────────────────
    "Hannah": (
        "young Hebrew woman, careworn gentle face, anguished prayer, "
        "simple dress with headcovering, lips moving silently in prayer, "
        "biblical Hannah, photorealistic"
    ),
    "Eli": (
        "extremely aged Hebrew high priest, nearly blind, heavy frame, long white beard, "
        "faded priestly robes with breastplate, biblical Eli, photorealistic"
    ),
    "Samuel": (
        "aged Hebrew prophet, long white beard and hair, intense piercing eyes, "
        "prophet's mantle, horn of oil in hand, biblical Samuel, photorealistic"
    ),
    "Samuel_boy": (
        "young Hebrew boy in priestly service, dark hair, intelligent serious eyes, "
        "simple white linen child's ephod, biblical young Samuel, photorealistic"
    ),
    "Saul": (
        "tall imposing Hebrew king, head and shoulders above all others in the frame, "
        "strong build, dark hair and beard, haunted suspicious eyes in later scenes, "
        "royal robes with simple Hebrew crown, sword at side, "
        "biblical King Saul, photorealistic"
    ),
    "David": (
        "ruddy young Hebrew shepherd, slightly fair complexion, chestnut-brown hair, "
        "bright intense eyes, slim athletic build, simple shepherd's tunic, sling at belt, "
        "holding a small Hebrew kinnor lyre, biblical young David, photorealistic"
    ),
    "David_king": (
        "Hebrew king, ruddy complexion, chestnut beard, weathered regal face, "
        "royal robes with embroidered borders, simple gold crown, mantle on shoulders, "
        "biblical King David, photorealistic"
    ),
    "Goliath": (
        "giant Philistine warrior, towering nine-foot height above all others, "
        "massive muscular build, full bronze scale armor, feathered Sea Peoples helmet (NOT horned), "
        "bronze greaves on his legs, holding a spear with massive bronze point, huge sword at side, "
        "biblical Goliath, photorealistic"
    ),
    "Jonathan": (
        "young Hebrew prince warrior, dark hair and beard, loyal expression, "
        "royal warrior dress with leather armor, bow and sword, "
        "biblical Jonathan, photorealistic"
    ),
    "Nathan": (
        "older Hebrew prophet, dignified white beard, fearless piercing eyes, "
        "prophet's mantle, simple robes, stands before kings without fear, "
        "biblical Nathan, photorealistic"
    ),
    "Bathsheba": (
        "beautiful young Hebrew woman, dark hair under headcovering, "
        "modest robes, dignified expression, "
        "biblical Bathsheba, restrained, photorealistic"
    ),
    "Absalom": (
        "strikingly handsome Hebrew prince, very long thick dark hair — his defining feature, "
        "polished beard, fine princely robes, biblical Absalom, photorealistic"
    ),
    "Joab": (
        "hard-faced Hebrew general, scarred warrior, "
        "leather armor, captain's mantle, biblical Joab, photorealistic"
    ),

    # ── Kingdom Era ───────────────────────────────────────────────────────────
    "Solomon": (
        "Hebrew king at the peak of glory, distinguished dark beard, "
        "intelligent commanding eyes, layered embroidered royal robes, "
        "gold crown set with precious stones, ceremonial scepter, "
        "biblical King Solomon, photorealistic"
    ),
    "Solomon_old": (
        "aged Hebrew king, white beard, world-weary expression, "
        "still opulent clothing but something behind the eyes that has seen everything, "
        "biblical aged Solomon, photorealistic"
    ),
    "Queen_of_Sheba": (
        "regal Ethiopian queen, deep brown skin, elaborate Sabean royal dress "
        "with gold and ivory ornaments, ornate headpiece, "
        "biblical Queen of Sheba, photorealistic"
    ),
    "Rehoboam": (
        "young Hebrew king, slightly arrogant features, "
        "royal robes less grand than his father Solomon, "
        "biblical Rehoboam, photorealistic"
    ),
    "Jeroboam": (
        "Hebrew rebel king of the north, strong build, dark beard, ambitious eyes, "
        "northern Israelite royal robes, biblical Jeroboam, photorealistic"
    ),
    "Ahab": (
        "Hebrew king of the northern kingdom, powerful build, dark beard, "
        "weak-willed expression dominated by his wife, royal robes, "
        "biblical King Ahab, photorealistic"
    ),
    "Jezebel": (
        "striking Phoenician queen, distinctly non-Hebrew lighter complexion, "
        "elaborate dark hair, intense painted eyes with heavy kohl — she painted her eyes, "
        "ornate Phoenician royal dress with Baal religious ornamentation subtly present, "
        "biblical Queen Jezebel, restrained sacred imagery, photorealistic"
    ),

    # ── Prophets ──────────────────────────────────────────────────────────────
    "Elijah": (
        "wild weathered Hebrew prophet, deeply tanned, intense burning eyes, "
        "long unkempt dark hair, full unkempt beard, "
        "rough haircloth mantle with the hair still on (camel hair, dark brown-black), "
        "leather belt around waist, walking staff, biblical Elijah, photorealistic"
    ),
    "Elisha": (
        "aged Hebrew prophet, completely bald head — this is his defining visual feature, "
        "full beard, weathered piercing eyes, rough prophet's mantle, "
        "biblical Elisha, photorealistic"
    ),
    "Amos": (
        "rough Hebrew shepherd prophet, deeply tanned weathered face, "
        "working man's hands, plain shepherd's robes, very rural appearance, "
        "biblical Amos, photorealistic"
    ),
    "Hosea": (
        "middle-aged Hebrew prophet, careworn tortured but kind eyes, "
        "prophet's mantle, biblical Hosea, photorealistic"
    ),
    "Isaiah": (
        "dignified older Hebrew prophet, white-streaked beard, intense scholar's eyes, "
        "fine prophet's robes with embroidered borders (court access), "
        "ancient scroll in hand, biblical Isaiah, photorealistic"
    ),
    "Micah": (
        "rural Hebrew prophet, sun-darkened weathered face, "
        "simple prophet's robes, biblical Micah, photorealistic"
    ),
    "Hezekiah": (
        "dignified Hebrew king of Judah, dark beard with gray, devout careworn face, "
        "royal robes with crown, spreading a scroll before the Lord, "
        "biblical King Hezekiah, photorealistic"
    ),
    "Sennacherib": (
        "imperious Assyrian emperor, square-cut tightly curled beard — the Assyrian signature look, "
        "hard cruel eyes, tall conical Assyrian crown, embroidered robes with rosettes and gold ornaments, "
        "biblical King Sennacherib, photorealistic"
    ),
    "Manasseh": (
        "Hebrew king with cruel hardened features, royal Judean robes "
        "with subtle pagan ornamentation, biblical King Manasseh, photorealistic"
    ),
    "Josiah": (
        "young Hebrew king with passionate righteous expression, "
        "royal robes with crown, biblical King Josiah, photorealistic"
    ),
    "Jeremiah": (
        "aged weeping Hebrew prophet, tear-streaked face, deep grief, white beard, "
        "plain torn prophet's robes, sometimes sackcloth, wooden yoke around neck in enacted prophecies, "
        "biblical Jeremiah, photorealistic"
    ),
    "Zedekiah": (
        "weak-featured final Hebrew king, hunted look, tattered royal robes, "
        "biblical King Zedekiah, photorealistic"
    ),

    # ── Exilic Era ────────────────────────────────────────────────────────────
    "Nebuchadnezzar": (
        "imposing Babylonian emperor, long luxurious curled beard (longer and more flowing than Assyrian), "
        "commanding eyes, cylindrical Babylonian crown with rosettes, "
        "embroidered polychrome royal robes, "
        "biblical King Nebuchadnezzar, photorealistic"
    ),
    "Nebuchadnezzar_mad": (
        "Babylonian king reduced to madness in field, wild matted long hair like eagle feathers, "
        "overgrown fingernails like bird claws, crawling in field grass, "
        "ragged royal remnants still visible, biblical Nebuchadnezzar madness, restrained, photorealistic"
    ),
    "Daniel": (
        "aged Hebrew statesman in Babylonian court, distinguished Hebrew features, "
        "intelligent serene eyes, white beard, fine but dignified Persian official robes, "
        "biblical Daniel, photorealistic"
    ),
    "Daniel_young": (
        "young Hebrew nobleman, distinctive Hebrew features amid Babylonian court, "
        "intelligent serene eyes, dark beard, fine Babylonian-Persian court robes, "
        "worn with Hebrew dignity, biblical young Daniel, photorealistic"
    ),
    "Shadrach": (
        "young Hebrew nobleman in the Babylonian court, distinct Hebrew features, "
        "fine court robes, courageous calm expression, "
        "biblical Shadrach, photorealistic"
    ),
    "Meshach": (
        "young Hebrew nobleman in the Babylonian court, distinct Hebrew features, "
        "fine court robes, courageous calm expression, "
        "biblical Meshach, photorealistic"
    ),
    "Abednego": (
        "young Hebrew nobleman in the Babylonian court, distinct Hebrew features, "
        "fine court robes, courageous calm expression, "
        "biblical Abednego, photorealistic"
    ),
    "Ezekiel": (
        "Hebrew priest-prophet in exile, dark beard with gray, intense visionary eyes, "
        "white linen ephod under prophet's mantle, biblical Ezekiel, photorealistic"
    ),
    "Belshazzar": (
        "decadent Babylonian co-regent, weak features, "
        "elaborate royal dress dishevelled in feast, biblical Belshazzar, photorealistic"
    ),
    "Darius_Mede": (
        "older Median-Persian ruler, white beard, troubled gracious face, "
        "long flowing Persian royal robes with Median tiara soft cap, "
        "biblical King Darius the Mede, photorealistic"
    ),
    "Cyrus": (
        "imposing Persian emperor, dignified Persian features, characteristic curled beard, "
        "Persian imperial royal robes with crown, biblical King Cyrus the Great, photorealistic"
    ),

    # ── Post-Exilic Era ───────────────────────────────────────────────────────
    "Zerubbabel": (
        "dignified Hebrew governor of the returned exiles, descendant of David, "
        "official but not royal robes, biblical Zerubbabel, photorealistic"
    ),
    "Ezra": (
        "aged Hebrew scribe-priest, distinguished scholar's bearing, white beard, "
        "priestly robes, holding a large scroll, biblical Ezra the scribe, photorealistic"
    ),
    "Nehemiah": (
        "middle-aged Hebrew official, dignified capable face, "
        "Persian court robes initially, working clothes with sword during wall-building, "
        "biblical Nehemiah, photorealistic"
    ),
    "Esther": (
        "strikingly beautiful young Hebrew queen in the Persian court, "
        "dark flowing hair, intelligent gentle eyes, "
        "elaborate Persian queen's robes layered with gold and lapis, ornate Persian crown, "
        "biblical Queen Esther, restrained, photorealistic"
    ),
    "Mordecai": (
        "distinguished older Hebrew man at the Persian king's gate, "
        "dark gray-streaked beard, intelligent watchful eyes, modest Hebrew robes, "
        "biblical Mordecai, photorealistic"
    ),
    "Ahasuerus": (
        "imposing Persian emperor, characteristic curled hair and beard, "
        "elaborate Persian imperial robes embroidered with gold, high Persian crown, "
        "golden ceremonial scepter, biblical King Ahasuerus, photorealistic"
    ),
    "Haman": (
        "Persian noble of Agagite descent, cold proud cruel features, "
        "elaborate Persian noble's robes second only to the king, "
        "biblical Haman, photorealistic"
    ),
    "Malachi": (
        "older Hebrew prophet, dignified bearing, plain prophet's robes, "
        "the last prophet of the Old Testament era, biblical Malachi, photorealistic"
    ),
    "Haggai": (
        "older Hebrew prophet, dignified bearing, prophet's mantle, "
        "biblical Haggai, photorealistic"
    ),
    "Zechariah_prophet": (
        "younger Hebrew prophet with visionary eyes, prophet's robes, "
        "biblical Zechariah post-exilic prophet, photorealistic"
    ),
    "Naaman": (
        "powerful Syrian general, Aramean features, commanding presence, "
        "fine Syrian military dress with chariot armor, "
        "visible white leprous patches on skin, biblical Naaman, restrained, photorealistic"
    ),
    "Job": (
        "Middle Eastern man of Uz, prosperous appearance in early scenes, "
        "same man in ash heap with torn robes and skin sores in suffering scenes, "
        "dignified resilient expression even in anguish, biblical Job, photorealistic"
    ),
    "Jonah": (
        "Hebrew prophet, middle-aged, dark beard, olive skin, plain prophet's robes, "
        "stubborn expression; dripping wet and pale after the great fish, "
        "biblical Jonah, photorealistic"
    ),
    "Abigail": (
        "wise dignified beautiful Hebrew woman, fine matron robes, intelligent kind eyes, "
        "provisions on donkeys nearby, biblical Abigail, photorealistic"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# PART 3 — SUPERNATURAL BEINGS & DIVINE REPRESENTATION
# ══════════════════════════════════════════════════════════════════════════════

SUPERNATURAL_ENTITIES: dict[str, str] = {
    "God_presence": (
        "diffuse warm divine light from above, glowing cloud, no figure visible, "
        "sacred presence implied through light and cloud, photorealistic"
    ),
    "Angel_of_Lord": (
        "luminous brilliant white-gold figure, back-lit and partially obscured by divine glory, "
        "face not clearly visible, tall imposing presence, "
        "biblical Angel of the Lord, photorealistic, sacred restraint"
    ),
    "Angel": (
        "tall luminous male figure in shining white linen robes, "
        "ageless beautiful severe face, radiant inner light, "
        "not cherubic putti, not feminine with halo — tall and severe, "
        "biblical angel, photorealistic"
    ),
    "Angel_warrior": (
        "massive warrior figure in white and light, drawn blazing sword, "
        "overwhelming physical presence, golden-white light, guardian stance, "
        "biblical angel of the Lord with sword drawn, photorealistic, sacred"
    ),
    "Cherubim": (
        "biblical cherubim, four-faced (human, lion, ox, eagle), four wings, "
        "feet like burnished bronze, awesome and strange, NOT Renaissance cherubs, "
        "photorealistic, sacred restraint"
    ),
    "Seraphim": (
        "biblical seraphim, six-winged celestial beings, "
        "two wings covering face, two covering feet, two flying, "
        "burning with divine fire, photorealistic, sacred restraint"
    ),
    "Fourth_in_furnace": (
        "luminous mysterious figure in the midst of furnace flames with three Hebrew youths, "
        "surrounded by fire but untouched, glowing white-gold, face not clearly visible, "
        "biblical fourth figure in the fiery furnace, photorealistic, sacred"
    ),
    "Ancient_of_Days": (
        "awesome enthroned figure clothed in pure white robes, hair like pure wool, "
        "face obscured by divine light, throne of flame, river of fire flowing before, "
        "biblical Ancient of Days vision, photorealistic, sacred restraint"
    ),
    "Burning_Bush": (
        "desert thornbush engulfed in flame yet unconsumed, "
        "leaves and branches visible through the holy fire, "
        "biblical burning bush at Sinai, photorealistic, sacred"
    ),
    "Pillar_Cloud": (
        "massive vertical pillar of glowing white cloud rising into the sky "
        "above a wilderness camp, biblical pillar of cloud by day, photorealistic, sacred"
    ),
    "Pillar_Fire": (
        "massive vertical pillar of bright flame rising into the night sky "
        "above a wilderness camp, biblical pillar of fire by night, photorealistic, sacred"
    ),
    "Glory_cloud": (
        "massive luminous golden cloud of divine glory filling an ancient temple sanctuary, "
        "priests stepping back unable to stand, biblical Glory of the Lord filling Solomon's Temple, "
        "photorealistic, sacred"
    ),
    "Serpent_Eden": (
        "beautiful subtle iridescent serpent creature with intelligent eyes, "
        "coiled around ancient tree branch in lush garden, "
        "biblical serpent in Eden before the curse, restrained sacred imagery, photorealistic"
    ),
    "Chariot_of_Fire": (
        "flaming celestial chariot drawn by flaming horses, descending from tearing sky, "
        "no figure of God within it, biblical chariot of fire taking Elijah, photorealistic, sacred restraint"
    ),
    "Writing_on_Wall": (
        "disembodied human hand appearing in midair, "
        "writing mysterious letters of fire on a white plaster wall, no arm or body attached, "
        "biblical writing on the wall at Belshazzar's feast, photorealistic, sacred"
    ),
    "Jacob_Ladder": (
        "luminous golden staircase rising from earth into starlit heavens, "
        "angelic figures ascending and descending on it, "
        "biblical Jacob's ladder dream vision, photorealistic, sacred, restrained"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# PART 4 — NATION AND PEOPLE PROFILES
# ══════════════════════════════════════════════════════════════════════════════

NATION_STYLE: dict[str, str] = {
    "Israelites": (
        "ancient Semitic people, olive to medium-brown skin tones, dark hair, dark eyes, "
        "men in undyed or earth-toned rough wool and linen robes with fringed edges (tzitzit), "
        "leather sandals, men typically full-bearded (never shaved), women with hair covered, "
        "plain functional clothing — no gold embroidery except priests and royalty, "
        "Bronze Age to Iron Age tools, clay pottery, goatskin water bags, "
        "rough hewn limestone, no dressed stone except Jerusalem"
    ),
    "Egyptians": (
        "ancient North African Mediterranean people, warm bronze-copper skin tones, dark eyes, "
        "men clean-shaven or with neat short kohl-lined hair, white linen kilts (shendyt), "
        "elaborate gold pectoral collars, women in sheer white linen sheath dresses, heavy kohl eyes, "
        "massive sandstone temples with lotus and papyrus columns, hieroglyphic-covered walls, "
        "New Kingdom 18th-19th dynasty aesthetic, Nile river, obelisks, sphinxes"
    ),
    "Philistines": (
        "Sea Peoples of Aegean origin on Canaan coastal plain, "
        "slightly lighter Mediterranean complexion, often beardless (smooth-shaven, unusual for region), "
        "DISTINCTIVE FEATHERED HELMETS — tall row of feathers or stiff bristles on top, "
        "bronze scale armor, round shields with bosses, iron weapons — technological advantage, "
        "Aegean-influenced pottery and architecture, five city-states"
    ),
    "Assyrians": (
        "most fearsome visual identity, square-cut TIGHTLY CURLED black beards — the signature look, "
        "heavy ornate robes covered in rosettes, conical bronze helmets with cheek-pieces, "
        "massive iron-tipped spears, large rectangular wicker shields, "
        "winged-bull lamassu statues at palace gates, "
        "massive stone fortifications, relief-carved walls of conquests"
    ),
    "Babylonians": (
        "similar Mesopotamian base to Assyrians but more LUXURIOUS, "
        "longer more flowing curled beards (less tight than Assyrian), "
        "polychrome glazed brick architecture — brilliant Ishtar Gate blue and gold, "
        "hanging gardens, great stepped ziggurat of Marduk, cylinder seal motifs"
    ),
    "Persians": (
        "Median-Persian dress, long flowing robes very different from Mesopotamian, "
        "soft caps (tiaras) for nobles, curled hair and beards (wave-like not tightly curled), "
        "generally lighter complexion than Mesopotamians, more polished and modern for the era, "
        "Persepolis — massive columned audience halls, double-bull capital columns, "
        "processions of subjected peoples in relief"
    ),
    "Canaanites": (
        "similar Mediterranean features to Hebrews but more colorful layered robes, "
        "Baal and Asherah religious iconography — standing stones, wooden poles, "
        "walled hill city-states, Late Bronze Age to Iron Age I"
    ),
    "Moabites": (
        "similar to Hebrews, cousin nation, slightly more colorful robes, "
        "east of Dead Sea, pastoral culture"
    ),
    "Arameans": (
        "Semitic people north of Israel, modern Syria region, olive skin, dark hair, "
        "Damascus as major city, chariots and cavalry, similar to Israelites but distinct culture"
    ),
    "Edomites": (
        "cousin nation to Hebrews, descendants of Esau, slightly more rugged, "
        "mountain-dwellers south of Dead Sea, reddish desert tones in clothing"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# PART 5 — GEOGRAPHIC LOCATION BIBLE
# ══════════════════════════════════════════════════════════════════════════════

LOCATION_BIBLE: dict[str, str] = {
    "Garden_of_Eden": (
        "lush primeval paradise garden, four rivers flowing outward, "
        "trees heavy with golden fruit, peaceful wild animals, "
        "soft golden eternal light, central glowing Tree of Life, "
        "biblical Garden of Eden, photorealistic"
    ),
    "Ur_Chaldees": (
        "ancient Mesopotamian city of mudbrick flat-roofed houses, "
        "great ziggurat of the moon god rising in the distance, "
        "biblical Ur of the Chaldees, photorealistic"
    ),
    "Mamre": (
        "cluster of ancient massive oak trees at Mamre, "
        "patriarch's goat-hair tents pitched nearby, "
        "biblical oaks of Mamre, photorealistic"
    ),
    "Sodom_Gomorrah": (
        "prosperous ancient walled cities of the plain consumed by fire and burning sulfur "
        "falling from a darkened sky, towering pillar of smoke and flame, "
        "biblical destruction of Sodom and Gomorrah, restrained, photorealistic"
    ),
    "Mount_Moriah": (
        "high wooded hill in the land of Canaan, stone altar at summit, "
        "wood arranged upon it, ram caught in thicket nearby, "
        "biblical Mount Moriah, photorealistic"
    ),
    "Egypt_Nile": (
        "ancient Egypt, the Nile flowing through desert, distant pyramids already a thousand years old, "
        "massive temple complexes with lotus-pillar courtyards, hieroglyphic walls, "
        "slave brick-making operations, sphinxes flanking processional ways, "
        "biblical Egypt, photorealistic"
    ),
    "Sinai": (
        "massive desert mountain rising from a barren plain, "
        "wrapped in thick dark cloud, lightning flashing from within, fire on the summit, "
        "smoke pouring out, trembling and terrible, "
        "biblical Mount Sinai in the giving of the Law, photorealistic"
    ),
    "Red_Sea": (
        "wide sea miraculously parted, towering walls of water on either side, "
        "dry seabed exposed below, fish visible swimming in the water walls, "
        "biblical Red Sea crossing, photorealistic"
    ),
    "Tabernacle": (
        "biblical Tabernacle in the wilderness, portable sanctuary tent with wooden frame, "
        "layered curtains, white linen outer court fence, golden lampstand glowing inside, "
        "cloud of glory hovering above, vast desert camp surrounding, "
        "photorealistic"
    ),
    "Canaan_Hills": (
        "hilly Levantine landscape, ancient olive groves on terraced hillsides, "
        "scattered ancient stone-walled villages on hilltops, "
        "biblical land of Canaan, photorealistic"
    ),
    "Jordan_River": (
        "swift Jordan river miraculously dammed, dry riverbed exposed, "
        "water piled up on the upstream side, biblical crossing of the Jordan, photorealistic"
    ),
    "Jericho": (
        "ancient circular walled city in the Jordan valley, massive mudbrick walls, "
        "palm tree groves nearby, oasis, city of palms, "
        "biblical Jericho, photorealistic"
    ),
    "Jerusalem_Davidic": (
        "ancient Jerusalem on its hilltop, City of David compact stone buildings "
        "on narrow ridge above Kidron Valley, early fortifications, "
        "biblical Jerusalem in David's time, photorealistic"
    ),
    "Jerusalem_Solomon": (
        "ancient Jerusalem on its hilltop, Solomon's First Temple at the northern end "
        "gleaming with gold and white limestone, walled city descending the slopes, "
        "biblical Jerusalem in the time of Solomon, photorealistic"
    ),
    "Jerusalem_ruins": (
        "Jerusalem in ruins after Babylonian destruction, charred walls, "
        "burned Temple, rubble and ash, smoke still rising, "
        "biblical Jerusalem after 586 BC, photorealistic"
    ),
    "Solomon_Temple": (
        "biblical Solomon's Temple, white limestone walls overlaid with gold, "
        "twin bronze pillars Jachin and Boaz at the entrance, cedar courtyard with golden ornamentation, "
        "the great bronze sea on twelve bronze oxen, golden lampstands glowing, "
        "biblical First Temple, photorealistic, sacred"
    ),
    "Valley_Elah": (
        "wide flat valley between two hills, Hebrews on one side, Philistines on the other, "
        "stream running through the middle, biblical Valley of Elah, photorealistic"
    ),
    "Mount_Carmel": (
        "coastal mountain ridge with sweeping views to the Mediterranean Sea, "
        "scrub forest and rocky outcrops, biblical Mount Carmel, photorealistic"
    ),
    "Samaria": (
        "capital of the northern kingdom on hilltop, Ahab's palace, "
        "Phoenician-influenced architecture, ivory decorations, "
        "biblical Samaria, photorealistic"
    ),
    "Babylon": (
        "legendary ancient Babylon, massive walls wider than chariots, "
        "Ishtar Gate in brilliant blue glazed brick with golden bulls and dragons, "
        "great ziggurat of Marduk rising in stages, hanging gardens cascading from terraces, "
        "Euphrates flowing through stone channels in the heart of the city, "
        "biblical Babylon, photorealistic"
    ),
    "Chebar_exile": (
        "Babylonian canal (Chebar River), willow trees on banks, "
        "Hebrew exile community of reed huts and mudbrick homes, "
        "date palms, distant ziggurat on horizon, the weight of displacement, "
        "photorealistic"
    ),
    "Persian_Susa": (
        "magnificent Persian palace complex at Susa, marble columns, "
        "brilliant glazed brick walls, hanging tapestries, gold ornamentation, "
        "biblical Susa of Esther's day, photorealistic"
    ),
    "Second_Temple": (
        "rebuilt Jerusalem Temple on same foundation, "
        "visibly smaller and less ornate than Solomon's First Temple — humble stone, "
        "no gold overlay, surrounded by rubble and rebuilding Jerusalem, "
        "biblical Second Temple, photorealistic"
    ),
    "Bethlehem": (
        "small hill town south of Jerusalem, stone houses, olive groves, sheep folds, "
        "night road to Bethlehem, single bright star rising on horizon, "
        "biblical Bethlehem, photorealistic"
    ),
    "Nineveh": (
        "massive walled Assyrian capital, towering city mound, "
        "palaces guarded by colossal winged-bull lamassu sculptures, "
        "biblical Nineveh, photorealistic"
    ),
    "Noah_Ark": (
        "massive boxy wooden ark, three decks, single door in the side, "
        "pitch-blackened exterior, no mast or sail, biblical Noah's ark, photorealistic"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# PART 6 — KEY STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

STRUCTURES: dict[str, str] = {
    "Ark_Covenant": (
        "biblical Ark of the Covenant, golden chest with two sculpted golden cherubim "
        "with wings stretched forward on the lid, golden carrying poles through side rings, "
        "glowing with sacred presence, photorealistic, sacred"
    ),
    "Fiery_furnace": (
        "massive ancient Mesopotamian industrial furnace, brick-walled, "
        "intense white-hot flames roaring from the opening and bursting from the top, "
        "biblical fiery furnace of Babylon, photorealistic"
    ),
    "Lions_den": (
        "deep stone pit with heavy stone covering the opening, "
        "magnificent Persian lions visible inside, Persian royal seals on the stone, "
        "shaft of light from above, photorealistic"
    ),
    "Tower_Babel": (
        "massive stepped ziggurat tower under construction, scaffolding climbing its sides, "
        "brick-making operations at the base, distinct from Egyptian pyramid (stepped vs smooth), "
        "biblical Tower of Babel on the plain of Shinar, photorealistic"
    ),
    "Patriarchal_tent": (
        "low wide black goat-hair tent, open sides for ventilation, "
        "fabric panels rolled up, cluster of tents for the patriarch's household, "
        "flocks of sheep nearby, photorealistic"
    ),
    "Ark_Noah": (
        "massive boxy wooden ark, pitch-blackened exterior, three decks, "
        "single door in the side, single window near the top, "
        "no mast or sail or oars — approximately 450 feet long, "
        "visually gigantic scale, animals approaching in pairs, "
        "biblical Noah's ark, photorealistic"
    ),
}

# ══════════════════════════════════════════════════════════════════════════════
# SUPPORTING STYLE TABLES
# ══════════════════════════════════════════════════════════════════════════════

EMOTION_STYLE: dict[str, str] = {
    "awe":            "divine golden light breaking through darkness, volumetric god-rays, vast scale, sacred haze",
    "dark_and_tense": "deep shadow and smoke, storm clouds, blood-red sky at horizon, high contrast chiaroscuro",
    "dramatic":       "high contrast directional light, deep shadow, Caravaggio chiaroscuro, intense focal moment",
    "hopeful":        "warm sunrise light, soft golden hour glow, open horizon, optimistic framing, warm honey tones",
    "solemn":         "muted warm tones, single oil lamp or torch light, heavy atmosphere, still composition",
    "mysterious":     "deep shadow, flickering torchlight, desert night, starlit sky, hidden forms in darkness",
    "triumphant":     "golden light, wide epic scope, raised banners, crowds, warm triumphant honey-gold palette",
    "epic_grandeur":  "sweeping aerial perspective, monumental architecture, vast landscape, awe-inspiring scale",
    "grief":          "grey cold tones, hunched figures, ash and smoke, tears on weathered faces, broken forms",
    "supernatural":   "unearthly luminous amber and white, impossible radiance, diffuse sacred haze, god-rays",
}

CHAPTER_ENVIRONMENT: dict[int, str] = {
    1:  "primordial ancient earth, Garden of Eden, pre-flood wilderness, early Bronze Age human settlements",
    2:  "post-flood new world, ancient Mesopotamian city-state of Ur, Canaan rolling hills, desert trade routes",
    3:  "Canaan hill country, Haran in northern Mesopotamia, trade caravans, Nile delta Egypt grain stores",
    4:  "New Kingdom Egypt, mud-brick slave quarters, Nile River valley, Sinai peninsula desert",
    5:  "Sinai wilderness, desert canyons, stone mountains, Tabernacle tent complex, plains of Moab",
    6:  "Canaan hill country, Jordan River valley, walled ancient Canaanite cities, wheat fields, Philistine coast",
    7:  "Shiloh Tabernacle, Philistine cities, Judean wilderness caves, early Jerusalem fortifications",
    8:  "Jerusalem city of David, David's palace, Temple Mount, Israelite capital at its height",
    9:  "Jerusalem at peak glory, Solomon's First Temple, Phoenician-influenced architecture, Solomon's palace",
    10: "Northern Israelite hill towns, Samaria, Mount Carmel, Sinai wilderness, Phoenician coastal town Zarephath",
    11: "Assyrian siege warfare, Babylon approaching, Jerusalem walls, burning ancient cities, Judean hills",
    12: "Neo-Babylonian empire, massive ziggurat city of Babylon, plain of Dura, Persian palace architecture",
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
        "rich Egyptian linen whites and painted gold for Joseph's rise, earthy ochre for caravans",
    4:  "bleached oranges and browns for Egyptian slavery, deep Nile blues for Moses' birth, "
        "Egyptian palace gold and lapis lazuli, blood red for the plagues, "
        "turquoise and white for the Red Sea crossing",
    5:  "sun-bleached desert tones darkening as Sinai approaches, "
        "smoky blacks and deep storm blues with sudden orange-red fire for the theophany, "
        "warm gold and linen white for Tabernacle interiors, dusty muted for forty years",
    6:  "harder more weathered — Bronze Age to early Iron Age palette, "
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
    15: "muted domestic human-scale — fragile warmth of post-exilic community, "
        "Second Temple in humble grey stone, Esther's court in opulent gold-crimson, "
        "closing in deep silent blue before the star rises over Bethlehem",
}

# ══════════════════════════════════════════════════════════════════════════════
# PART 6 (continued) — SECTION-LEVEL SCENE DESCRIPTIONS
# ══════════════════════════════════════════════════════════════════════════════

SECTION_VISUAL: dict[str, str] = {

    # ── Chapter 1: Creation to the Flood ──────────────────────────────────────
    "Cold Open": (
        "vast cosmic void, infinite black space with faintest blue mist, "
        "single beam of warm golden light beginning to pierce the darkness, "
        "volumetric light rays, infinite darkness before creation, "
        "deep navy to gold gradient, cinematic wide shot, sacred restraint"
    ),
    "The Creation": (
        "first light of creation bursting through cosmic darkness, divine golden radiance, "
        "waters separating from sky, mountains rising from primordial sea, "
        "sun rising for the first time over the new world, "
        "silhouette of man being formed from red desert clay and dust, no visible face of God, "
        "radiant golden-white light pouring from unseen divine presence"
    ),
    "Adam and Eve": (
        "lush primeval paradise garden, four rivers flowing outward, "
        "towering ancient trees heavy with glowing fruit, central Tree of Life glowing softly, "
        "two silhouettes walking hand in hand through tall grass, "
        "peaceful wild animals nearby, soft golden eternal light"
    ),
    "The Fall": (
        "beautiful iridescent serpent creature with intelligent gleaming eye coiled in ancient tree, "
        "woman's hand reaching toward glowing forbidden fruit (fig or pomegranate, not apple), "
        "golden garden light beginning to dim at the edges, "
        "two figures crouched hidden among large leaves, ashamed and afraid"
    ),
    "Cain and Abel": (
        "two stone altars side by side in barren field at dusk, "
        "one altar with smoke rising straight to heaven, other smoke blowing sideways in wind, "
        "one brother kneeling in prayer, one standing in dark silent rage, "
        "shadow of violence in the air, warm golden sunset behind"
    ),
    "Corruption of Mankind": (
        "aerial shot of ancient sprawling city at dusk, smoke rising from many fires, "
        "Mesopotamian mud-brick architecture, figures in corruption and violence below, "
        "crumbling civilization, foreboding darkness gathering on horizon"
    ),
    "Noah and the Flood": (
        "aged patriarch Noah on hillside gazing at sky as first dark storm clouds gather, "
        "enormous pitch-blackened wooden ark on mountain slope, no mast or sail, "
        "animals approaching in pairs, last sunlight before the deluge, "
        "rain beginning to fall, golden hour giving way to storm"
    ),
    "The Covenant with Noah": (
        "brilliant full rainbow arching across clearing sky over fresh wet landscape, "
        "golden hour after the storm, Noah kneeling at simple stone altar, "
        "white dove returning with fresh olive branch, green world reborn"
    ),
    "The Tower of Babel": (
        "vast flat plain of Shinar at dawn, massive stepped ziggurat under construction, "
        "scaffolding climbing its sides, brick-making operations at base, "
        "distinct from Egyptian pyramids (stepped not smooth), "
        "confusion breaking out — people gesturing, unable to understand each other"
    ),
    "Closing Transition": (
        "lone elderly man standing at gate of ancient Mesopotamian city at dawn, "
        "gazing at vast desert ahead, stars still bright overhead, "
        "the call going out, hopeful and mysterious"
    ),

    # ── Chapter 2: Abraham — Father of Nations ────────────────────────────────
    "The Calling of Abraham": (
        "bustling ancient Mesopotamian marketplace of Ur, great ziggurat in background, "
        "elderly Abraham in striped mantle at edge of city gates at night, "
        "vast desert ahead, stars brilliant overhead"
    ),
    "The Covenant": (
        "vast desert sky at night, infinite stars stretching to horizon, "
        "single small silhouette of elderly Abraham with head tilted back gazing upward, "
        "descendants promised as countless as the stars, starlit covenant in Canaan desert"
    ),
    "The Three Visitors": (
        "three luminous robed travelers approaching black goat-hair tent "
        "under ancient massive oak trees at Mamre, midday heat shimmer, "
        "three mysterious figures, sacred hospitality, Abraham running to meet them"
    ),
    "Sodom and Gomorrah": (
        "twin ancient walled cities consumed by fire and burning sulfur falling from darkened sky, "
        "massive columns of black smoke rising to heaven, "
        "fleeing figures, distant pale pillar-of-salt figure looking back, "
        "Abraham watching from hilltop, smoke of the land like a furnace"
    ),
    "The Birth of Isaac": (
        "elderly Sarah holding newborn baby in her arms, face streaked with tears of joy, "
        "soft warm lamplight interior of desert tent, intimate miraculous birth, "
        "her ancient face transformed by impossible joy"
    ),
    "The Binding of Isaac": (
        "elderly Abraham with raised knife over bound teenage Isaac on stone altar, "
        "wood arranged beneath, ram caught by horns in thorny thicket nearby, "
        "angel's hand reaching from above to stop the blade, Mount Moriah, "
        "dramatic golden light descending from above"
    ),
    "Sarah and Rebekah": (
        "aged Abraham kneeling at entrance of stone burial cave of Machpelah, mourning Sarah, "
        "beautiful young Rebekah with water jar on shoulder approaching stone well "
        "surrounded by sheep, golden hour, Rebekah at the well"
    ),
    "Jacob and Esau": (
        "two brothers at tent camp — powerfully built hairy Esau returning with game, "
        "smooth-faced thoughtful Jacob holding bowl of red stew, tense family scene, "
        "Rebekah praying for her unborn twins"
    ),
    "Jacob's Ladder": (
        "Jacob sleeping on open ground with single stone as pillow, "
        "luminous golden staircase ascending from earth to heaven, "
        "angelic figures ascending and descending, vast starry night sky, "
        "Bethel, the gate of heaven"
    ),
    "Jacob Leah Rachel": (
        "strikingly beautiful young Rachel approaching stone well surrounded by sheep, "
        "Jacob rolling great stone from well mouth with one arm, "
        "uncle Laban's household, seven years of labor for love"
    ),
    "Jacob Wrestles God": (
        "lone Jacob at edge of moonlit Jabbok River at night, absolute isolation, "
        "two figures locked in intense struggle at river's edge in darkness, "
        "dawn light breaking on horizon, Jacob limping at first light"
    ),
    "The Reconciliation": (
        "Jacob limping across open plain bowing to ground repeatedly, "
        "Jacob and Esau embracing with tears in open Canaanite land"
    ),
    "Joseph and His Brothers": (
        "teenage Joseph in ornate many-colored long-sleeved striped tunic "
        "walking through tall grass, brothers watching from distance with cold jealous expressions, "
        "young man thrown into empty stone cistern, camel caravan passing toward Egypt"
    ),
    "Joseph in Egypt": (
        "young Joseph in fine Egyptian vizier dress, white linen kilt, gold collar of office, "
        "kohl-lined eyes, distinctly Hebrew features under Egyptian dress, "
        "same man kneeling in Egyptian prison, hands bound, face resolute and trusting"
    ),
    "Dreams of Pharaoh": (
        "two Egyptian officials in dim prison cell, troubled expressions, "
        "Joseph standing before seated Pharaoh on great gold throne, "
        "interpreting the dream of seven fat and seven gaunt cows by the Nile"
    ),
    "The Brothers Return": (
        "ten travel-worn Hebrew brothers in dusty robes bowing low before Egyptian vizier "
        "on raised dais, great grain stores of Egypt around them"
    ),
    "Jacob Comes to Egypt": (
        "vast caravan of Hebrew families, flocks, tents, and wagons moving across desert "
        "from Canaan into Egypt's eastern delta, epic wide shot, dust rising, Goshen ahead"
    ),

    # ── Chapter 3: Moses — Deliverer of Israel ────────────────────────────────
    "The Birth of Moses": (
        "Egyptian soldiers patrolling Hebrew slave quarters at night, torches, "
        "Hebrew mother Jochebed placing woven papyrus basket in Nile reeds at dawn, "
        "Pharaoh's daughter walking to the riverside with servants"
    ),
    "Moses Flees Egypt": (
        "young Egyptian-raised Moses in royal linen, colonnaded palace, hieroglyphs on walls, "
        "same man in rough shepherd's cloak crossing empty Sinai desert, "
        "fugitive between two worlds"
    ),
    "The Burning Bush": (
        "elderly shepherd Moses walking through rocky Sinai wilderness, "
        "solitary shepherd before single desert thornbush engulfed in flame yet unconsumed — "
        "leaves and branches visible through the holy fire, "
        "sandals removed on holy ground, face turned away"
    ),
    "Moses Returns": (
        "Moses and Aaron walking up vast Egyptian temple staircase, "
        "dwarfed by colossal columns and statuary covered in hieroglyphs, "
        "approaching Pharaoh's throne room"
    ),
    "Let My People Go": (
        "Moses and Aaron before enthroned Pharaoh surrounded by guards and priests, "
        "Aaron's staff becoming a serpent swallowing the magicians' serpents, "
        "battle of wills in the throne room of Egypt"
    ),
    "The Ten Plagues": (
        "Nile River running blood red from bank to bank, "
        "swarms of locusts blackening Egyptian sky over green crops, "
        "hailstones with fire mingled falling on Egypt while Goshen is untouched, "
        "three days of impenetrable supernatural darkness — Egyptians cannot see, "
        "Hebrew quarter glowing with lamplight inside"
    ),
    "The Passover": (
        "blood of spotless lamb smeared on the lintel and side doorposts of humble Hebrew dwelling at night, "
        "Hebrew family eating in robes with staffs ready, dark empty Egyptian streets outside, "
        "Egyptian families in grief in their houses, angel of death passing as shadow over doorposts"
    ),
    "The Exodus": (
        "vast columns of Hebrews and their flocks walking through desert, "
        "massive vertical pillar of glowing white cloud rising before them by day, "
        "two million people moving as one body, epic wide shot, dust rising"
    ),
    "The Red Sea": (
        "towering walls of water on both sides, dry seabed exposed below, "
        "millions of Hebrews walking across under stars, "
        "Egyptian chariots pursuing at shore's edge, sea wall beginning to collapse"
    ),
    "The Song of Moses": (
        "elderly Moses on rocky eastern shore at dawn with arms raised toward sky, "
        "Miriam with tambourine leading women in dance, "
        "triumphant celebration as Egypt lies drowned behind them"
    ),

    # ── Chapter 4: The Law and the Wilderness ─────────────────────────────────
    "The Mountain of God": (
        "vast Hebrew camp spread across desert plain at foot of towering Mount Sinai, "
        "mountain wrapped in thick dark cloud, lightning cracking the summit, "
        "fire and smoke, two million Israelites forbidden to approach, watching below"
    ),
    "The Ten Commandments": (
        "two large stone tablets carved with ancient Hebrew letters "
        "held in the aged weathered hands of Moses descending the smoking mountain, "
        "sky split with lightning, mountain fire behind"
    ),
    "The Covenant in Blood": (
        "Moses reading aloud from scroll before vast assembled crowd at mountain's foot, "
        "stone altar, blood of covenant sprinkled on assembled people"
    ),
    "The Golden Calf": (
        "golden calf idol on stone pedestal gleaming in desert sun, "
        "Hebrews dancing around it in pagan revelry, "
        "Moses descending from smoke-covered mountain above, righteous fury on his face"
    ),
    "The Radiant Face": (
        "Moses descending with veil over radiant glowing face, "
        "Israelites drawing back in fear, glory reflecting from his skin, "
        "face too bright to look at directly"
    ),
    "The Tabernacle": (
        "Hebrew artisans carefully working gold-overlaid wood and fine linen, "
        "intricate craftwork by Bezalel, "
        "portable sanctuary with golden lampstand (seven-branched menorah) glowing inside linen tent, "
        "cloud of glory hovering above, desert camp surrounding"
    ),
    "The Law": (
        "Aaron in full high priestly regalia — white linen ephod, blue robe "
        "with golden bells and pomegranates on hem, ornate gold breastplate set with twelve stones, "
        "gold turban with engraved plate, Tabernacle interior, incense rising"
    ),
    "The Twelve Spies": (
        "twelve men in dust-stained robes leaving vast camp at edge of wilderness, "
        "Caleb and Joshua carrying enormous cluster of grapes on pole between two men, "
        "returning from Canaan with mixed reports"
    ),
    "Forty Years": (
        "endless desert stretching to horizon in every direction, "
        "Hebrew camp of goat-hair tents, sun beating down, "
        "same landscape year after year, a generation dying in the wilderness"
    ),
    "Death of Miriam Aaron": (
        "aged Miriam lying still in desert tent, women mourning around her, "
        "Aaron in full priestly robes on summit of Mount Hor, peaceful death"
    ),
    "Balak and Balaam": (
        "worried Moabite king on high balcony overlooking vast Hebrew camp below, "
        "Balaam the Aramean diviner on donkey on Moabite road, "
        "angel with drawn sword blocking the path"
    ),
    "The Farewell of Moses": (
        "aged Moses with long flowing white beard and staff "
        "standing before vast assembly of Hebrews on plains of Moab, "
        "Jordan River valley visible in distance, final addresses to the nation"
    ),
    "The Death of Moses": (
        "aged Moses climbing steep mountain path alone at sunrise, staff in hand, final ascent, "
        "solitary figure on summit of Mount Nebo gazing at sunlit promised land across Jordan far below, "
        "Canaan visible but unreachable"
    ),

    # ── Chapter 5: The Promised Land ──────────────────────────────────════════
    "Crossing the Jordan": (
        "spring-flooded Jordan River running powerful and brown, "
        "priests carrying gold Ark of Covenant stepping into the water, "
        "river dammed up, millions crossing on dry ground"
    ),
    "The Fall of Jericho": (
        "Hebrew army marching silently around ancient circular walled city of Jericho day after day, "
        "seven circuits on the seventh day, seven shofars (ram's horn trumpets) sounding, "
        "massive mudbrick walls collapsing in cloud of dust and rubble"
    ),
    "The Conquest": (
        "Joshua's army in battle across Canaanite hill country, "
        "cities falling one by one, Israel claiming the land, "
        "Gibeonites in deliberately worn travel-clothes with moldy bread"
    ),
    "Dividing the Land": (
        "older Joshua sitting in tent with tribal elders around him, "
        "large map of Canaan on ground, tribes receiving their inheritance by lot"
    ),
    "Choose This Day": (
        "aged warrior Joshua standing before assembled nation at Shechem, "
        "grey hair and deeply weathered face, "
        "final challenge: choose this day whom you will serve"
    ),
    "The Cycle of Judges": (
        "young generation of Hebrew children playing in village, oblivious to history, "
        "the cycle beginning again — sin, oppression, cry, deliverance, peace, repeat"
    ),
    "Deborah and Barak": (
        "Deborah sitting under large date palm tree judging Israel, "
        "Hebrew army routing Canaanite iron chariots in flooded Kishon Valley, "
        "Jael with tent peg in her hand"
    ),
    "Gideon": (
        "young Hebrew farmer hiding inside stone wine press secretly threshing wheat, anxious, "
        "three hundred men with clay jars and torches surrounding night-time enemy camp, "
        "jars smashed simultaneously revealing 300 torches at once, chaos erupting"
    ),
    "Samson": (
        "enormous Samson pushing great stone pillars of crowded Philistine temple, "
        "his very long uncut dark hair flowing, roof beginning to collapse, "
        "angel in wheat field at sunset before his mother in background"
    ),
    "Dark End of Judges": (
        "single oil lamp burning low in empty Hebrew village street at night, "
        "tribal Israel in chaos, everyone doing what was right in their own eyes, "
        "darkest period, no king, no prophet"
    ),
    "The Book of Ruth": (
        "Ruth gleaning barley sheaves in ancient Judean field at golden harvest, "
        "Ruth and Naomi on dusty road, two women alone on long journey, "
        "Bethlehem ahead, loyal companionship"
    ),

    # ── Chapter 6: Samuel, Saul, and the First King ───────────────────────────
    "Hannah and Samuel": (
        "Hebrew family gathered at Shiloh Tabernacle for feast, "
        "Hannah sitting alone at edge weeping, lips moving in silent anguished prayer "
        "at Tabernacle entrance, oil lamps burning"
    ),
    "Samuel Called": (
        "small boy Samuel sleeping in priestly linen on low cot inside ancient sanctuary, "
        "single oil lamp burning low, boy awakening in darkness, "
        "listening to unseen voice calling his name"
    ),
    "The Ark Captured": (
        "Hebrew warriors marching with gold Ark of Covenant onto Philistine battlefield, "
        "Philistine victory, aged Eli falling backward from his chair at the news, "
        "Ark carried into Philistine captivity"
    ),
    "Give Us a King": (
        "aged Samuel sitting before council of demanding Hebrew elders, "
        "the last judge's sorrow, Israel's demand for a king like the nations"
    ),
    "Saul Anointed": (
        "very tall young Saul in dusty travel clothes searching rocky hills for lost donkeys, "
        "Samuel privately anointing tall Saul with oil, "
        "Saul standing head and shoulders above every man around him"
    ),
    "The Fall of Saul": (
        "Saul impatiently standing before stone altar, smoke rising, face conflicted, "
        "unlawful sacrifice at Gilgal, Samuel's arrival and rebuke, "
        "the kingdom taken from Saul"
    ),
    "The Boy in Bethlehem": (
        "aged Samuel walking with horn of oil into small Judean hill town at dawn, "
        "Samuel before Jesse's sons, youngest shepherd David called in from the fields"
    ),
    "David and Goliath": (
        "wide Valley of Elah between two opposing armies on hilltops, stream running through middle, "
        "giant Philistine Goliath in full bronze scale armor with feathered Sea Peoples helmet, "
        "towering nine feet above all others, "
        "small ruddy young David with sling and five smooth stones facing him across the valley"
    ),
    "Jonathan and David": (
        "Hebrew women dancing in streets celebrating David's victory, tambourines raised, "
        "Jonathan giving David his own robe and weapons, swearing covenant friendship, "
        "inseparable bond"
    ),
    "The Wilderness Years": (
        "David running across desert hills at dawn, caves of Engedi, "
        "desert strongholds, David refusing to raise his hand against Saul in cave darkness"
    ),
    "Death of Samuel": (
        "ancient Samuel lying still in Hebrew home, all Israel mourning, "
        "the last era of the judges ending, his absence a profound silence"
    ),
    "The Witch of Endor": (
        "Saul in disguise with cloak and hood pulled low walking through dark hills at night, "
        "ghostly apparition of Samuel rising from the ground, Saul's terror"
    ),
    "Mount Gilboa": (
        "mountainside battle at dawn, Hebrew warriors retreating up steep slopes, "
        "King Saul and Jonathan falling in battle on Mount Gilboa, crown in the dust"
    ),
    "David Crowned King": (
        "young David being anointed by tribal elders in city of Hebron, "
        "David taking Jerusalem the Jebusite fortress, "
        "united kingdom at last established"
    ),
    "The Ark Comes Home": (
        "thirty thousand Hebrews escorting gold Ark of Covenant uphill toward Jerusalem, "
        "King David dancing before the Ark in the streets, crowd celebrating"
    ),
    "The Covenant with David": (
        "David standing in richly appointed cedar-paneled palace, "
        "Nathan bringing the eternal covenant — David's throne forever"
    ),
    "David and Bathsheba": (
        "David walking restlessly on high palace rooftop at evening, Jerusalem spread below, "
        "moonlit night, temptation and fall"
    ),
    "Nathan and the Lamb": (
        "Nathan in modest robes standing alone in king's throne room, "
        "parable of the ewe lamb, David's anguished recognition: 'You are the man'"
    ),
    "Absalom's Rebellion": (
        "young woman Tamar in torn robes weeping at door, "
        "strikingly handsome Absalom with very long thick dark hair on horse, "
        "fleeing through forest, hair caught in oak branches, judgment coming"
    ),
    "The Old King": (
        "aged David writing on parchment scroll by lamplight, Hebrew kinnor lyre nearby, "
        "old David on his deathbed giving final charge to young Solomon"
    ),

    # ── Chapter 7: Solomon and the Kingdom Divided ────────────────────────────
    "The Dream at Gibeon": (
        "vast hilltop altar at twilight, smoke rising from a thousand burnt offerings, "
        "young Solomon sleeping on stone floor beside smoking altar under open night sky"
    ),
    "The Two Mothers": (
        "two women in plain robes standing before young Solomon on throne, "
        "both reaching toward swaddled infant on low table, Solomon's wisdom"
    ),
    "The Golden Age": (
        "aerial wide shot of Jerusalem at golden hour, prosperous and green, "
        "Solomon's reign at height, peace from Dan to Beersheba"
    ),
    "Building the Temple": (
        "massive cedar logs being floated down coastal river at dawn, workers guiding them, "
        "massive dressed stones being set with no iron tools heard, "
        "cedar pillars gleaming, craftsmen working under Hiram of Tyre"
    ),
    "The Temple Dedicated": (
        "Jerusalem First Temple filled with massive luminous golden cloud of divine glory, "
        "priests prostrate on floor overwhelmed unable to stand, "
        "Solomon kneeling before the whole assembly, fire from heaven consuming the offerings"
    ),
    "The Queen of Sheba": (
        "vast caravan of camels laden with spices, gold, and precious stones crossing desert at sunset, "
        "regal Ethiopian Queen of Sheba at Solomon's court, breath taken away by his wisdom"
    ),
    "The Fall of Solomon": (
        "seven hundred foreign wives in elaborate robes in royal hall, "
        "foreign altars on Mount of Olives, aged Solomon's heart turned from God"
    ),
    "The Kingdom Divided": (
        "young Rehoboam sitting on his father Solomon's throne, listening to elders, "
        "his harsh foolish answer, ten northern tribes tearing away, "
        "kingdom split forever at Shechem"
    ),
    "Ahab and Jezebel": (
        "Ahab on northern Israelite throne in dark hall, Jezebel in elaborate Phoenician crimson beside him, "
        "Israel's most wicked king and his Phoenician queen, Baal worship spreading"
    ),
    "Elijah Appears": (
        "wild Elijah in rough haircloth mantle and leather belt "
        "walking into luxurious palace throne room, "
        "Elijah standing before Ahab, three-year drought announced"
    ),
    "The Widow's Oil": (
        "Elijah at door of impoverished widow's mudbrick house in Zarephath, "
        "drought landscape, widow's jar of oil that never ran dry, miracle of provision"
    ),
    "Mount Carmel": (
        "Elijah alone before drenched stone altar on Mount Carmel, "
        "vertical bolt of brilliant white-gold fire descending from clear sky consuming the sacrifice, "
        "450 prophets of Baal watching"
    ),
    "The Still Small Voice": (
        "Elijah collapsed in cave entrance on Mount Sinai, "
        "massive wind tearing rocks, earthquake shaking mountain, fire raging — "
        "then utter quiet stillness, dust suspended, single leaf, prophet kneeling, "
        "the still small voice"
    ),
    "Naboth's Vineyard": (
        "green vineyard on hillside next to palace estate, Naboth's inheritance, "
        "Jezebel's false letter, Naboth stoned, "
        "Elijah confronting Ahab in the vineyard"
    ),
    "The Chariot of Fire": (
        "Elijah and Elisha walking together along dusty road at dawn, "
        "flaming celestial chariot drawn by flaming horses descending between them, "
        "whirlwind rising, Elijah taken to heaven, Elisha watching with his cloak"
    ),

    # ── Chapter 8: The Fall of the Kingdoms ──────────────────────────────────
    "Ministry of Elisha": (
        "completely bald Elisha walking dusty roads through Hebrew villages, "
        "his miracles — floating axe head, Shunammite woman's son raised, "
        "healing of Syrian general Naaman in Jordan River"
    ),
    "The Prophets Rise": (
        "rough shepherd-prophet Amos sun-darkened in plain shepherd's robes "
        "walking into wealthy northern Samaria marketplace, "
        "Hosea in northern Israel, Micah in Judean hills — voices crying against injustice"
    ),
    "Fall of Samaria": (
        "massive disciplined Assyrian army marching in columns — square-cut curled black beards, "
        "conical bronze helmets, heavy iron weapons — across northern plain, "
        "siege works around Samaria's walls, northern kingdom's final days, 722 BC"
    ),
    "Isaiah in the Temple": (
        "young Isaiah in fine robes praying in Temple courtyard at dawn, "
        "then the overwhelming vision — seraphim with six wings above the throne of fire, "
        "two wings covering face, two covering feet, two flying, Isaiah prostrate: "
        "'I am a man of unclean lips'"
    ),
    "Sennacherib at Gates": (
        "imperious Assyrian Sennacherib in war camp with officers, "
        "Assyrian army with lamassu-bearing banners circling Jerusalem walls, "
        "Rabshakeh herald shouting insults at defenders on rampart, "
        "pale dawn over empty Assyrian camp — silent tents and abandoned weapons, "
        "185,000 struck down overnight"
    ),
    "Darkness of Manasseh": (
        "boy Manasseh being crowned on great throne, "
        "desecrated Temple with foreign altars, child sacrifice fires at Hinnom Valley, "
        "Judah's darkest reign"
    ),
    "The Found Book": (
        "young Josiah being crowned at age eight, "
        "high priest Hilkiah finding ancient Torah scroll in Temple, "
        "young king Josiah tearing his royal robes in grief at what he hears"
    ),
    "The Call of Jeremiah": (
        "young Jeremiah alone in small village of Anathoth at dawn, "
        "the reluctant prophet: 'I do not know how to speak, I am only a child'"
    ),
    "The Final Days": (
        "massive Babylonian army under Nebuchadnezzar marching south, "
        "Jerusalem under eighteen-month siege, Jeremiah imprisoned in courtyard of the guard, "
        "city near its end"
    ),
    "The Temple Burns": (
        "Jerusalem First Temple engulfed in orange fire and black smoke, 586 BC, "
        "Babylonian soldiers watching, weeping captives bound in chains"
    ),
    "The Weeping Prophet": (
        "aged Jeremiah sitting alone in smoking ruins of Jerusalem at dusk, "
        "head in hands, ash and broken stone all around, "
        "'Is it nothing to you, all who pass by?'"
    ),

    # ── Chapter 9: Daniel — Exile in Babylon ─────────────────────────────────
    "The Choice": (
        "line of young Hebrew nobles being inspected by Babylonian officials in palace courtyard, "
        "Daniel and friends chosen, the choice not to defile themselves with the king's food"
    ),
    "The Statue Dream": (
        "troubled Nebuchadnezzar lying awake on his bed in darkness, "
        "young Daniel before Nebuchadnezzar interpreting the dream statue "
        "of gold, silver, bronze, iron, and clay"
    ),
    "The Fiery Furnace": (
        "massive golden statue ninety feet tall on vast plain of Dura, glittering in sun, "
        "Shadrach, Meshach, and Abednego standing unbound and unharmed inside roaring furnace, "
        "luminous mysterious fourth figure walking with them, face not clearly visible"
    ),
    "Madness of the King": (
        "Nebuchadnezzar driven to madness, wild matted long hair like eagle feathers, "
        "overgrown fingernails like bird claws, eating grass in open field, "
        "ragged royal remnants visible, later restored and testifying"
    ),
    "Ezekiel's Vision": (
        "Ezekiel sitting alone beside Chebar canal under vast Babylonian sky, "
        "then the overwhelming vision — biblical cherubim, four faces, four wings, "
        "feet like burnished bronze, wheels within wheels of fire, "
        "the throne of God above them, Ezekiel prostrate"
    ),
    "The Strange Acts": (
        "Ezekiel kneeling on Babylonian street drawing Jerusalem's outline "
        "on clay tablet on ground, enacted prophecies — lying on his side, shaving his head"
    ),
    "The Glory Departs": (
        "Ezekiel transported in vision, the glory of the Lord departing the Temple, "
        "rising over the threshold, then over the east gate, then over the Mount of Olives, "
        "leaving Jerusalem behind"
    ),
    "The Dry Bones": (
        "Ezekiel standing in vast valley covered with bleached bones as far as eye can see "
        "under grey sky, breath entering the bones, tendons forming, flesh covering, "
        "an army rising to life"
    ),
    "The Writing on the Wall": (
        "vast Babylonian banqueting hall, thousand lords at long tables, "
        "disembodied human hand appearing in midair writing letters of fire "
        "on white plaster wall — no arm or body attached — Belshazzar's face going pale"
    ),
    "Fall of Babylon": (
        "legendary ancient Babylon at night — Ishtar Gate in brilliant blue glazed brick, "
        "great ziggurat of Marduk, Persian army of Cyrus entering, "
        "Babylon fallen in one night, 539 BC"
    ),
    "The Lions Den": (
        "aged Daniel kneeling in prayer in deep stone pit, "
        "magnificent ancient Persian lions surrounding him with mouths peacefully shut, "
        "shaft of light from above, Darius at top calling down at dawn"
    ),
    "Visions of Daniel": (
        "aged Daniel writing by lamplight, "
        "the Ancient of Days on blazing throne, hair like pure wool, face obscured by divine light, "
        "ten thousand times ten thousand serving him, "
        "one like a Son of Man approaching on the clouds of heaven"
    ),

    # ── Chapter 10: The Return — Ezra, Nehemiah, Esther ──────────────────────
    "The Decree of Cyrus": (
        "imposing Cyrus issuing decree in grand Persian court, "
        "royal scribe inscribing proclamation, "
        "Jewish elders weeping with joy as the news spreads"
    ),
    "The First Return": (
        "heads of Hebrew families gathering in Babylonian courtyard, scrolls open, "
        "great caravan of returning exiles setting out from Babylon toward Jerusalem, "
        "the long road home through the desert"
    ),
    "The Altar Rebuilt": (
        "Hebrew men carefully clearing rubble from ancient stone altar platform at dawn, "
        "new altar standing in Jerusalem ruins, "
        "first sacrifice and first Feast of Tabernacles in the ruins"
    ),
    "The Foundation Laid": (
        "Hebrew priests in white linen robes blowing shofars at Temple foundation stones, "
        "old men who remembered Solomon's Temple weeping, "
        "young men shouting for joy, voices mingled"
    ),
    "The Long Pause": (
        "Samaritan elders approaching Hebrew leaders with accusations and opposition, "
        "abandoned foundation lying silent for fifteen years, "
        "Jerusalem ruins and quiet Temple Mount"
    ),
    "Haggai and Zechariah": (
        "older Haggai addressing builders and farmers in public square, "
        "younger Zechariah with visions of lampstands and olive trees, "
        "the prophets renewing courage to build"
    ),
    "Second Temple Complete": (
        "completed Second Temple visibly smaller and less ornate than Solomon's but standing, "
        "old men who saw the First Temple weeping, young men shouting for joy, "
        "voices mingled, 516 BC, humble triumph"
    ),
    "For Such a Time — Esther": (
        "aerial of great Persian palace at Susa — marble columns, gold-leafed walls, gardens, "
        "beautiful Esther in elaborate Persian queen's robes "
        "approaching king's throne room, golden scepter extended toward her"
    ),
    "Ezra Returns": (
        "aged Ezra surrounded by ancient scrolls in Babylonian study, "
        "Ezra reading the Law aloud from wooden platform to thousands in Jerusalem, "
        "people weeping as they hear it"
    ),
    "Walls of Jerusalem": (
        "Nehemiah serving wine to Ahasuerus at Persian marble table, "
        "Nehemiah surveying Jerusalem's broken walls by night on donkey, torchlight and rubble"
    ),
    "The Great Reading": (
        "vast public square inside rebuilt Jerusalem walls, people gathered at dawn, "
        "Ezra on wooden platform reading Torah scroll to thousands standing, "
        "people weeping and celebrating simultaneously"
    ),
    "Malachi — Last Prophet": (
        "Hebrew priests offering blemished sickly animals on Second Temple altar, "
        "Malachi's final warning — turn back, the messenger is coming, the day of the Lord"
    ),
    "The Four Hundred Years": (
        "aerial view of Jerusalem and Temple Mount through passing centuries, "
        "Hellenistic soldiers in Greek armor, then Roman legions, "
        "four hundred years of prophetic silence, waiting"
    ),
    "Closing Transition": (
        "night road to Bethlehem, single bright star rising on horizon, "
        "young couple on donkey approaching in darkness, the long silence about to break"
    ),
}


# ══════════════════════════════════════════════════════════════════════════════
# PROMPT BUILDER — Part 12 Template
# ══════════════════════════════════════════════════════════════════════════════

# Camera angle rotation — cycles per scene so consecutive frames differ visually
_ANGLES = [
    "wide establishing shot, low horizon line",
    "medium shot, subject fills lower third",
    "close-up on hands and face, shallow depth of field",
    "low angle looking up, dramatic sky above",
    "over-the-shoulder view, subject facing away toward distant landscape",
    "aerial wide angle, vast landscape below",
    "tight medium shot, strong side lighting",
    "foreground rocks framing distant figure",
]

# Keyword → visual phrase mapping for narration-driven scene specificity
_NARRATION_VISUALS: list[tuple[str, str]] = [
    ("egypt",            "ancient Egypt, Nile delta, palm trees, mudbrick buildings"),
    ("pharaoh",          "ancient Egyptian throne room, gilded columns, linen-robed court"),
    ("nile",             "Nile river at flood, papyrus reeds, distant pyramids"),
    ("pyramid",          "massive stone pyramid under construction, workers hauling stone"),
    ("wilderness",       "barren desert wilderness, rocky terrain, sparse thorny scrub"),
    ("sinai",            "Mount Sinai rocky summit, harsh desert plateau, storm clouds"),
    ("tabernacl",        "portable wilderness tabernacle, linen courtyard fence, cloud pillar"),
    ("burning bush",     "solitary desert thornbush burning with supernatural fire"),
    ("red sea",          "vast body of water, dramatic sky, sandy shore"),
    ("jordan",           "Jordan River crossing, Levantine landscape, spring vegetation"),
    ("canaan",           "hilly Canaan landscape, ancient olive groves, stone terraces"),
    ("jerusalem",        "ancient Jerusalem on hilltop, stone walls, Kidron valley below"),
    ("temple",           "massive ancient stone temple, carved cedar pillars, bronze basin"),
    ("babylon",          "Babylonian city, massive ziggurat temple, hanging gardens"),
    ("exile",            "long column of Hebrew captives on dusty road, weeping women"),
    ("persia",           "grand Persian palace, glazed tile walls, throne room"),
    ("flood",            "dark storm-churned waters, rain sheeting down, chaos"),
    ("ark",              "colossal wooden ark structure on dry land, animals approaching"),
    ("rainbow",          "dramatic rainbow arching over flooded landscape, clearing sky"),
    ("fire",             "supernatural consuming fire, dramatic night, ash and smoke"),
    ("mountain",         "rocky mountain peak, steep trail, dramatic elevation and sky"),
    ("shepherd",         "open rolling hillside pasture, scattered sheep on green slopes"),
    ("harvest",          "ancient grain field, workers cutting wheat with bronze sickles"),
    ("battle",           "ancient battlefield, bronze-armed soldiers in formation"),
    ("king",             "ancient throne room, stone columns, gathered court"),
    ("prophet",          "lone robed figure on rocky hilltop, speaking into wind"),
    ("prayer",           "kneeling figure facing open sky, hands raised"),
    ("covenant",         "stone altar, ceremonial fire, sacred landscape, solemn gathering"),
    ("creation",         "primordial landscape taking shape, light breaking into darkness"),
    ("garden",           "lush ancient garden, towering trees, flowing river, mist"),
    ("serpent",          "ancient tree in garden, shadow, subtle coiled form"),
    ("before",           "vast empty ancient landscape, no civilization, primordial earth"),
    ("rise of",          "ancient region at its height, dramatic landscape vista"),
    ("kingdom",          "ancient hilltop city, stone walls, distant plains"),
    ("nation",           "large gathering of ancient people, desert camp, many tents"),
    ("people",           "crowd of ancient Semitic people, period dress, sun-drenched"),
    ("voice",            "lone figure in open landscape, looking upward, divine light"),
    ("word",             "ancient scribe writing on parchment by torchlight"),
    ("covenant",         "stone altar with sacred fire, two figures in solemn agreement"),
    ("sacrifice",        "stone altar on rocky hilltop, smoke rising into dawn sky"),
    ("angel",            "radiant figure in brilliant white light, rocky landscape"),
    ("dream",            "figure sleeping on rocky ground, night sky above, moon"),
    ("vision",           "ethereal light, rocky landscape, awestruck figure"),
    ("weep",             "figure bowed low in grief, dust and ash, desolate landscape"),
    ("praise",           "figures with arms raised toward dramatic sky, golden light"),
    ("wander",           "long winding trail through rocky desert, distant figure walking"),
    ("return",           "long road home, ancient city walls in distance, twilight"),
    # Broad fallback for abstract/short narration that didn't hit a specific keyword
    ("fall and rise",    "ancient walled city, dramatic sky, cycle of history"),
    ("creator",          "vast primordial landscape, divine golden light on horizon"),
    ("lord god",         "lone figure kneeling in awe, overwhelming golden divine light"),
    ("the deep",         "infinite dark primordial ocean, first light touching water"),
    ("refused",          "lone figure standing firm, desolate rocky landscape, storm"),
    ("walked away",      "long empty road disappearing to horizon, ancient landscape"),
    ("turned against",   "crowd of ancient figures in conflict, dusty ancient square"),
    # Creation / divine phenomena
    ("let there be",     "moment of creation, divine light splitting primordial darkness"),
    ("in the beginning", "void before creation, primordial darkness, first light emerging"),
    ("light",            "brilliant shaft of divine light piercing deep darkness, volumetric rays"),
    ("darkness",         "total darkness, deep black sky, single distant torch or starlight"),
    ("heavens",          "sweeping view of ancient night sky, brilliant stars, Milky Way arc"),
    ("waters",           "primordial waters, misty ancient sea, horizon vanishing in haze"),
    ("sea",              "ancient coastline, dramatic waves crashing on rocky shore"),
    ("wind",             "figure in billowing robes on rocky hilltop, dramatic stormy sky"),
    ("cloud",            "massive supernatural cloud, pillar of cloud, divine presence"),
    ("dust",             "sun-baked dust road, ancient figure walking, heat haze"),
    ("sword",            "ancient warrior raising bronze sword, battlefield"),
    ("spear",            "bronze-tipped spear, ancient warrior in formation"),
    ("wall",             "massive ancient stone city wall, gatehouse, heavy timber doors"),
    ("gate",             "ancient stone city gate, crowded marketplace, stone arch"),
    ("tent",             "ancient nomadic tent camp, goat-hair tents, desert plain"),
    ("bread",            "ancient bread baking, clay oven, simple stone house interior"),
    ("famine",           "parched cracked earth, wilted crops, gaunt figures"),
    ("plague",           "devastated ancient landscape, dark sky, suffering crowds"),
    ("cross",            "wide river crossing, figure wading, Levantine landscape"),
    ("stone",            "ancient stone altar or monument, rocky hilltop"),
    ("oil",              "ceremonial anointing, clay vessel of oil, solemn gathering"),
    ("crown",            "ancient king being crowned, stone throne room, gathered nobles"),
    ("bow",              "ancient archer with composite bow, desert landscape"),
    ("ship",             "ancient wooden vessel on stormy sea, waves crashing"),
    ("city",             "ancient walled city on hilltop, stone buildings, bustling"),
    ("born",             "stone house interior, newborn, lamplight, women attending"),
    ("died",             "mourning scene, figures in sackcloth, ancient burial preparation"),
    ("sun",              "blazing Middle Eastern sun, heat haze, ancient arid landscape"),
    ("moon",             "full moon over ancient Levantine landscape, silhouetted palm trees"),
    ("star",             "night sky filled with stars, Milky Way arc, figure looking up"),
]


def build_prompt(section_title: str, chapter_num: int, emotion: str,
                 setting: str | None = None, key_figures: list[str] | None = None,
                 narration: str = "", scene_number: int = 0) -> str:
    """Build a full image generation prompt following the Master Visual Bible template."""
    env = CHAPTER_ENVIRONMENT.get(chapter_num, "ancient biblical landscape")
    emo = EMOTION_STYLE.get(emotion, EMOTION_STYLE["solemn"])
    angle = _ANGLES[scene_number % len(_ANGLES)]

    # Primary visual: derive from narration for scene-specific variety
    visual = _visual_from_narration(narration, section_title, setting)

    # Inject exact character prompt fragments for visual consistency
    char_parts = []
    if key_figures:
        for fig in key_figures:
            if fig in CHARACTER_APPEARANCE:
                char_parts.append(CHARACTER_APPEARANCE[fig])
            else:
                char_parts.append(fig)

    char_desc = ""
    if char_parts:
        char_desc = "CHARACTERS — " + " | ".join(char_parts) + ". "

    return (
        f"{visual}, {angle}, "
        f"{char_desc}"
        f"{emo}, "
        f"{env}, "
        f"{OT_BASE_STYLE}, "
        f"{OT_INLINE_NEGATIVE}"
    )


def _visual_from_narration(narration: str, section_title: str,
                            setting: str | None) -> str:
    """Derive a scene-specific visual description from the narration text."""
    import re
    text = narration.lower().strip()

    # Title cards — use section visual for establishing context
    if len(text) < 12 or text in {"", ".", "...", "—"}:
        return SECTION_VISUAL.get(section_title, setting or "ancient Near Eastern cinematic scene")

    # Word-boundary keyword match → specific visual (longer/more specific first)
    for keyword, visual_hint in _NARRATION_VISUALS:
        if re.search(r"\b" + re.escape(keyword) + r"\b", text):
            return visual_hint

    # No keyword match: use section visual augmented with cleaned narration as context
    base = SECTION_VISUAL.get(section_title, setting or "ancient Near Eastern landscape")
    words = narration.split()
    brief = " ".join(words[:10]).rstrip(".,;:—")
    return f"{base} — {brief}"


def get_nation_context(chapter_num: int) -> str:
    """Return dominant nation style for a chapter."""
    chapter_nations = {
        4: "Egyptians", 12: "Babylonians", 13: "Babylonians",
        14: "Persians", 15: "Persians",
    }
    nation = chapter_nations.get(chapter_num, "Israelites")
    return NATION_STYLE.get(nation, "")


def get_location_context(section_title: str) -> str:
    """Return location-specific visual context if defined."""
    location_map = {
        "Adam and Eve":          "Garden_of_Eden",
        "The Fall":              "Garden_of_Eden",
        "The Burning Bush":      "Sinai",
        "The Mountain of God":   "Sinai",
        "The Ten Commandments":  "Sinai",
        "The Tabernacle":        "Tabernacle",
        "Crossing the Jordan":   "Jordan_River",
        "The Fall of Jericho":   "Jericho",
        "The Temple Dedicated":  "Solomon_Temple",
        "Building the Temple":   "Solomon_Temple",
        "Fall of Babylon":       "Babylon",
        "The Fiery Furnace":     "Babylon",
        "The Lions Den":         "Babylon",
        "For Such a Time — Esther": "Persian_Susa",
        "Second Temple Complete": "Second_Temple",
        "Closing Transition":    "Bethlehem",
        "David and Goliath":     "Valley_Elah",
        "Mount Carmel":          "Mount_Carmel",
        "The Sodom and Gomorrah": "Sodom_Gomorrah",
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
