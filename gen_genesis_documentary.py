#!/usr/bin/env python3
"""
THE OLD TESTAMENT: A Cinematic Documentary
Genesis Patriarchs — Documentary Assembly

Pipeline:
  1. ElevenLabs TTS voiceover per scene (David voice)
  2. FFmpeg title card clips (black screen with white text, 5s each)
  3. Ken Burns motion video clip per image
  4. Concat into final Genesis Patriarchs MP4

Output: project/documentary/genesis_patriarchs.mp4
        project/documentary/genesis_patriarchs_720p.mp4

Story sections (with title cards):
  01  THE CALLING OF ABRAM         c. 2000 BC   (scenes   1-18)
  02  THE COVENANT WITH GOD                      (scenes  19-34)
  03  THE THREE VISITORS                         (scenes  35-46)
  04  SODOM AND GOMORRAH           c. 1900 BC   (scenes  47-64)
  05  THE BIRTH OF ISAAC                         (scenes  65-76)
  06  THE BINDING OF ISAAC                       (scenes  77-94)
  07  REBEKAH — WIFE OF ISAAC                    (scenes  95-106)
  08  JACOB AND ESAU                             (scenes 107-126)
  09  JACOBS DREAM AT BETHEL                     (scenes 127-136)
  10  JACOB — LEAH AND RACHEL                    (scenes 137-150)
  11  JACOB WRESTLES WITH GOD                    (scenes 151-162)
  12  JOSEPH AND HIS BROTHERS      c. 1900 BC   (scenes 163-180)
  13  JOSEPH IN EGYPT                            (scenes 181-196)
  14  PHARAOHS DREAMS                            (scenes 197-218)
"""

import os, sys, subprocess, requests, argparse, time, tempfile
from pathlib import Path

IMG_DIR    = Path("project/stories/genesis_patriarchs")
AUDIO_DIR  = Path("project/documentary/genesis/audio")
CLIPS_DIR  = Path("project/documentary/genesis/clips")
TCARDS_DIR = Path("project/documentary/genesis/title_cards")
OUTPUT_DIR = Path("project/documentary")
FINAL_OUT  = OUTPUT_DIR / "genesis_patriarchs.mp4"

for d in [AUDIO_DIR, CLIPS_DIR, TCARDS_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

VOICE_ID    = "kmjgtnoB3DMXA9wZpudu"  # Brady J — Gripping Suspense
EL_MODEL    = "eleven_multilingual_v2"
SILENCE_PAD = 0.45

FPS  = 25
W, H = 1920, 1080
FADE = 0.25

FONT_FILE = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

MOTION = {
    "zoom_in":        "z='min(zoom+0.0007,1.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    "zoom_out":       "z='if(eq(on,1),1.3,max(1.001,zoom-0.0007))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    "pan_right":      "z='1.18':x='min(iw*(1-1/zoom),0+on*0.5)':y='ih/2-(ih/zoom/2)'",
    "pan_left":       "z='1.18':x='max(0,iw*(1-1/zoom)-on*0.5)':y='ih/2-(ih/zoom/2)'",
    "pan_up":         "z='1.18':x='iw/2-(iw/zoom/2)':y='max(0,ih*(1-1/zoom)-on*0.35)'",
    "pan_down":       "z='1.18':x='iw/2-(iw/zoom/2)':y='min(ih*(1-1/zoom),0+on*0.35)'",
    "drift_right_up": "z='1.2':x='min(iw*(1-1/zoom),0+on*0.4)':y='max(0,ih*(1-1/zoom)-on*0.25)'",
    "zoom_in_up":     "z='min(zoom+0.0007,1.3)':x='iw/2-(iw/zoom/2)':y='max(0,ih/2-(ih/zoom/2)-on*0.15)'",
    "zoom_out_right": "z='if(eq(on,1),1.3,max(1.001,zoom-0.0006))':x='min(iw*(1-1/zoom),iw/2-(iw/zoom/2)+on*0.3)':y='ih/2-(ih/zoom/2)'",
}

# ── Content list ───────────────────────────────────────────────────────────────
# ("title", story_num, "TITLE TEXT", "subtitle text")
# ("scene", scene_num, "filename.jpg", "narration", "motion")

CONTENT = [

    ("title", 1, "THE CALLING OF ABRAM", "c. 2000 BC"),
    ("scene",  1, "001_abram_in_ur.jpg",            "His name was Abram.",                                                                                                   "zoom_in"),
    ("scene",  2, "002_city_of_ur.jpg",              "He lived in Ur of the Chaldeans — one of the greatest cities in the ancient world.",                                    "zoom_out"),
    ("scene",  3, "003_temples_and_trade.jpg",        "A city of ziggurats and merchant roads. Of temples and trade.",                                                        "pan_right"),
    ("scene",  4, "004_god_comes_to_abram.jpg",       "But God came to him there.",                                                                                           "zoom_in"),
    ("scene",  5, "005_the_call_go.jpg",              "Go. Leave your country, your people, your father's household.",                                                        "zoom_out"),
    ("scene",  6, "006_land_i_will_show.jpg",         "Go to the land I will show you.",                                                                                      "pan_right"),
    ("scene",  7, "007_great_nation.jpg",             "I will make you into a great nation.",                                                                                 "zoom_in"),
    ("scene",  8, "008_bless_you.jpg",                "I will bless you. I will make your name great.",                                                                       "zoom_out"),
    ("scene",  9, "009_blessed_through_you.jpg",      "And all peoples on earth will be blessed through you.",                                                               "zoom_in"),
    ("scene", 10, "010_abram_did_not_know.jpg",       "Abram did not know where he was going.",                                                                               "pan_right"),
    ("scene", 11, "011_but_he_went.jpg",              "But he went.",                                                                                                         "zoom_out"),
    ("scene", 12, "012_sarai_lot_flocks.jpg",         "He packed everything — his wife Sarai, his nephew Lot, his flocks and herds and servants.",                           "zoom_in"),
    ("scene", 13, "013_they_set_out.jpg",             "And they set out.",                                                                                                    "zoom_out"),
    ("scene", 14, "014_across_desert.jpg",            "Across the desert. Across the rivers. Toward a land they had never seen.",                                            "pan_right"),
    ("scene", 15, "015_came_to_canaan.jpg",           "At last, they came to the land of Canaan.",                                                                           "zoom_in"),
    ("scene", 16, "016_to_your_offspring.jpg",        "God appeared to Abram there. 'To your offspring I will give this land.'",                                             "zoom_out"),
    ("scene", 17, "017_abram_builds_altar.jpg",       "Abram built an altar. His first act in the promised land was worship.",                                               "zoom_in"),
    ("scene", 18, "018_left_everything.jpg",          "He had left everything. He would wait to receive everything.",                                                        "pan_right"),

    ("title", 2, "THE COVENANT WITH GOD", ""),
    ("scene", 19, "019_years_passed.jpg",             "Years passed. Abram grew old. The promise seemed impossible.",                                                         "zoom_out"),
    ("scene", 20, "020_sarai_barren.jpg",             "[sighs] He had no children. Sarai was barren.",                                                                               "zoom_in"),
    ("scene", 21, "021_do_not_be_afraid.jpg",         "But God came to Abram in a vision. 'Do not be afraid. I am your shield.'",                                           "zoom_out"),
    ("scene", 22, "022_what_can_you_give.jpg",        "Abram asked — what can you give me, since I have no child?",                                                          "pan_right"),
    ("scene", 23, "023_count_the_stars.jpg",          "God took him outside and said — look at the sky. Count the stars.",                                                   "zoom_in"),
    ("scene", 24, "024_so_shall_your_offspring.jpg",  "So shall your offspring be.",                                                                                         "zoom_out"),
    ("scene", 25, "025_abram_believed.jpg",           "Abram believed. And God counted it to him as righteousness.",                                                         "zoom_in"),
    ("scene", 26, "026_god_made_covenant.jpg",        "Then God made a covenant — a binding promise.",                                                                       "pan_right"),
    ("scene", 27, "027_animals_cut.jpg",              "He had Abram cut animals in half and lay them in two rows.",                                                          "zoom_out"),
    ("scene", 28, "028_sun_goes_down.jpg",            "And as the sun went down, Abram fell into a deep, terrifying sleep.",                                                 "zoom_in"),
    ("scene", 29, "029_smoking_firepot.jpg",          "A smoking firepot. A blazing torch. Moving between the pieces.",                                                      "zoom_out"),
    ("scene", 30, "030_god_passing_through.jpg",      "God alone passing through — taking the full weight of the promise onto Himself.",                                     "pan_right"),
    ("scene", 31, "031_ninety_nine_years.jpg",        "When Abram was ninety-nine years old, God appeared again.",                                                           "zoom_in"),
    ("scene", 32, "032_walk_before_me.jpg",           "I am God Almighty. Walk before me and be blameless.",                                                                 "zoom_out"),
    ("scene", 33, "033_name_abraham.jpg",             "Your name will no longer be Abram. It will be Abraham — father of many nations.",                                     "zoom_in"),
    ("scene", 34, "034_sarah_mother_of_nations.jpg",  "And Sarai — she will be called Sarah. She will become the mother of nations.",                                        "pan_right"),

    ("title", 3, "THE THREE VISITORS", ""),
    ("scene", 35, "035_tent_at_mamre.jpg",            "One day, Abraham was sitting at the entrance of his tent in the heat of the day.",                                    "zoom_out"),
    ("scene", 36, "036_three_strangers.jpg",           "He looked up — and three strangers were standing before him.",                                                        "zoom_in"),
    ("scene", 37, "037_ran_to_meet_them.jpg",          "He ran to meet them. He bowed low. He begged them to rest and eat.",                                                  "zoom_out"),
    ("scene", 38, "038_curds_and_milk.jpg",            "He killed a calf. He brought curds and milk. He stood beneath a tree while they ate.",                               "pan_right"),
    ("scene", 39, "039_where_is_sarah.jpg",            "Then one of them asked — where is Sarah your wife?",                                                                  "zoom_in"),
    ("scene", 40, "040_she_is_in_the_tent.jpg",        "She is there. In the tent.",                                                                                          "zoom_out"),
    ("scene", 41, "041_return_next_year.jpg",           "'I will return to you at this time next year. And your wife Sarah will have a son.'",                               "zoom_in"),
    ("scene", 42, "042_sarah_listening.jpg",           "Sarah was listening at the tent entrance behind them.",                                                               "pan_right"),
    ("scene", 43, "043_sarah_ninety.jpg",              "She was ninety years old.",                                                                                           "zoom_out"),
    ("scene", 44, "044_sarah_laughed.jpg",             "She laughed to herself. [laughs]",                                                                                             "zoom_in"),
    ("scene", 45, "045_anything_too_hard.jpg",         "The Lord asked — why did Sarah laugh? Is anything too hard for the Lord?",                                           "zoom_out"),
    ("scene", 46, "046_yes_you_did.jpg",               "Sarah said, 'I did not laugh.' But the Lord said — 'Yes, you did.'",                                                "pan_right"),

    ("title", 4, "SODOM AND GOMORRAH", "c. 1900 BC"),
    ("scene", 47, "047_men_looked_toward_sodom.jpg",   "The men rose and looked toward Sodom.",                                                                              "zoom_in"),
    ("scene", 48, "048_abraham_walked_with_them.jpg",  "Abraham walked with them part of the way.",                                                                          "zoom_out"),
    ("scene", 49, "049_shall_i_hide.jpg",              "And the Lord said — shall I hide from Abraham what I am about to do?",                                               "zoom_in"),
    ("scene", 50, "050_outcry_against_sodom.jpg",      "The outcry against Sodom and Gomorrah was great. Their sin was very grave.",                                         "pan_right"),
    ("scene", 51, "051_will_you_sweep_away.jpg",       "Abraham stood before God and asked — will you sweep away the righteous with the wicked?",                            "zoom_out"),
    ("scene", 52, "052_fifty_righteous.jpg",           "What if there are fifty righteous in the city?",                                                                     "zoom_in"),
    ("scene", 53, "053_god_will_spare.jpg",            "God said — if I find fifty, I will spare the whole place.",                                                          "zoom_out"),
    ("scene", 54, "054_bargaining.jpg",                "Abraham bargained — forty-five? Forty? Thirty? Twenty? Ten?",                                                        "pan_right"),
    ("scene", 55, "055_ten_righteous.jpg",             "God agreed — for the sake of ten, I will not destroy it.",                                                           "zoom_in"),
    ("scene", 56, "056_angels_at_sodom.jpg",           "Two angels arrived in Sodom at evening. Lot was sitting in the gateway.",                                            "zoom_out"),
    ("scene", 57, "057_lot_begged.jpg",                "He begged them to come to his house. They came in. He made them a feast.",                                           "zoom_in"),
    ("scene", 58, "058_men_surrounded.jpg",            "But before they could sleep, the men of the city surrounded Lot's house.",                                           "pan_right"),
    ("scene", 59, "059_angels_struck_blind.jpg",       "The angels struck the men outside with blindness.",                                                                  "zoom_out"),
    ("scene", 60, "060_flee_to_escape.jpg",            "They said to Lot — get your family out. We are about to destroy this place.",                                        "zoom_in"),
    ("scene", 61, "061_angels_urged_hurry.jpg",        "At dawn, the angels urged Lot to hurry. 'Flee! And don't look back.'",                                              "zoom_out"),
    ("scene", 62, "062_burning_sulfur.jpg",            "Then the Lord rained burning sulfur on Sodom and Gomorrah.",                                                         "zoom_in"),
    ("scene", 63, "063_lots_wife.jpg",                 "Lot's wife looked back. And she became a pillar of salt.",                                                           "pan_right"),
    ("scene", 64, "064_dense_smoke.jpg",               "Abraham looked toward Sodom. Dense smoke rose from the land, like smoke from a furnace.",                            "zoom_out"),

    ("title", 5, "THE BIRTH OF ISAAC", ""),
    ("scene", 65, "065_god_remembered.jpg",            "God remembered His promise.",                                                                                        "zoom_in"),
    ("scene", 66, "066_sarah_conceived.jpg",           "Sarah conceived. At ninety years old.",                                                                              "zoom_out"),
    ("scene", 67, "067_bore_a_son.jpg",                "She bore a son.",                                                                                                    "zoom_in"),
    ("scene", 68, "068_named_isaac.jpg",               "Abraham named him Isaac — which means: he laughs.",                                                                  "pan_right"),
    ("scene", 69, "069_sarah_said.jpg",                "Sarah said — God has brought me laughter. [laughs] Everyone who hears about this will laugh with me.",                        "zoom_out"),
    ("scene", 70, "070_who_would_have_said.jpg",       "Who would have said that Sarah would nurse children? Yet I have borne him a son in his old age.",                    "zoom_in"),
    ("scene", 71, "071_abraham_hundred.jpg",           "Abraham was one hundred years old when Isaac was born.",                                                             "zoom_out"),
    ("scene", 72, "072_trouble_entered.jpg",           "But not long after, trouble entered the tent.",                                                                      "pan_right"),
    ("scene", 73, "073_hagar_son_mocking.jpg",         "Sarah saw Hagar's son Ishmael mocking Isaac.",                                                                      "zoom_in"),
    ("scene", 74, "074_send_them_away.jpg",            "She told Abraham — send that woman and her son away.",                                                               "zoom_out"),
    ("scene", 75, "075_hard_thing.jpg",                "It was a hard thing. [sighs] But God told Abraham — listen to what Sarah says.",                                             "zoom_in"),
    ("scene", 76, "076_hagar_desert.jpg",              "Hagar and Ishmael went into the desert. And God was with the boy.",                                                  "pan_right"),

    ("title", 6, "THE BINDING OF ISAAC", ""),
    ("scene", 77, "077_god_tested_abraham.jpg",        "Then God tested Abraham.",                                                                                           "zoom_out"),
    ("scene", 78, "078_take_your_son.jpg",             "Take your son. Your only son. The one you love. Isaac.",                                                             "zoom_in"),
    ("scene", 79, "079_go_to_moriah.jpg",              "Go to the region of Moriah and offer him as a burnt offering.",                                                      "zoom_out"),
    ("scene", 80, "080_rose_early.jpg",                "Abraham rose early in the morning. He saddled his donkey.",                                                          "pan_right"),
    ("scene", 81, "081_cut_the_wood.jpg",              "He cut the wood for the offering. He set out with two servants and his son.",                                        "zoom_in"),
    ("scene", 82, "082_third_day_mountain.jpg",        "On the third day, he looked up and saw the place in the distance.",                                                  "zoom_out"),
    ("scene", 83, "083_stay_here_with_donkey.jpg",     "He told his servants — stay here with the donkey. The boy and I will go over there. We will worship. And we will come back.", "zoom_in"),
    ("scene", 84, "084_wood_on_isaac.jpg",             "Abraham laid the wood on Isaac. He carried the fire and the knife.",                                                 "pan_right"),
    ("scene", 85, "085_isaac_said_father.jpg",         "Isaac said — Father?",                                                                                               "zoom_out"),
    ("scene", 86, "086_abraham_answered.jpg",          "Abraham answered — Yes, my son?",                                                                                    "zoom_in"),
    ("scene", 87, "087_where_is_the_lamb.jpg",         "The fire and the wood are here. But where is the lamb?",                                                             "zoom_out"),
    ("scene", 88, "088_god_will_provide.jpg",          "Abraham said — God will provide the lamb, my son.",                                                                  "pan_right"),
    ("scene", 89, "089_went_on_together.jpg",          "And the two of them went on together.",                                                                               "zoom_in"),
    ("scene", 90, "090_built_the_altar.jpg",           "Abraham built the altar. He bound his son. He laid him on the wood.",                                                "zoom_out"),
    ("scene", 91, "091_raised_the_knife.jpg",          "He raised the knife.",                                                                                                "zoom_in"),
    ("scene", 92, "092_angel_called.jpg",              "Then the angel called — Abraham! Abraham! Do not harm the boy.",                                                     "pan_right"),
    ("scene", 93, "093_ram_in_thicket.jpg",            "Abraham looked — and saw a ram caught in the thicket.",                                                              "zoom_out"),
    ("scene", 94, "094_lord_will_provide.jpg",         "He called that place — The Lord Will Provide. And so the saying arose.",                                             "zoom_in"),

    ("title", 7, "REBEKAH — WIFE OF ISAAC", ""),
    ("scene", 95, "095_sarah_died.jpg",                "[sighs] Sarah died at one hundred and twenty-seven years old. Abraham mourned deeply for her.",                              "zoom_out"),
    ("scene", 96, "096_cave_of_machpelah.jpg",         "He bought a field and a cave from the Hittites at Machpelah to bury her.",                                          "pan_right"),
    ("scene", 97, "097_swear_to_me.jpg",               "Then Abraham called his oldest servant. 'Swear you will not get a wife for my son from the Canaanites.'",           "zoom_in"),
    ("scene", 98, "098_go_to_my_homeland.jpg",         "You will go to my homeland. And find a wife for Isaac from among my own people.",                                    "zoom_out"),
    ("scene", 99, "099_ten_camels.jpg",                "The servant set out with ten camels loaded with gifts.",                                                              "zoom_in"),
    ("scene",100, "100_well_of_nahor.jpg",             "At a well outside the city of Nahor, he stopped and prayed.",                                                        "pan_right"),
    ("scene",101, "101_the_prayer.jpg",                "Let the girl who gives water to my camels be the one you have chosen for Isaac.",                                    "zoom_out"),
    ("scene",102, "102_rebekah_approaches.jpg",        "Before he had finished praying — Rebekah came out with a jar on her shoulder.",                                      "zoom_in"),
    ("scene",103, "103_she_watered_camels.jpg",        "She gave him water. Then she watered all ten camels — without being asked.",                                         "zoom_out"),
    ("scene",104, "104_servant_bowed.jpg",             "The servant bowed his head and worshiped the Lord.",                                                                 "pan_right"),
    ("scene",105, "105_this_is_from_the_lord.jpg",     "He went to her family. He told them everything. And they said — this is from the Lord.",                             "zoom_in"),
    ("scene",106, "106_isaac_loved_her.jpg",           "Isaac saw her coming from a distance. He married her. He loved her.",                                                "zoom_out"),

    ("title", 8, "JACOB AND ESAU", ""),
    ("scene",107, "107_two_sons.jpg",                  "Isaac and Rebekah had two sons.",                                                                                    "zoom_in"),
    ("scene",108, "108_esau_red_hairy.jpg",            "The first came out red and hairy — they named him Esau.",                                                            "pan_right"),
    ("scene",109, "109_jacob_grasping_heel.jpg",       "The second came out grasping Esau's heel — they named him Jacob.",                                                   "zoom_out"),
    ("scene",110, "110_esau_hunter.jpg",               "Esau was a skillful hunter. A man of the open country.",                                                             "zoom_in"),
    ("scene",111, "111_jacob_stayed_tents.jpg",        "Jacob was a quiet man. He stayed among the tents.",                                                                  "zoom_out"),
    ("scene",112, "112_isaac_loved_esau.jpg",          "Isaac loved Esau. Rebekah loved Jacob.",                                                                             "pan_right"),
    ("scene",113, "113_esau_came_in_exhausted.jpg",    "One day, Esau came in from the fields exhausted. Jacob was cooking stew.",                                           "zoom_in"),
    ("scene",114, "114_give_me_the_stew.jpg",          "Esau said — give me some of that red stew. I'm starving.",                                                           "zoom_out"),
    ("scene",115, "115_sell_me_your_birthright.jpg",   "Jacob said — sell me your birthright first.",                                                                        "zoom_in"),
    ("scene",116, "116_what_good_is_birthright.jpg",   "Esau said — what good is my birthright if I die of hunger?",                                                        "pan_right"),
    ("scene",117, "117_sold_for_stew.jpg",             "He sold his birthright for a bowl of stew.",                                                                         "zoom_out"),
    ("scene",118, "118_isaac_old_eyes_dim.jpg",        "Years passed. Isaac grew old and his eyes grew dim.",                                                                "zoom_in"),
    ("scene",119, "119_isaac_calls_esau.jpg",          "He called Esau — go hunt and make me a meal. Before I die, I will give you my blessing.",                           "zoom_out"),
    ("scene",120, "120_rebekah_overheard.jpg",         "Rebekah overheard. She told Jacob — listen to what I say.",                                                          "pan_right"),
    ("scene",121, "121_jacob_disguised.jpg",           "She dressed Jacob in Esau's clothes. She put goatskin on his hands and neck.",                                       "zoom_in"),
    ("scene",122, "122_i_am_esau.jpg",                 "Jacob went to his blind father. 'I am Esau your firstborn.'",                                                        "zoom_out"),
    ("scene",123, "123_voice_is_jacobs.jpg",           "Isaac said — the voice is Jacob's. But the hands are Esau's.",                                                       "zoom_in"),
    ("scene",124, "124_isaac_blessed_jacob.jpg",       "He was deceived. He blessed Jacob with Esau's blessing.",                                                            "pan_right"),
    ("scene",125, "125_esau_discovered.jpg",           "Esau came in — and discovered it too late.",                                                                         "zoom_out"),
    ("scene",126, "126_esau_wept.jpg",                 "He wept. He raged. [sighs] He said — my brother has stolen from me twice.",                                                  "zoom_in"),

    ("title", 9, "JACOBS DREAM AT BETHEL", ""),
    ("scene",127, "127_esau_hated_jacob.jpg",          "Esau hated Jacob for what he had done. He planned to kill him.",                                                     "zoom_out"),
    ("scene",128, "128_flee_to_haran.jpg",             "Rebekah warned Jacob — flee to my brother Laban in Haran.",                                                          "pan_right"),
    ("scene",129, "129_jacob_left_alone.jpg",          "Jacob left with nothing but his staff.",                                                                              "zoom_in"),
    ("scene",130, "130_stone_under_head.jpg",          "That night, he lay down on the ground, a stone under his head.",                                                     "zoom_out"),
    ("scene",131, "131_jacobs_ladder.jpg",             "He dreamed. A stairway reaching from earth to heaven. Angels ascending and descending.",                              "zoom_in"),
    ("scene",132, "132_i_am_the_god.jpg",              "The Lord stood above it and said — I am the God of Abraham and Isaac.",                                              "pan_right"),
    ("scene",133, "133_land_i_give_you.jpg",           "The land you lie on — I give to you and your descendants.",                                                          "zoom_out"),
    ("scene",134, "134_i_will_be_with_you.jpg",        "And I will be with you wherever you go.",                                                                            "zoom_in"),
    ("scene",135, "135_jacob_woke_in_awe.jpg",         "[gasps] Jacob woke in awe. 'Surely the Lord is in this place. How awesome is this place.'",                                 "zoom_out"),
    ("scene",136, "136_bethel.jpg",                    "He set the stone upright as a pillar and poured oil over it. He called the place Bethel — House of God.",           "pan_right"),

    ("title",10, "JACOB — LEAH AND RACHEL", ""),
    ("scene",137, "137_land_of_the_east.jpg",          "Jacob arrived in the land of the east.",                                                                             "zoom_in"),
    ("scene",138, "138_well_with_shepherds.jpg",       "He came to a well. Shepherds were gathered there, waiting to water their flocks.",                                   "zoom_out"),
    ("scene",139, "139_rachel_approaches.jpg",         "A beautiful young woman approached with her father's sheep.",                                                         "zoom_in"),
    ("scene",140, "140_daughter_of_laban.jpg",         "Her name was Rachel. She was the daughter of Laban — his mother's brother.",                                        "pan_right"),
    ("scene",141, "141_jacob_kissed_rachel.jpg",       "Jacob kissed Rachel and wept.",                                                                                      "zoom_out"),
    ("scene",142, "142_work_for_laban.jpg",            "He worked for Laban for a month. Then Laban asked — what shall I pay you?",                                         "zoom_in"),
    ("scene",143, "143_seven_years_for_rachel.jpg",    "Jacob said — I will serve you seven years for Rachel, your younger daughter.",                                       "zoom_out"),
    ("scene",144, "144_seemed_few_days.jpg",           "The seven years seemed like only a few days to him, because he loved her.",                                          "pan_right"),
    ("scene",145, "145_wedding_night_deceived.jpg",    "But on the wedding night, Laban deceived him — and gave him Leah, the older daughter, instead.",                    "zoom_in"),
    ("scene",146, "146_in_morning_saw_leah.jpg",       "In the morning, Jacob saw it was Leah. He went to Laban — what have you done to me?",                               "zoom_out"),
    ("scene",147, "147_older_before_younger.jpg",      "Laban said — in our country, we do not give the younger daughter before the firstborn.",                             "zoom_in"),
    ("scene",148, "148_seven_more_years.jpg",          "Finish this week — and I will give you Rachel as well. For seven more years of work.",                               "pan_right"),
    ("scene",149, "149_jacob_loved_rachel.jpg",        "Jacob agreed. He loved Rachel. He served seven more years.",                                                         "zoom_out"),
    ("scene",150, "150_twelve_tribes.jpg",             "From Jacob and his wives, twelve sons were born — the twelve tribes of Israel.",                                     "zoom_in"),

    ("title",11, "JACOB WRESTLES WITH GOD", ""),
    ("scene",151, "151_return_to_canaan.jpg",          "After twenty years, God told Jacob — return to the land of your fathers.",                                           "zoom_out"),
    ("scene",152, "152_jacob_set_out.jpg",             "Jacob set out with his wives, his children, his flocks, his herds, his servants.",                                   "pan_right"),
    ("scene",153, "153_esau_four_hundred.jpg",         "But he was afraid. Esau was coming to meet him with four hundred men.",                                              "zoom_in"),
    ("scene",154, "154_divided_into_two.jpg",          "Jacob divided his people and animals into two groups — if Esau attacks one, the other may escape.",                 "zoom_out"),
    ("scene",155, "155_left_alone.jpg",                "He sent everything ahead and was left alone.",                                                                        "zoom_in"),
    ("scene",156, "156_man_wrestled.jpg",              "A man wrestled with him until the breaking of the day.",                                                             "pan_right"),
    ("scene",157, "157_touched_hip.jpg",               "When the man saw that he could not overpower him, he touched Jacob's hip — and wrenched it.",                       "zoom_out"),
    ("scene",158, "158_let_me_go.jpg",                 "The man said — let me go. The day is breaking.",                                                                     "zoom_in"),
    ("scene",159, "159_i_will_not_let_go.jpg",         "Jacob said — I will not let you go unless you bless me.",                                                            "zoom_out"),
    ("scene",160, "160_what_is_your_name.jpg",         "The man asked — what is your name?",                                                                                 "pan_right"),
    ("scene",161, "161_jacob_answered.jpg",            "Jacob answered. And the man said — your name will no longer be Jacob.",                                              "zoom_in"),
    ("scene",162, "162_name_is_israel.jpg",            "It will be Israel — for you have striven with God and with men — and you have prevailed.",                           "zoom_out"),

    ("title",12, "JOSEPH AND HIS BROTHERS", "c. 1900 BC"),
    ("scene",163, "163_jacob_settled_canaan.jpg",      "Jacob settled in the land of Canaan.",                                                                               "zoom_in"),
    ("scene",164, "164_twelve_sons.jpg",               "He had twelve sons. But one he loved more than all the others.",                                                     "pan_right"),
    ("scene",165, "165_his_name_was_joseph.jpg",       "His name was Joseph.",                                                                                               "zoom_out"),
    ("scene",166, "166_coat_of_many_colors.jpg",       "Jacob made him a beautiful robe — a coat of many colors.",                                                           "zoom_in"),
    ("scene",167, "167_brothers_hated_him.jpg",        "When Joseph's brothers saw that their father loved him more, they hated him.",                                       "zoom_out"),
    ("scene",168, "168_could_not_speak.jpg",           "They could not speak a kind word to him.",                                                                           "pan_right"),
    ("scene",169, "169_joseph_dreamed.jpg",            "Joseph dreamed a dream and told his brothers.",                                                                      "zoom_in"),
    ("scene",170, "170_sheaves_bowing.jpg",            "We were binding sheaves in the field. My sheaf rose and stood upright. And your sheaves gathered around and bowed down to mine.", "zoom_out"),
    ("scene",171, "171_do_you_intend_to_reign.jpg",    "His brothers said — do you intend to reign over us?",                                                               "zoom_in"),
    ("scene",172, "172_second_dream.jpg",              "He dreamed again. The sun and moon and eleven stars were bowing down to me.",                                        "pan_right"),
    ("scene",173, "173_even_father_rebuked.jpg",       "Even his father rebuked him — what is this dream? Shall I and your mother and brothers all bow down to you?",       "zoom_out"),
    ("scene",174, "174_jacob_sent_joseph.jpg",         "One day, the brothers were tending flocks far from home. Jacob sent Joseph to check on them.",                       "zoom_in"),
    ("scene",175, "175_here_comes_the_dreamer.jpg",    "They saw him coming from a distance. They said — here comes the dreamer.",                                          "zoom_out"),
    ("scene",176, "176_lets_kill_him.jpg",             "Let's kill him and throw him into a pit.",                                                                           "pan_right"),
    ("scene",177, "177_reuben_said_no.jpg",            "Reuben — the oldest — said no. Throw him in the pit but do not kill him. He planned to rescue Joseph later.",       "zoom_in"),
    ("scene",178, "178_stripped_and_pit.jpg",          "They stripped Joseph of his beautiful coat. They threw him in the pit.",                                             "zoom_out"),
    ("scene",179, "179_sold_to_traders.jpg",           "A caravan of Ishmaelite traders passed by. The brothers sold Joseph for twenty pieces of silver.",                   "zoom_in"),
    ("scene",180, "180_jacob_wept.jpg",                "They dipped his coat in goat's blood and took it back to their father. Jacob wept for years. [sighs]",                       "pan_right"),

    ("title",13, "JOSEPH IN EGYPT", ""),
    ("scene",181, "181_traders_to_egypt.jpg",          "The traders brought Joseph down to Egypt.",                                                                          "zoom_out"),
    ("scene",182, "182_sold_to_potiphar.jpg",          "He was sold to Potiphar — an officer of Pharaoh, captain of the guard.",                                            "zoom_in"),
    ("scene",183, "183_lord_with_joseph.jpg",          "The Lord was with Joseph. Everything he touched prospered.",                                                         "zoom_out"),
    ("scene",184, "184_potiphar_noticed.jpg",          "Potiphar noticed — this Hebrew's god is with him.",                                                                  "pan_right"),
    ("scene",185, "185_put_joseph_in_charge.jpg",      "He put Joseph in charge of his entire household.",                                                                   "zoom_in"),
    ("scene",186, "186_potiphars_wife.jpg",            "But Potiphar's wife noticed Joseph. He was handsome and well-built.",                                                "zoom_out"),
    ("scene",187, "187_come_to_bed.jpg",               "She said — come to bed with me.",                                                                                    "zoom_in"),
    ("scene",188, "188_joseph_refused.jpg",            "Joseph refused. Day after day. He would not sin against his master. He would not sin against God.",                  "pan_right"),
    ("scene",189, "189_she_grabbed_cloak.jpg",         "One day she grabbed his cloak. He fled and left his cloak in her hand.",                                             "zoom_out"),
    ("scene",190, "190_she_lied.jpg",                  "She told her husband — the Hebrew slave tried to attack me.",                                                        "zoom_in"),
    ("scene",191, "191_thrown_in_prison.jpg",          "Potiphar was furious. He threw Joseph in prison.",                                                                   "zoom_out"),
    ("scene",192, "192_lord_with_joseph_prison.jpg",   "But the Lord was with Joseph — even in prison. The warden put Joseph in charge of everything.",                     "pan_right"),
    ("scene",193, "193_cupbearer_baker.jpg",           "Two of Pharaoh's servants were thrown into prison — the cupbearer and the baker.",                                   "zoom_in"),
    ("scene",194, "194_each_had_a_dream.jpg",          "Each of them had a dream the same night. Each dream had a meaning.",                                                 "zoom_out"),
    ("scene",195, "195_joseph_interpreted.jpg",        "Joseph interpreted their dreams. To the cupbearer — in three days you will be restored. Remember me.",               "zoom_in"),
    ("scene",196, "196_cupbearer_forgot.jpg",          "The cupbearer was restored. But he forgot Joseph. [sighs] Joseph remained in prison for two more years.",                     "pan_right"),

    ("title",14, "PHARAOHS DREAMS", ""),
    ("scene",197, "197_pharaoh_had_a_dream.jpg",       "Then Pharaoh had a dream.",                                                                                          "zoom_out"),
    ("scene",198, "198_seven_fat_cows.jpg",            "Seven fat cows rose from the Nile. Seven thin cows devoured them.",                                                  "zoom_in"),
    ("scene",199, "199_seven_heads_of_grain.jpg",      "Seven healthy heads of grain. Seven scorched heads swallowed them.",                                                 "zoom_out"),
    ("scene",200, "200_none_could_interpret.jpg",      "None of Egypt's wise men could interpret the dreams.",                                                               "pan_right"),
    ("scene",201, "201_cupbearer_remembered.jpg",      "The cupbearer remembered — there is a Hebrew in the prison who interprets dreams.",                                  "zoom_in"),
    ("scene",202, "202_joseph_brought_out.jpg",        "They brought Joseph out. He was shaved and given clean clothes.",                                                    "zoom_out"),
    ("scene",203, "203_stood_before_pharaoh.jpg",      "He stood before Pharaoh.",                                                                                           "zoom_in"),
    ("scene",204, "204_god_will_give_answer.jpg",      "Joseph said — it is not I who interprets. God will give Pharaoh the answer.",                                       "pan_right"),
    ("scene",205, "205_seven_years_abundance.jpg",     "Seven years of great abundance are coming. Followed by seven years of terrible famine.",                             "zoom_out"),
    ("scene",206, "206_appoint_wise_man.jpg",          "Let Pharaoh appoint a wise man and set him over the land of Egypt.",                                                 "zoom_in"),
    ("scene",207, "207_spirit_of_god.jpg",             "Pharaoh said — can we find anyone like this man, in whom is the spirit of God?",                                    "zoom_out"),
    ("scene",208, "208_signet_ring.jpg",               "He placed his signet ring on Joseph's finger. He gave him gold and fine linen.",                                    "pan_right"),
    ("scene",209, "209_joseph_thirty.jpg",             "Joseph was thirty years old when he stood before Pharaoh.",                                                          "zoom_in"),
    ("scene",210, "210_seven_years_abundance.jpg",     "Seven years of abundance came. Joseph stored grain beyond counting.",                                                 "zoom_out"),
    ("scene",211, "211_famine_began.jpg",              "Then the famine began. It spread over the whole world.",                                                              "zoom_in"),
    ("scene",212, "212_jacob_sent_sons.jpg",           "Jacob heard there was grain in Egypt and sent his sons.",                                                             "pan_right"),
    ("scene",213, "213_brothers_bowed.jpg",            "Joseph's brothers came and bowed down before him with their faces to the ground.",                                   "zoom_out"),
    ("scene",214, "214_joseph_recognized.jpg",         "Joseph recognized them. They did not recognize him. [sighs] He wept in secret.",                                             "zoom_in"),
    ("scene",215, "215_he_tested_them.jpg",            "He tested them. He accused them. He watched their hearts.",                                                          "zoom_out"),
    ("scene",216, "216_could_not_control.jpg",         "Finally — he could not control himself. He wept so loudly the Egyptians heard.",                                    "pan_right"),
    ("scene",217, "217_i_am_joseph.jpg",               "I am Joseph. [sighs] Is my father still alive?",                                                                             "zoom_in"),
    ("scene",218, "218_jacob_comes_to_egypt.jpg",      "Jacob came to Egypt. Joseph rode out to meet him. He held his father and wept.",                                    "zoom_out"),

]

# Derived lists
SCENES = [(item[1], item[2], item[3], item[4]) for item in CONTENT if item[0] == "scene"]
TITLES = [(item[1], item[2], item[3]) for item in CONTENT if item[0] == "title"]
TOTAL_SCENES = len(SCENES)


SRT_DIR    = Path("project/documentary/stories/subtitles")
STORIES_DIR = Path("project/documentary/stories")

# (title_card_num, scene_start, scene_end) for per-story assembly
STORY_ASSEMBLY = {
    "06_calling_of_abram.mp4":        (1,   1,   18),
    "07_covenant_with_god.mp4":       (2,   19,  34),
    "08_the_three_visitors.mp4":      (3,   35,  46),
    "09_sodom_and_gomorrah.mp4":      (4,   47,  64),
    "10_birth_of_isaac.mp4":          (5,   65,  76),
    "11_binding_of_isaac.mp4":        (6,   77,  94),
    "12_rebekah_wife_of_isaac.mp4":   (7,   95,  106),
    "13_jacob_and_esau.mp4":          (8,   107, 126),
    "14_jacobs_dream_at_bethel.mp4":  (9,   127, 136),
    "15_jacob_leah_and_rachel.mp4":   (10,  137, 150),
    "16_jacob_wrestles_with_god.mp4": (11,  151, 162),
    "17_joseph_and_his_brothers.mp4": (12,  163, 180),
    "18_joseph_in_egypt.mp4":         (13,  181, 196),
    "19_pharaohs_dreams.mp4":         (14,  197, 218),
}

# scene ranges for SRT generation (subset of STORY_ASSEMBLY)
STORY_SCENE_RANGES = {k: (v[1], v[2]) for k, v in STORY_ASSEMBLY.items()}


def load_env():
    env = {}
    p = Path(".env")
    if p.exists():
        for line in p.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip())


def fmt_srt_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_story_srt(story_file, scene_start, scene_end):
    """Generate SRT content for one story using audio file durations."""
    import re
    TITLE_DUR = 5.0
    entries = []
    entry_n = 1
    t = TITLE_DUR  # start after title card

    for item in CONTENT:
        if item[0] != "scene":
            continue
        scene_num, filename, narration, motion = item[1], item[2], item[3], item[4]
        if not (scene_start <= scene_num <= scene_end):
            continue

        audio_file = AUDIO_DIR / f"{scene_num:03d}.mp3"
        if not audio_file.exists():
            t += 3.0 + SILENCE_PAD  # rough estimate if missing
            continue

        audio_dur = get_duration(audio_file)
        clean = re.sub(r'\[[^\]]+\]', '', narration).strip()
        clean = re.sub(r'\s+', ' ', clean)

        if clean:
            entries.append(
                f"{entry_n}\n"
                f"{fmt_srt_time(t)} --> {fmt_srt_time(t + audio_dur)}\n"
                f"{clean}\n"
            )
            entry_n += 1

        t += audio_dur + SILENCE_PAD

    return "\n".join(entries)


def generate_tts(text, out_path, key):
    resp = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        json={
            "text": text,
            "model_id": EL_MODEL,
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.80,
                "style": 0.35,
                "use_speaker_boost": True,
            },
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"ElevenLabs {resp.status_code}: {resp.text[:200]}")
    Path(out_path).write_bytes(resp.content)


def make_clip(img_path, audio_path, out_path, motion, video_dur):
    frames = max(FPS, int(video_dur * FPS))
    zp = MOTION[motion]
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
        f"zoompan={zp}:d={frames}:s={W}x{H}:fps={FPS},"
        f"fade=t=in:st=0:d={FADE},"
        f"fade=t=out:st={video_dur - FADE:.3f}:d={FADE},"
        f"format=yuv420p"
    )
    af = (
        f"apad=pad_dur={video_dur:.3f},atrim=0:{video_dur:.3f},"
        f"afade=t=in:st=0:d=0.1,afade=t=out:st={max(0, video_dur - 0.15):.3f}:d=0.1"
    )
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(img_path),
        "-i", str(audio_path),
        "-vf", vf, "-af", af,
        "-t", str(video_dur),
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(out_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {r.stderr[-400:]}")


def make_title_card(story_num, title_text, subtitle_text, out_path, duration=5.0):
    """Generate a black title card with white text using FFmpeg drawtext."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    tf1 = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
    tf1.write(title_text)
    tf1.close()

    tf2 = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
    tf2.write(subtitle_text if subtitle_text else "")
    tf2.close()

    try:
        fontfile = FONT_FILE if Path(FONT_FILE).exists() else ""
        font_opt = f":fontfile={fontfile}" if fontfile else ""

        if subtitle_text:
            vf = (
                f"drawtext=textfile='{tf1.name}':fontcolor=white:fontsize=80"
                f":x=(w-text_w)/2:y=(h-text_h)/2-55{font_opt},"
                f"drawtext=textfile='{tf2.name}':fontcolor=0xAAAAAA:fontsize=50"
                f":x=(w-text_w)/2:y=(h-text_h)/2+55{font_opt},"
                f"fade=t=in:st=0:d=0.5:color=black,"
                f"fade=t=out:st={duration-0.5:.1f}:d=0.5:color=black"
            )
        else:
            vf = (
                f"drawtext=textfile='{tf1.name}':fontcolor=white:fontsize=80"
                f":x=(w-text_w)/2:y=(h-text_h)/2{font_opt},"
                f"fade=t=in:st=0:d=0.5:color=black,"
                f"fade=t=out:st={duration-0.5:.1f}:d=0.5:color=black"
            )

        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}",
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-vf", vf,
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "96k",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(out_path),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"Title card error: {r.stderr[-300:]}")
    finally:
        os.unlink(tf1.name)
        os.unlink(tf2.name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start",      type=int, default=1,           help="Resume from scene N")
    parser.add_argument("--end",        type=int, default=TOTAL_SCENES, help="End at scene N (by scene number)")
    parser.add_argument("--skip-audio", action="store_true",           help="Skip TTS, reuse existing audio")
    parser.add_argument("--skip-clips", action="store_true",           help="Skip clip render, go to assembly")
    parser.add_argument("--assemble-only", action="store_true",        help="Only run assembly phase")
    args = parser.parse_args()

    if args.assemble_only:
        args.skip_audio = True
        args.skip_clips = True

    env = load_env()
    el_key = env.get("ELEVENLABS_API_KEY", "")
    if not el_key and not args.skip_audio:
        sys.exit("ELEVENLABS_API_KEY not in .env")

    # Filter scenes to range
    scenes_in_range = [(num, fn, nar, mot) for (num, fn, nar, mot) in SCENES
                       if args.start <= num <= args.end]

    # ── Phase 1: TTS ──────────────────────────────────────────────────────────
    if not args.skip_audio:
        print(f"\n{'='*60}")
        print(f"  Phase 1: TTS voiceover ({len(scenes_in_range)} lines)")
        print(f"{'='*60}")
        for scene_num, filename, narration, motion in scenes_in_range:
            audio_out = AUDIO_DIR / f"{scene_num:03d}.mp3"
            if audio_out.exists():
                print(f"  [{scene_num:03d}] Audio exists, skipping")
                continue
            print(f"  [{scene_num:03d}] \"{narration[:65]}{'…' if len(narration)>65 else ''}\"")
            for attempt in range(3):
                try:
                    generate_tts(narration, audio_out, el_key)
                    print(f"         ✓ {audio_out.stat().st_size // 1024}KB")
                    break
                except Exception as e:
                    print(f"         ✗ Attempt {attempt+1}: {e}")
                    if attempt < 2:
                        time.sleep(5)

    # ── Phase 2a: Title cards ─────────────────────────────────────────────────
    if not args.skip_clips:
        print(f"\n{'='*60}")
        print(f"  Phase 2a: Title cards ({len(TITLES)} cards)")
        print(f"{'='*60}")
        for story_num, title_text, subtitle_text in TITLES:
            tc_path = TCARDS_DIR / f"tc_{story_num:02d}.mp4"
            if tc_path.exists():
                print(f"  Story {story_num:02d}: Title card exists, skipping")
                continue
            print(f"  Story {story_num:02d}: {title_text}")
            try:
                make_title_card(story_num, title_text, subtitle_text, tc_path)
                print(f"         ✓ Done")
            except Exception as e:
                print(f"         ✗ {e}")

    # ── Phase 2b: Scene clips ─────────────────────────────────────────────────
    if not args.skip_clips:
        print(f"\n{'='*60}")
        print(f"  Phase 2b: Rendering clips ({len(scenes_in_range)} scenes)")
        print(f"{'='*60}")
        for scene_num, filename, narration, motion in scenes_in_range:
            img_path   = IMG_DIR / filename
            audio_path = AUDIO_DIR / f"{scene_num:03d}.mp3"
            clip_path  = CLIPS_DIR / f"{scene_num:03d}.mp4"

            if clip_path.exists():
                print(f"  [{scene_num:03d}] Clip exists, skipping")
                continue
            if not img_path.exists():
                print(f"  [{scene_num:03d}] ✗ Image missing: {filename}")
                continue
            if not audio_path.exists():
                print(f"  [{scene_num:03d}] ✗ Audio missing: {scene_num:03d}.mp3")
                continue

            dur = get_duration(audio_path) + SILENCE_PAD
            print(f"  [{scene_num:03d}] {filename} ({dur:.2f}s)...")
            try:
                make_clip(img_path, audio_path, clip_path, motion, dur)
                print(f"         ✓ Done")
            except Exception as e:
                print(f"         ✗ {e}")

    # ── Phase 3: Assembly ─────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Phase 3: Assembly")
    print(f"{'='*60}")

    all_clips = []
    missing   = []

    for item in CONTENT:
        if item[0] == "title":
            story_num = item[1]
            tc_path = TCARDS_DIR / f"tc_{story_num:02d}.mp4"
            if tc_path.exists():
                all_clips.append(tc_path)
            else:
                missing.append(f"title_card_{story_num:02d}")
        else:  # scene
            scene_num = item[1]
            clip_path = CLIPS_DIR / f"{scene_num:03d}.mp4"
            if clip_path.exists():
                all_clips.append(clip_path)
            else:
                missing.append(f"scene_{scene_num:03d}")

    total_items = len(CONTENT)
    print(f"  Ready: {len(all_clips)}/{total_items} clips")
    if missing:
        print(f"  Missing ({len(missing)}): {missing[:10]}{'...' if len(missing)>10 else ''}")

    if len(all_clips) < 10:
        print("  Not enough clips for assembly. Run phases 1 and 2 first.")
        return

    list_file = OUTPUT_DIR / "genesis_concat_list.txt"
    list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in all_clips))

    print(f"  Assembling {len(all_clips)} clips...")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c", "copy",
        "-movflags", "+faststart",
        str(FINAL_OUT),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  Assembly error: {r.stderr[-400:]}")
        return

    size_mb = FINAL_OUT.stat().st_size / 1_000_000
    print(f"\n✓ {FINAL_OUT} ({size_mb:.1f} MB)")

    # ── Phase 3b: Per-story assembly for mix_audio.py ─────────────────────────
    print(f"\n{'='*60}")
    print(f"  Phase 3b: Assembling individual story files")
    print(f"{'='*60}")
    STORIES_DIR.mkdir(parents=True, exist_ok=True)
    story_list_file = OUTPUT_DIR / "story_concat_list.txt"
    for story_name, (tc_num, sc_start, sc_end) in STORY_ASSEMBLY.items():
        story_out = STORIES_DIR / story_name
        tc_path   = TCARDS_DIR / f"tc_{tc_num:02d}.mp4"
        story_clips = []
        if tc_path.exists():
            story_clips.append(tc_path)
        for sn in range(sc_start, sc_end + 1):
            cp = CLIPS_DIR / f"{sn:03d}.mp4"
            if cp.exists():
                story_clips.append(cp)
        if len(story_clips) < 2:
            print(f"  ✗ Not enough clips for {story_name}, skipping")
            continue
        story_list_file.write_text("\n".join(f"file '{p.resolve()}'" for p in story_clips))
        r = subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(story_list_file),
            "-c:v", "libx264", "-b:v", "600k", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart",
            str(story_out),
        ], capture_output=True, text=True)
        if r.returncode == 0:
            mb = story_out.stat().st_size / 1_000_000
            print(f"  ✓ {story_name} ({mb:.1f} MB)")
        else:
            print(f"  ✗ {story_name}: {r.stderr[-200:]}")

    # ── Phase 4: SRT subtitle files ───────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Phase 4: Generating SRT subtitle files")
    print(f"{'='*60}")
    SRT_DIR.mkdir(parents=True, exist_ok=True)
    for story_file, (sc_start, sc_end) in STORY_SCENE_RANGES.items():
        srt_path = SRT_DIR / story_file.replace(".mp4", ".srt")
        srt_content = build_story_srt(story_file, sc_start, sc_end)
        srt_path.write_text(srt_content, encoding="utf-8")
        line_count = srt_content.count("\n\n") + 1
        print(f"  ✓ {srt_path.name} ({line_count} entries)")

    web_out = OUTPUT_DIR / "genesis_patriarchs_720p.mp4"
    print("Encoding 720p web version...")
    cmd720 = [
        "ffmpeg", "-y", "-i", str(FINAL_OUT),
        "-vf", "scale=1280:720",
        "-c:v", "libx264", "-preset", "fast", "-crf", "28",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        str(web_out),
    ]
    r = subprocess.run(cmd720, capture_output=True, text=True)
    if r.returncode == 0:
        print(f"✓ Web version: {web_out} ({web_out.stat().st_size / 1_000_000:.1f} MB)")
    else:
        print(f"720p encode error: {r.stderr[-200:]}")


if __name__ == "__main__":
    main()
