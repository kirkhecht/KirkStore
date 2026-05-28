"""
Script parser for The Old Testament documentary.
Parses the master script into structured chapters → sections → scenes.
Outputs chapters.json used by downstream phases for richer prompts.
"""
import json
import re
from pathlib import Path

from .config import DIRS
from .utils import setup_logging, save_json

log = setup_logging("parse_script")

# ── Chapter definitions (matches the 10 PART structure of the script) ─────────
CHAPTERS = {
    1:  {"title": "The Book of Genesis — Creation to Babel",
         "period": "Before recorded history", "setting": "primordial earth, Eden, ancient Near East"},
    2:  {"title": "The Book of Genesis — The Patriarchs",
         "period": "Approx. 2000–1600 BC", "setting": "Mesopotamia, Canaan, Egypt"},
    3:  {"title": "The Book of Exodus — From Slavery to the Red Sea",
         "period": "Approx. 1500–1446 BC", "setting": "Egypt, Sinai desert"},
    4:  {"title": "The Law and the Wilderness",
         "period": "Approx. 1446–1406 BC", "setting": "Sinai, Wilderness of Paran"},
    5:  {"title": "The Promised Land — Joshua, Judges, and Ruth",
         "period": "Approx. 1406–1000 BC", "setting": "Canaan, Jordan Valley"},
    6:  {"title": "The Rise of the Kingdom — Samuel, Saul, and David",
         "period": "Approx. 1100–970 BC", "setting": "Israel, Jerusalem"},
    7:  {"title": "The Glory and the Fracture — Solomon and Elijah",
         "period": "Approx. 970–850 BC", "setting": "Jerusalem, Israel, Mount Carmel"},
    8:  {"title": "The Fall of the Kingdoms",
         "period": "Approx. 850–586 BC", "setting": "Israel, Judah, Assyria, Babylon"},
    9:  {"title": "The Exile and the Fiery Furnace",
         "period": "Approx. 605–538 BC", "setting": "Babylon, Persia"},
    10: {"title": "The Return and the Silence",
         "period": "Approx. 538–400 BC", "setting": "Persia, Jerusalem"},
}

# ── Section definitions per chapter (title, key figures, setting, emotion) ───
SECTIONS = {
    1: [
        {"title": "Cold Open",             "key_figures": [],                         "emotion": "awe",           "setting": "void, primordial darkness"},
        {"title": "The Creation",          "key_figures": ["God"],                    "emotion": "awe",           "setting": "void becoming creation"},
        {"title": "Adam and Eve",          "key_figures": ["Adam", "Eve", "serpent"], "emotion": "hopeful",       "setting": "Garden of Eden"},
        {"title": "The Fall",              "key_figures": ["Adam", "Eve"],            "emotion": "dark_and_tense","setting": "Garden of Eden, gates closing"},
        {"title": "Cain and Abel",         "key_figures": ["Cain", "Abel"],           "emotion": "dark_and_tense","setting": "ancient fields east of Eden"},
        {"title": "Corruption of Mankind", "key_figures": ["Noah"],                  "emotion": "solemn",        "setting": "ancient world, violent cities"},
        {"title": "Noah and the Flood",    "key_figures": ["Noah"],                   "emotion": "dramatic",      "setting": "wooden ark, raging flood"},
        {"title": "The Covenant with Noah","key_figures": ["Noah", "God"],            "emotion": "hopeful",       "setting": "new world after flood, rainbow"},
        {"title": "The Tower of Babel",    "key_figures": [],                         "emotion": "epic_grandeur", "setting": "plain of Shinar, ziggurat construction"},
        {"title": "Closing Transition",    "key_figures": ["Abram"],                  "emotion": "mysterious",    "setting": "city of Ur, ancient Mesopotamia"},
    ],
    2: [
        {"title": "Cold Open",             "key_figures": ["Abram"],                  "emotion": "mysterious",    "setting": "ancient Ur, Euphrates River"},
        {"title": "The Calling of Abraham","key_figures": ["Abram", "Sarai"],         "emotion": "hopeful",       "setting": "Ur, desert journey, Canaan"},
        {"title": "The Covenant",          "key_figures": ["Abraham"],                "emotion": "awe",           "setting": "starlit desert, night sky over Canaan"},
        {"title": "The Three Visitors",    "key_figures": ["Abraham", "Sarah"],       "emotion": "mysterious",    "setting": "tent under oak trees at Mamre"},
        {"title": "Sodom and Gomorrah",    "key_figures": ["Lot", "Abraham"],         "emotion": "dark_and_tense","setting": "ancient cities, fire from sky"},
        {"title": "The Birth of Isaac",    "key_figures": ["Sarah", "Isaac"],         "emotion": "hopeful",       "setting": "tent camp in Canaan"},
        {"title": "The Binding of Isaac",  "key_figures": ["Abraham", "Isaac"],       "emotion": "solemn",        "setting": "Mount Moriah, altar on hilltop"},
        {"title": "Sarah and Rebekah",     "key_figures": ["Isaac", "Rebekah"],       "emotion": "hopeful",       "setting": "well in ancient Mesopotamia"},
        {"title": "Jacob and Esau",        "key_figures": ["Jacob", "Esau"],          "emotion": "dramatic",      "setting": "Isaac's tent camp, Canaan"},
        {"title": "Jacob's Ladder",        "key_figures": ["Jacob"],                  "emotion": "awe",           "setting": "open desert, stars overhead, bethel"},
        {"title": "Jacob Leah Rachel",     "key_figures": ["Jacob", "Rachel", "Leah"],"emotion": "dramatic",      "setting": "Haran, uncle Laban's household"},
        {"title": "Jacob Wrestles God",    "key_figures": ["Jacob"],                  "emotion": "dramatic",      "setting": "riverbank at Jabbok at night"},
        {"title": "The Reconciliation",    "key_figures": ["Jacob", "Esau"],          "emotion": "hopeful",       "setting": "open land of Canaan"},
        {"title": "Joseph and His Brothers","key_figures": ["Joseph"],                "emotion": "dark_and_tense","setting": "Canaan, empty pit, trade caravan"},
        {"title": "Joseph in Egypt",       "key_figures": ["Joseph", "Potiphar"],     "emotion": "dramatic",      "setting": "Egyptian household, Egyptian prison"},
        {"title": "Dreams of Pharaoh",     "key_figures": ["Joseph", "Pharaoh"],      "emotion": "epic_grandeur", "setting": "throne room of Egypt, Nile"},
        {"title": "The Brothers Return",   "key_figures": ["Joseph", "Benjamin"],     "emotion": "dramatic",      "setting": "grain stores of Egypt"},
        {"title": "Jacob Comes to Egypt",  "key_figures": ["Jacob", "Joseph"],        "emotion": "hopeful",       "setting": "land of Goshen, Egypt"},
        {"title": "Closing Transition",    "key_figures": [],                         "emotion": "solemn",        "setting": "Egypt, sarcophagus of Joseph"},
    ],
    3: [
        {"title": "Cold Open",             "key_figures": [],                         "emotion": "dark_and_tense","setting": "Egyptian brick pits, slave labor"},
        {"title": "The Birth of Moses",    "key_figures": ["Moses", "Jochebed"],      "emotion": "hopeful",       "setting": "Nile River, Egyptian palace"},
        {"title": "Moses Flees Egypt",     "key_figures": ["Moses"],                  "emotion": "dramatic",      "setting": "Egyptian streets, Midian desert"},
        {"title": "The Burning Bush",      "key_figures": ["Moses", "God"],           "emotion": "awe",           "setting": "Mount Horeb, burning bush in desert"},
        {"title": "Moses Returns",         "key_figures": ["Moses", "Aaron"],         "emotion": "dramatic",      "setting": "Egyptian desert, Pharaoh's palace"},
        {"title": "Let My People Go",      "key_figures": ["Moses", "Pharaoh"],       "emotion": "dark_and_tense","setting": "throne room of Egypt"},
        {"title": "The Ten Plagues",       "key_figures": ["Moses", "Pharaoh"],       "emotion": "dark_and_tense","setting": "Egypt, Nile, cities, fields"},
        {"title": "The Passover",          "key_figures": ["Moses"],                  "emotion": "solemn",        "setting": "Hebrew homes at night, Egypt"},
        {"title": "The Exodus",            "key_figures": ["Moses", "Israel"],        "emotion": "triumphant",    "setting": "Egyptian cities, desert road"},
        {"title": "The Red Sea",           "key_figures": ["Moses", "Pharaoh"],       "emotion": "dramatic",      "setting": "shores of Red Sea, Egyptian chariots"},
        {"title": "The Song of Moses",     "key_figures": ["Moses", "Miriam"],        "emotion": "triumphant",    "setting": "eastern shore of Red Sea"},
        {"title": "Closing Transition",    "key_figures": [],                         "emotion": "mysterious",    "setting": "Sinai wilderness, distant mountain"},
    ],
    4: [
        {"title": "Cold Open",             "key_figures": [],                         "emotion": "awe",           "setting": "Sinai desert, Mount Sinai"},
        {"title": "The Mountain of God",   "key_figures": ["Moses", "Israel"],        "emotion": "awe",           "setting": "Mount Sinai, thunder and lightning"},
        {"title": "The Ten Commandments",  "key_figures": ["Moses", "God"],           "emotion": "solemn",        "setting": "Mount Sinai, smoking summit"},
        {"title": "The Covenant in Blood", "key_figures": ["Moses", "Aaron"],         "emotion": "solemn",        "setting": "altar at base of Sinai"},
        {"title": "The Golden Calf",       "key_figures": ["Aaron", "Moses"],         "emotion": "dark_and_tense","setting": "Israelite camp, golden idol"},
        {"title": "The Radiant Face",      "key_figures": ["Moses", "God"],           "emotion": "awe",           "setting": "Mount Sinai, rock cleft"},
        {"title": "The Tabernacle",        "key_figures": ["Moses", "Bezalel"],       "emotion": "solemn",        "setting": "wilderness camp, portable temple"},
        {"title": "The Law",               "key_figures": ["Moses"],                  "emotion": "solemn",        "setting": "Tabernacle in wilderness"},
        {"title": "The Twelve Spies",      "key_figures": ["Caleb", "Joshua"],        "emotion": "dramatic",      "setting": "Kadesh-Barnea, Canaan borderlands"},
        {"title": "Forty Years",           "key_figures": ["Moses"],                  "emotion": "solemn",        "setting": "Sinai wilderness, desert wandering"},
        {"title": "Death of Miriam Aaron", "key_figures": ["Moses"],                  "emotion": "solemn",        "setting": "Kadesh desert, Mount Hor"},
        {"title": "Balak and Balaam",      "key_figures": ["Balaam"],                 "emotion": "mysterious",    "setting": "Moabite highlands overlooking Israel"},
        {"title": "The Farewell of Moses", "key_figures": ["Moses"],                  "emotion": "solemn",        "setting": "plains of Moab, Jordan River valley"},
        {"title": "The Death of Moses",    "key_figures": ["Moses"],                  "emotion": "solemn",        "setting": "Mount Nebo summit, Promised Land vista"},
        {"title": "Closing Transition",    "key_figures": ["Joshua"],                 "emotion": "hopeful",       "setting": "plains of Moab, Jordan River"},
    ],
    5: [
        {"title": "Cold Open",             "key_figures": ["Joshua"],                 "emotion": "epic_grandeur", "setting": "plains of Moab, Canaan horizon"},
        {"title": "Crossing the Jordan",   "key_figures": ["Joshua", "Ark"],          "emotion": "awe",           "setting": "Jordan River, flooded waters parting"},
        {"title": "The Fall of Jericho",   "key_figures": ["Joshua", "Rahab"],        "emotion": "dramatic",      "setting": "Jericho city walls, trumpet blast"},
        {"title": "The Conquest",          "key_figures": ["Joshua"],                 "emotion": "triumphant",    "setting": "Canaanite cities, battle scenes"},
        {"title": "Dividing the Land",     "key_figures": ["Joshua"],                 "emotion": "hopeful",       "setting": "hill country of Canaan"},
        {"title": "Choose This Day",       "key_figures": ["Joshua"],                 "emotion": "solemn",        "setting": "Shechem, assembly of Israel"},
        {"title": "The Cycle of Judges",   "key_figures": [],                         "emotion": "dark_and_tense","setting": "Canaan, idol worship, oppression"},
        {"title": "Deborah and Barak",     "key_figures": ["Deborah", "Jael"],        "emotion": "triumphant",    "setting": "palm tree, Kishon Valley battle"},
        {"title": "Gideon",                "key_figures": ["Gideon"],                 "emotion": "dramatic",      "setting": "wine press in hiding, Midian camp at night"},
        {"title": "Samson",                "key_figures": ["Samson", "Delilah"],      "emotion": "dark_and_tense","setting": "Philistine temple, Gaza, valley of Sorek"},
        {"title": "Dark End of Judges",    "key_figures": [],                         "emotion": "dark_and_tense","setting": "tribal Israel, chaos and violence"},
        {"title": "The Book of Ruth",      "key_figures": ["Ruth", "Naomi", "Boaz"], "emotion": "hopeful",       "setting": "Bethlehem grain fields, threshing floor"},
        {"title": "Closing Transition",    "key_figures": ["Samuel"],                 "emotion": "hopeful",       "setting": "Shiloh, Tabernacle at dusk"},
    ],
    6: [
        {"title": "Cold Open",             "key_figures": ["Samuel"],                 "emotion": "mysterious",    "setting": "hill country of Ramah, Tabernacle"},
        {"title": "Hannah and Samuel",     "key_figures": ["Hannah", "Eli"],          "emotion": "solemn",        "setting": "Shiloh Tabernacle"},
        {"title": "Samuel Called",         "key_figures": ["Samuel", "Eli"],          "emotion": "mysterious",    "setting": "Tabernacle at night, lamplight"},
        {"title": "The Ark Captured",      "key_figures": ["Eli"],                    "emotion": "dark_and_tense","setting": "battlefield, Philistine camp, Shiloh"},
        {"title": "Give Us a King",        "key_figures": ["Samuel"],                 "emotion": "solemn",        "setting": "gate of an Israelite city"},
        {"title": "Saul Anointed",         "key_figures": ["Saul", "Samuel"],         "emotion": "epic_grandeur", "setting": "Samuel's town, Israelite assembly"},
        {"title": "The Fall of Saul",      "key_figures": ["Saul", "Samuel"],         "emotion": "dark_and_tense","setting": "Gilgal altar, battlefield"},
        {"title": "The Boy in Bethlehem",  "key_figures": ["David", "Samuel"],        "emotion": "hopeful",       "setting": "Bethlehem hills, Jesse's household"},
        {"title": "David and Goliath",     "key_figures": ["David", "Goliath"],       "emotion": "dramatic",      "setting": "Valley of Elah, two opposing armies"},
        {"title": "Jonathan and David",    "key_figures": ["Jonathan", "David"],      "emotion": "hopeful",       "setting": "Saul's court, fields of Israel"},
        {"title": "The Wilderness Years",  "key_figures": ["David"],                  "emotion": "dark_and_tense","setting": "caves of Engedi, desert strongholds"},
        {"title": "Death of Samuel",       "key_figures": ["Samuel"],                 "emotion": "solemn",        "setting": "Ramah, mourning Israel"},
        {"title": "The Witch of Endor",    "key_figures": ["Saul"],                   "emotion": "dark_and_tense","setting": "dark hut at Endor, ghost of Samuel"},
        {"title": "Mount Gilboa",          "key_figures": ["Saul", "Jonathan"],       "emotion": "dark_and_tense","setting": "Mount Gilboa battle, Philistine archers"},
        {"title": "David Crowned King",    "key_figures": ["David"],                  "emotion": "triumphant",    "setting": "Hebron, Jerusalem city"},
        {"title": "The Ark Comes Home",    "key_figures": ["David"],                  "emotion": "triumphant",    "setting": "Jerusalem streets, dancing before the Ark"},
        {"title": "The Covenant with David","key_figures": ["David", "Nathan"],       "emotion": "solemn",        "setting": "Jerusalem palace"},
        {"title": "David and Bathsheba",   "key_figures": ["David", "Bathsheba"],     "emotion": "dark_and_tense","setting": "Jerusalem palace roof at night"},
        {"title": "Nathan and the Lamb",   "key_figures": ["Nathan", "David"],        "emotion": "dramatic",      "setting": "Jerusalem palace throne room"},
        {"title": "Absalom's Rebellion",   "key_figures": ["Absalom", "David"],       "emotion": "dark_and_tense","setting": "Jerusalem streets, forest battle"},
        {"title": "The Old King",          "key_figures": ["David", "Solomon"],       "emotion": "solemn",        "setting": "Jerusalem palace, deathbed"},
        {"title": "Closing Transition",    "key_figures": ["Solomon"],                "emotion": "hopeful",       "setting": "Jerusalem, Temple Mount"},
    ],
    7: [
        {"title": "Cold Open",             "key_figures": ["Solomon"],                "emotion": "epic_grandeur", "setting": "Jerusalem palace, new kingdom"},
        {"title": "The Dream at Gibeon",   "key_figures": ["Solomon"],                "emotion": "awe",           "setting": "Gibeon high place, sleeping by altar"},
        {"title": "The Two Mothers",       "key_figures": ["Solomon"],                "emotion": "dramatic",      "setting": "Solomon's throne room"},
        {"title": "The Golden Age",        "key_figures": ["Solomon"],                "emotion": "epic_grandeur", "setting": "Jerusalem at height of glory"},
        {"title": "Building the Temple",   "key_figures": ["Solomon"],                "emotion": "solemn",        "setting": "Temple Mount construction, cedar logs"},
        {"title": "The Temple Dedicated",  "key_figures": ["Solomon", "God"],         "emotion": "awe",           "setting": "Jerusalem Temple, cloud of glory"},
        {"title": "The Queen of Sheba",    "key_figures": ["Solomon", "Sheba Queen"],"emotion": "epic_grandeur", "setting": "Jerusalem palace, royal reception"},
        {"title": "The Fall of Solomon",   "key_figures": ["Solomon"],                "emotion": "dark_and_tense","setting": "Jerusalem, foreign altars on Mount of Olives"},
        {"title": "The Kingdom Divided",   "key_figures": ["Rehoboam", "Jeroboam"],  "emotion": "dark_and_tense","setting": "Shechem assembly, kingdom splitting"},
        {"title": "Ahab and Jezebel",      "key_figures": ["Ahab", "Jezebel"],       "emotion": "dark_and_tense","setting": "Samaria, Baal temple"},
        {"title": "Elijah Appears",        "key_figures": ["Elijah"],                 "emotion": "dramatic",      "setting": "Ahab's palace, drought landscape"},
        {"title": "The Widow's Oil",       "key_figures": ["Elijah"],                 "emotion": "hopeful",       "setting": "Zarephath, widow's house in drought"},
        {"title": "Mount Carmel",          "key_figures": ["Elijah", "Baal prophets"],"emotion": "dramatic",      "setting": "Mount Carmel, fire from heaven"},
        {"title": "The Still Small Voice", "key_figures": ["Elijah"],                 "emotion": "solemn",        "setting": "cave at Mount Sinai/Horeb"},
        {"title": "Naboth's Vineyard",     "key_figures": ["Ahab", "Jezebel", "Naboth"],"emotion": "dark_and_tense","setting": "Jezreel, vineyard, Naboth's trial"},
        {"title": "The Chariot of Fire",   "key_figures": ["Elijah", "Elisha"],       "emotion": "awe",           "setting": "Jordan River, chariot ascending"},
        {"title": "Closing Transition",    "key_figures": ["Elisha"],                 "emotion": "dramatic",      "setting": "Jordan River, Elijah's mantle"},
    ],
    8: [
        {"title": "Cold Open",             "key_figures": ["Elisha"],                 "emotion": "dramatic",      "setting": "Jordan riverbank, prophets watching"},
        {"title": "Ministry of Elisha",    "key_figures": ["Elisha"],                 "emotion": "hopeful",       "setting": "various northern kingdom locations"},
        {"title": "The Prophets Rise",     "key_figures": ["Amos", "Hosea", "Micah"],"emotion": "solemn",        "setting": "Samaria markets, Judean hills"},
        {"title": "Fall of Samaria",       "key_figures": [],                         "emotion": "dark_and_tense","setting": "Samaria under Assyrian siege"},
        {"title": "Isaiah in the Temple",  "key_figures": ["Isaiah"],                 "emotion": "awe",           "setting": "Jerusalem Temple, vision of God's throne"},
        {"title": "Sennacherib at Gates",  "key_figures": ["Hezekiah", "Isaiah"],     "emotion": "dark_and_tense","setting": "Jerusalem walls, Assyrian army camp"},
        {"title": "Darkness of Manasseh",  "key_figures": ["Manasseh"],               "emotion": "dark_and_tense","setting": "Jerusalem, desecrated Temple"},
        {"title": "The Found Book",        "key_figures": ["Josiah"],                 "emotion": "dramatic",      "setting": "Temple of Jerusalem, scroll discovery"},
        {"title": "The Call of Jeremiah",  "key_figures": ["Jeremiah"],               "emotion": "solemn",        "setting": "village of Anathoth, hills of Judah"},
        {"title": "The Final Days",        "key_figures": ["Jeremiah", "Zedekiah"],   "emotion": "dark_and_tense","setting": "Jerusalem under siege, city walls"},
        {"title": "The Temple Burns",      "key_figures": [],                         "emotion": "dark_and_tense","setting": "Jerusalem Temple engulfed in fire"},
        {"title": "The Weeping Prophet",   "key_figures": ["Jeremiah"],               "emotion": "solemn",        "setting": "smoking ruins of Jerusalem"},
        {"title": "Closing Transition",    "key_figures": ["Daniel", "Ezekiel"],      "emotion": "mysterious",    "setting": "road to Babylon, captive procession"},
    ],
    9: [
        {"title": "Cold Open",             "key_figures": [],                         "emotion": "epic_grandeur", "setting": "road to Babylon, distant ziggurat"},
        {"title": "The Choice",            "key_figures": ["Daniel"],                 "emotion": "solemn",        "setting": "Babylon palace training hall"},
        {"title": "The Statue Dream",      "key_figures": ["Daniel", "Nebuchadnezzar"],"emotion": "awe",          "setting": "Babylon throne room, night vision"},
        {"title": "The Fiery Furnace",     "key_figures": ["Shadrach", "Meshach", "Abednego"],"emotion": "dramatic","setting": "plain of Dura, massive golden statue, furnace"},
        {"title": "Madness of the King",   "key_figures": ["Nebuchadnezzar"],         "emotion": "dark_and_tense","setting": "Babylon palace rooftop, fields"},
        {"title": "Ezekiel's Vision",      "key_figures": ["Ezekiel"],                "emotion": "awe",           "setting": "Chebar River bank, heavenly vision"},
        {"title": "The Strange Acts",      "key_figures": ["Ezekiel"],                "emotion": "solemn",        "setting": "exile community, Ezekiel's house"},
        {"title": "The Glory Departs",     "key_figures": ["Ezekiel"],                "emotion": "dark_and_tense","setting": "Temple vision, Mount of Olives"},
        {"title": "The Dry Bones",         "key_figures": ["Ezekiel"],                "emotion": "hopeful",       "setting": "valley of dry bones, vision of restoration"},
        {"title": "The Writing on the Wall","key_figures": ["Belshazzar", "Daniel"],  "emotion": "dramatic",      "setting": "Babylon banquet hall, ghostly hand writing"},
        {"title": "Fall of Babylon",       "key_figures": ["Cyrus"],                  "emotion": "epic_grandeur", "setting": "Babylon city, Persian army entering"},
        {"title": "The Lions Den",         "key_figures": ["Daniel"],                 "emotion": "dramatic",      "setting": "Persian court, deep stone lions den"},
        {"title": "Visions of Daniel",     "key_figures": ["Daniel"],                 "emotion": "awe",           "setting": "throne room of heaven, heavenly court"},
        {"title": "Closing Transition",    "key_figures": [],                         "emotion": "hopeful",       "setting": "streets of Babylon, rumour of return"},
    ],
    10: [
        {"title": "Cold Open",             "key_figures": ["Cyrus"],                  "emotion": "hopeful",       "setting": "Babylon, Persian palace"},
        {"title": "The Decree of Cyrus",   "key_figures": ["Cyrus"],                  "emotion": "hopeful",       "setting": "Persian palace, proclamation in streets"},
        {"title": "The First Return",      "key_figures": ["Zerubbabel"],             "emotion": "hopeful",       "setting": "road from Babylon to Jerusalem"},
        {"title": "The Altar Rebuilt",     "key_figures": ["Zerubbabel"],             "emotion": "solemn",        "setting": "ruins of Jerusalem, new altar"},
        {"title": "The Foundation Laid",   "key_figures": ["Zerubbabel"],             "emotion": "hopeful",       "setting": "Temple Mount, foundation stones"},
        {"title": "The Long Pause",        "key_figures": [],                         "emotion": "solemn",        "setting": "Jerusalem ruins, abandoned foundation"},
        {"title": "Haggai and Zechariah",  "key_figures": ["Haggai", "Zechariah"],   "emotion": "hopeful",       "setting": "Jerusalem, prophets in rebuilt community"},
        {"title": "Second Temple Complete","key_figures": ["Zerubbabel"],             "emotion": "solemn",        "setting": "second Temple dedication, Jerusalem"},
        {"title": "For Such a Time — Esther","key_figures": ["Esther", "Mordecai"],  "emotion": "dramatic",      "setting": "Susa palace, Persian court"},
        {"title": "Ezra Returns",          "key_figures": ["Ezra"],                   "emotion": "solemn",        "setting": "Jerusalem, people gathered before the Law"},
        {"title": "Walls of Jerusalem",    "key_figures": ["Nehemiah"],               "emotion": "dramatic",      "setting": "Jerusalem rubble, wall construction"},
        {"title": "The Great Reading",     "key_figures": ["Ezra"],                   "emotion": "solemn",        "setting": "Jerusalem square, people listening to the Law"},
        {"title": "Malachi — Last Prophet","key_figures": ["Malachi"],                "emotion": "solemn",        "setting": "Jerusalem, people at Temple"},
        {"title": "The Four Hundred Years","key_figures": [],                         "emotion": "mysterious",    "setting": "Hellenistic Jerusalem, silent heavens"},
        {"title": "Closing Transition",    "key_figures": [],                         "emotion": "hopeful",       "setting": "Bethlehem road, night sky, star rising"},
    ],
}


def build_chapter_json() -> list[dict]:
    chapters = []
    for num, meta in CHAPTERS.items():
        sections = SECTIONS.get(num, [])
        chapters.append({
            "chapter_number":   num,
            "chapter_title":    meta["title"],
            "period":           meta["period"],
            "setting":          meta["setting"],
            "filename":         f"{num:02d}_{_slug(meta['title'])}.mp3",
            "sections":         sections,
            "section_count":    len(sections),
        })
    return chapters


def _slug(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s[:50]


def run(output_path: Path | None = None) -> list[dict]:
    chapters = build_chapter_json()
    out = output_path or (DIRS["production"] / "chapters.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    save_json(chapters, out)
    log.info("chapters.json written: %d chapters, %d total sections",
             len(chapters),
             sum(len(c["sections"]) for c in chapters))
    return chapters
