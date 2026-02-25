"""
mikmakpy.constants
─────────────────
Defines game related constants: room IDs, safe chat message IDs, emote/dance IDs, etc.
"""

from enum import IntEnum, StrEnum


class Server(StrEnum):
    """Servers available for auto-join after initial connection."""

    KIWI = "קיווי"
    KREMBO = "קרמבו"
    ADMINS = "מנהלים"


class LoggerLevel(StrEnum):
    """Keys recognised by the logger_levels set."""

    INCOMING = "incoming"
    CONNECTION_CHANGE = "connection_change"
    OUTGOING = "outgoing"
    PARSING_ERROR = "parsing_error"
    INTERNAL_ERROR = "internal_error"


class EmoteFace(IntEnum):
    """Emote IDs (1000 series) - character expressions/animations."""

    # Row 1 (left to right)
    BLUSH_KISS = 1005  # Blushing with kiss mark
    COOL = 1006  # Sunglasses cool
    IN_LOVE = 1010  # Heart eyes loving
    WINK = 1011  # Winking
    SUSPICIOUS = 1012  # Skeptical/suspicious look
    ANGRY = 1013  # Angry red face
    HEARTBREAK = 1014  # Broken heart crying
    SICK = 1015  # Green sick face
    PLEADING = 1017  # Pleading/puppy eyes
    # Row 2 (left to right)
    PARTY = 1001  # Party celebration
    HEARTS_FLOAT = 1002  # Hearts floating around
    HEARTS_EYES = 1003  # Heart eyes excited
    LOVE = 1007  # Red heart eyes love
    SHOCKED = 1008  # Surprised/shocked
    THINKING = 1009  # Confused/thinking
    ANGEL = 1004  # Angel with halo
    SLEEPY = 1016  # Sleepy with zzz
    SLEEPING = 1018  # Sleeping


class Dance(IntEnum):
    """Dance IDs (2000 series) - character dance/movement animations."""

    # Row 1 (top, left to right)
    CHEER = 2030  # Arms out with sparkles
    WAVE = 2001  # Waving
    WIGGLE = 2002  # Arms wiggling
    WALK = 2013  # Walking motion
    SHRINK = 2014  # Shrinking inward
    SPIN = 2017  # Spinning around
    # Row 2 (bottom, left to right)
    JUMP = 2057  # Jumping (legs still)
    ARMS = 2003  # Arms moving (body still)
    HEAD = 2004  # Head moving (body still)
    FLIP = 2015  # Upside down flip
    HANDSTAND = 2016  # Handstand with hearts
    POINT = 2026  # Pointing (body still)
    # Sit directions (clockwise from left)
    SIT_L = 2008  # Sit facing left
    SIT_UL = 2005  # Sit facing up-left
    SIT_U = 2006  # Sit facing up
    SIT_UR = 2007  # Sit facing up-right
    SIT_R = 2009  # Sit facing right
    SIT_DR = 2012  # Sit facing down-right
    SIT_D = 2011  # Sit facing down
    SIT_DL = 2010  # Sit facing down-left


class SafeChat(IntEnum):
    """Safe chat message IDs - predefined messages (Hebrew)."""

    # Greetings (שלום)
    GREETINGS = 1  # שלום (parent menu)
    HI = 2  # היי
    HI_EVERYONE = 3  # היי לכולם
    HI_TO_YOU = 4  # היי לך
    HELLO_TO_YOU = 5  # שלום לך
    HELLO_EVERYONE = 6  # שלום לכולם
    WELCOME = 7  # ברוך הבא
    GOOD_MORNING = 8  # בוקר טוב
    GOOD_DAY = 9  # יום טוב
    HAVE_A_MIKMAK_DAY = 10  # שיהיה לך יום ממקמק
    SHABBAT_SHALOM = 11  # שבת שלום
    MIKCATION_DAY = 12  # יום מיקציון
    MAZAL_TOV = 13  # מזל טוב
    WAITER = 14  # מלצר

    # Goodbye (להתראות)
    GOODBYE = 15  # להתראות (parent menu)
    BYE_BYE = 16  # ביי ביי
    SEE_YOU = 17  # נתראה
    SEE_YOU_TOMORROW = 18  # נתראה מחר
    SEE_YOU_LATER = 19  # נתראה אחר כך
    SEE_YOU_LATER_2 = 20  # נתראה מאוחר יותר
    GOOD_NIGHT = 21  # לילה טוב
    HAVE_TO_GO = 24  # חייב/ת ללכת
    HAVE_TO_RUN = 25  # חייב/ת לרוץ
    IM_LEAVING = 26  # אני זז/ה
    WILL_RETURN_LATER = 27  # אחזור אחר כך
    BE_RIGHT_BACK = 28  # תכף אחזור

    # Friendship (חברות)
    FRIENDSHIP = 29  # חברות (parent menu)
    WANNA_BE_FRIENDS = 30  # רוצה להיות חבר שלי?
    SENT_FRIEND_REQUEST = 31  # שלחתי לך בקשת חברות
    FUN_BEING_FRIENDS = 33  # איזה כיף שאנחנו חברים
    FUN_PLAYING_WITH_YOU = 34  # כיף לי לשחק איתך
    PARTY_AT_MY_HOUSE = 35  # מסיבה בביתי

    # Join me (הצטרף אליי)
    JOIN_ME = 43  # הצטרף אליי (parent menu)
    COME_TO_MY_HOUSE = 44  # בוא/י לביתי
    JOIN_MY_GAME = 45  # הצטרף אליי למשחק
    JOIN_WORLD_TOUR = 46  # הצטרף אליי לסיבוב בעולם
    JOIN_MIKNION = 47  # הצטרף אליי למיקניון
    FOLLOW_ME = 48  # בוא/י אחרי

    # Questions (שאלות)
    QUESTIONS = 53  # שאלות (parent menu)
    WANNA_COME_WITH = 54  # רוצה לבוא איתי?
    WANNA_GO_SHOPPING = 55  # רוצה לבוא איתי לקניות?
    WANNA_GO_MIKNION = 56  # רוצה לבוא איתי למיקניון?
    WANNA_GO_MIKAFE = 57  # רוצה לבוא איתי למיקפה
    WHEN = 58  # מתי? (parent menu)
    WHEN_IS_YOUR_PARTY = 59  # מתי המסיבה שלך?
    WHEN_MEET_AGAIN = 60  # מתי ניפגש שוב?
    WHEN_YOU_COMING_BACK = 61  # מתי את/ה חוזר/ת?
    HOW_ARE_YOU = 62  # מה שלומך? (parent menu)
    WHATS_UP = 63  # מה נשמע?
    WHATS_NEW = 64  # מה חדש?
    WHATS_HAPPENING = 65  # מה קורה?
    WHATS_MIKMAKKING = 66  # מה מתמקמק?
    IM_NEW_SHOW_AROUND = 67  # אני חדש– אתה יכול להכיר לי את העולם?
    READ_NEW_BLOG = 68  # קראת כבר את הבלוג החדש?!
    WHAT_WOULD_YOU_LIKE = 69  # מה תרצה להזמין?

    # Answers (תשובות)
    ANSWERS = 73  # תשובות (parent menu)
    GREAT = 74  # אחלה
    COOL = 75  # סבבה
    GOOD = 76  # טוב
    NOT_GOOD = 77  # לא טוב
    EXCELLENT = 78  # מעולה
    SOON = 79  # עוד מעט
    SURE = 80  # ברור
    THANKS = 81  # תודה
    THANKS_EVERYONE = 82  # תודה לכולם
    THANKS_FOR_HELP = 83  # תודה על העזרה
    THANKS_FUN_PLAYING = 84  # תודה, היה כיף לשחק איתך
    PLEASE = 85  # בבקשה
    SORRY = 86  # סליחה
    LOVELY = 87  # מקסים

    # Games (משחקים)
    GAMES = 89  # משחקים (parent menu)
    WANNA_PLAY = 90  # רוצה לשחק איתי?
    WANNA_PLAY_AGAIN = 91  # רוצה לשחק שוב?
    WANNA_JOIN_GAME = 93  # רוצה להצטרף אליי למשחק?
    GOOD_GAME = 95  # משחק טוב!
    FOOTBALL = 150  # כדורגל!
    GAME_STARTING_SOON = 151  # עוד מעט המשחק מתחיל
    GAME_OVER = 152  # המשחק הסתיים
    GOOOAL = 154  # גוווווללל
    PASS_TO_ME = 155  # תמסור אליי
    COME_CHEER = 156  # בואו לעודד
    WE_WON = 157  # יש ניצחנו
    TRIVIA = 131  # טריוויה!
    I_KNOW_ANSWERS = 132  # אני יודע/ת את התשובות
    PLAY_TRIVIA = 134  # בוא לשחק בטריוויה?
    QUESTIONS_HARD = 135  # השאלות ממש קשות

    # Stop/Enough (מספיק)
    ENOUGH = 100  # מספיק (parent menu)
    LEAVE_ME_ALONE = 101  # תניח לי בבקשה
    MOVING_TO_OTHER_AREA = 102  # אני עובר לאזור אחר
    NOT_COMFORTABLE = 103  # זה לא נעים לי
    NOT_NICE = 104  # זה לא נחמד
    UNFRIENDLY_BEHAVIOR = 105  # התנהגות לא חברית

    # I like (אהבתי)
    I_LIKE = 107  # אהבתי (parent menu)
    NICE = 108  # יופי
    HOW_NICE = 109  # איזה יופי
    WELL_DONE = 110  # כל הכבוד!
    WONDERFUL = 111  # נהדר
    COOL_2 = 117  # מגניב
    CONGRATS = 112  # תתחדש (parent menu)
    CONGRATS_CLOTHES = 114  # תתחדש/י על הבגדים
    CONGRATS_HOUSE = 115  # תתחדש/י על הבית
    CONGRATS_FURNITURE = 116  # תתחדש/י על הרהיטים
    ADORABLE = 123  # מקסים (parent menu)
    ADORABLE_CLOTHES = 124  # הבגדים שלך מקסימים
    ADORABLE_HOUSE = 125  # מקסים איך שעיצבת את הבית שלך
    PRETTIEST_MIKMAK = 126  # אתה המיקמק הכי יפה שראיתי
    CUTE_MIKMAK = 127  # איזה מיקמק חמוד
    STUNNING = 128  # מהמם
    MIKMAKKING_IT = 129  # מיקמקת אותה!

    # Trading (החלפות)
    TRADING = 180  # החלפות (parent menu)
    WANNA_TRADE = 181  # רוצה להחליף איתי?
    READY_TO_TRADE = 184  # אני מוכן/ה להחליף איתך
    ADD_MORE_ITEMS = 185  # הוסף עוד פריט
    CHANGE_ITEM_PLEASE = 186  # תחליף פריט בבקשה
    ALREADY_HAVE_ITEM = 187  # יש לי כבר את הפריט הזה
    ITEM_LOOKS_GREAT = 188  # הפריט הזה יראה מצוין בבית שלך
    I_APPROVED_TRADE = 190  # אני אישרתי את ההחלפה
    NOT_MY_TASTE = 191  # הפריט הזה לא לטעמי
    LOVELY_ITEM = 192  # איזה פריט מקסים!

    # Achievements (הישגים)
    ACHIEVEMENTS = 136  # הישגים (parent menu)
    LEVELED_UP = 137  # איזה כיף,עליתי רמה
    JOIN_ACHIEVEMENT_HILL = 138  # הצטרף אליי להר ההישגים
    HAVE_MANY_ACHIEVEMENTS = 139  # יש לי כבר מלא הישגים
    CONGRATS_ACHIEVEMENT = 140  # איזה כיף קיבלת הישג
    WHAT_LEVEL_ARE_YOU = 141  # באיזו דרגה את/ה?
    IM_LEVEL_FOUR = 142  # אני בדרגה רביעית
    IM_LEVEL_FIVE = 143  # אני בדרגה חמישית
    IM_LEVEL_TEN = 144  # אני בדרגה עשירית
    JOIN_ADMIN_SERVER = 145  # הצטרף אליי לשרת מנהלים (note: XML has duplicate id=144)

    # Upgrades (שדרוגים)
    UPGRADES = 160  # שדרוגים (parent menu)
    GOT_NEW_UPGRADE = 161  # יש לך את השדרוג החדש?
    UNLOCK_TAXI = 162  # תפתחו מונית
    UNLOCK_JET_SKI = 163  # תפתח אופנוע ים
    UNLOCK_SHIP = 189  # תפתח ספינה
    UNLOCK_HELICOPTER = 159  # תפתח מסוק
    UNLOCK_YACHT = 131  # תפתח יאכטה (note: duplicate id with TRIVIA)
    UNLOCK_HEAD_TO_HEAD = 193  # תפתחו ראש בראש

    # Missions (משימות)
    MISSIONS = 167  # משימות (parent menu)
    WHERE_IS_FIRST = 168  # איפה הראשון?
    WHERE_IS_SECOND = 169  # איפה השני?
    WHERE_IS_THIRD = 170  # איפה השלישי?
    WHERE_IS_FOURTH = 171  # איפה הרביעי?
    WHERE_IS_LAST = 172  # איפה האחרון?
    FINISHED_MISSION = 173  # סיימתי את המשימה!
    NEW_MISSION = 174  # יש משימה חדשה!
    WHO_CAN_HELP = 175  # מי יכול לעזור לי?

    # Quick responses
    YES = 164  # כן
    NO = 165  # לא
    OK = 166  # OK


class SafeChatEmoji(IntEnum):
    """Emoji IDs (3000 series) - yellow smiley faces shown in chat bubble."""

    # Row 1 - Basic expressions
    SMILE = 3001
    LAUGH = 3002
    SAD = 3003
    CONFUSED = 3004
    WINK = 3005
    COOL = 3006
    TONGUE = 3007
    SURPRISED = 3008
    CRY = 3009
    SLEEPY = 3010
    KISS = 3011
    NERVOUS = 3012
    DIZZY = 3013
    NERD = 3014
    SLEEPING = 3015
    HEHE = 3016
    SILENT = 3017
    SICK = 3018
    THINKING = 3019
    ANGRY = 3020
    # Row 2 - Special expressions and objects
    DEVIL = 3021
    ANGEL_EVIL = 3022
    LOVE_EYES = 3023
    BORING = 3024
    IN_LOVE = 3025
    ANGEL = 3026
    COFFEE = 3027
    LATTE = 3028
    PIZZA = 3029
    SUN = 3030
    PARTY = 3031
    CAKE = 3032
    HEART = 3033
    THUMBS_UP = 3034
    PEACE = 3035
    TAXI = 3036
    ADMIN = 3039
    MIKTOK = 3040


class MiktokSafeChat(IntEnum):
    """Miktok safe chat message IDs - predefined emojies and messages (Hebrew)."""

    # Not fully mapped yet.
    SMILE = 100


ROOM_IDS: dict[str, int] = {
    "game_lobby": 1,
    "lobby": 2,
    "beach": 3,
    "city": 4,
    "jungle": 5,
    "jungle1": 6,
    "jungle2": 7,
    "forest": 8,
    "club": 9,
    "park": 10,
    "island": 11,
    "submarine": 12,
    "city_store": 13,
    "forest_store": 14,
    "arcade": 15,
    "dance": 16,
    "forest_maze": 17,
    "mikea": 18,
    "coffeeshop": 19,
    "fashion_store": 20,
    "carnaval": 21,
    "permaid": 22,
    "contest": 23,
    "cave": 24,
    "trivia_lab": 25,
    "volcano": 26,
    "rank2": 27,
    "rank3": 28,
    "football": 29,
    "lockerroom": 30,
    "mountentrance": 31,
    "candystore": 32,
    "candyfactory": 33,
    "sewer": 34,
    "meteor": 35,
    "muze_out": 36,
    "city_trade_lobby": 37,
    "clearing": 38,
    "theater_lobby": 39,
    "studio_lobby_1": 40,
    "sampler_lobby": 41,
    "superheroes": 42,
    "racingtrack": 43,
    "space_room": 44,
    "space_lobby": 45,
    "space_from_map": 46,
    "rank4": 47,
    "city2": 48,
    "cityhall": 49,
    "lab_outside": 50,
    "lab_inside": 51,
    "mazeroom_1": 52,
    "mazeroom_2": 53,
    "mazeroom_3": 54,
    "mazeroom_4": 55,
    "mazeroom_5": 56,
    "mazeroom_6": 57,
    "mazeroom_7": 58,
    "mazeroom_8": 59,
    "mazeroom_9": 60,
    "mazeroom_10": 61,
    "mazeroom_11": 62,
    "mazeroom_12": 63,
    "mazeroom_13": 64,
    "mazeroom_14": 65,
    "mazeroom_15": 66,
    "mazeroom_16": 67,
    "mazeroom_17": 68,
    "mazeroom_18": 69,
    "mazeroom_19": 70,
    "mazeroom_20": 71,
    "mazeroom_21": 72,
    "mazeroom_22": 73,
    "mazeroom_23": 74,
    "mazeroom_24": 75,
    "mazeroom_25": 76,
    "treasureroom": 77,
    "studio_lobby_2": 78,
    "magic_room": 79,
    "dolls_lobby": 80,
    "room_doll_max": 81,
    "room_doll_zoe": 82,
    "room_doll_jimbo": 83,
    "room_doll_sunny": 84,
    "paintball": 85,
    "sports_lobby": 86,
    "sports_shop": 87,
    "archive_room": 88,
    "bank": 89,
    "tent": 90,
    "billboard": 91,
    "rank5": 92,
    "game_center": 93,
    "mind": 94,
    "sail": 95,
    "lostship": 96,
    "seabottom": 97,
    "shipwreck": 98,
    "mindbattle2": 99,
    "m_old_park": 100,
    "m_valantine": 101,
    "m_old_city": 102,
    "m_watertower": 103,
    "m_carnaval2010": 104,
    "m_snow": 105,
    "m_fireplace": 106,
    "m_hanuka": 107,
    "m_darkness": 108,
    "m_superheroes": 109,
    "m_p_jungle2012": 110,
    "m_p_forest2012": 111,
    "m_p_club2012": 112,
    "m_clearing_plane": 113,
    "m_city_elections": 114,
    "m_luanch_room": 115,
    "m_cinema_building": 116,
    "m_island_rain": 117,
    "m_trampolina": 118,
    "m_star_wars": 119,
    "room_doll_rainy": 120,
    "room_doll_elvis": 121,
    "room_doll_mondo": 122,
    "room_doll_fancy": 123,
    "room_doll_mondo_s": 124,
    "room_doll_elvis_s": 125,
    "rank6": 126,
    "mountain_car_race": 127,
    "star_wars": 128,
    "room_doll_axel": 129,
    "room_doll_mayor": 130,
    "room_doll_mikyavelli": 131,
    "room_doll_alexis": 132,
    "room_mikcafe_library": 133,
    "water_park": 134,
    "diner": 135,
    "balcony": 136,
    "rank7": 137,
    "room_doll_snooz": 138,
    "forest_maze_lev2": 139,
    "museum_pics": 140,
    "museum_statues": 141,
    "backyard": 142,
    "woods1": 143,
    "woods2": 144,
    "woods3": 145,
    "woods4": 146,
    "woods5": 147,
    "woods6": 148,
    "woods7": 149,
    "woods8": 150,
    "woods9": 151,
    "woods10": 152,
    "woods11": 153,
    "woods12": 154,
    "woods13": 155,
    "woods14": 156,
    "woods15": 157,
    "woods16": 158,
    "woods17": 159,
    "woods18": 160,
    "woods19": 161,
    "woods20": 162,
    "backyard_store": 163,
    "fantasy_pur": 164,
    "fair_lobby": 165,
    "fair": 166,
    "fair_wheel": 167,
    "fair_wheel_ride": 168,
    "rank8": 169,
    "under_water": 170,
    "zeppelin": 171,
    "las_vegas": 172,
    "japan": 173,
    "paris": 174,
    "ballon_fly": 175,
    "vegas_machine": 176,
    "football_new": 177,
    "sports_shop_mondial": 178,
    "limo_promeroom": 179,
    "cityhall_f2": 180,
    "meteor_f2": 181,
    "mall_f1": 182,
    "mall_f2": 183,
    "ma_hom": 184,
    "ma_sp1": 185,
    "ma_sp2": 186,
    "ma_elc": 187,
    "ma_hir": 188,
    "ma_phn": 189,
    "ma_acs": 190,
    "rank9": 191,
    "mikloyada": 192,
    "carnaval2": 193,
    "movie_lobby": 194,
    "movie_cave": 195,
    "movie_underwater": 196,
    "ma_half": 197,
    "choclate": 198,
    "spng_krusty_krab": 199,
    "spng_bikini_bottom": 200,
    "rank10": 201,
    "ma_upgrades": 202,
    "hanuka_room": 203,
    "caribbean": 204,
    "jet_sail": 205,
    "ma_gucci": 206,
    "rank1": 207,
    "suk_space_lobby": 208,
    "suk_caffe": 209,
    "suk_store": 210,
    "suk_football": 211,
    "italy": 212,
    "post_office": 213,
    "snow_lobby": 214,
    "pesach_rare": 215,
    "ma_hom2": 216,
    "survivor_red": 217,
    "survivor_blue": 218,
    "kamping": 219,
    "park_new": 220,
    "manag_week": 221,
    "bd_city2": 222,
    "bd_city_6": 223,
    "bd_clearing": 224,
    "bd_club": 225,
    "bd_jungle": 226,
    "bd_island": 227,
    "bd_beach": 228,
    "flash_room": 229,
    "bat_room": 230,
    "wonder_room": 231,
    "cyborg_room": 232,
    "escape_lab": 233,
    "escape_pyramid": 234,
    "escape_mayor": 235,
    "love_prome": 236,
    "esca_caffe": 237,
    "bit_shopcenter": 238,
    "bit_carshop": 239,
    "bit_studioshop": 240,
    "bit_studiofloor": 241,
    "bit_vault": 242,
    "esc_library": 243,
    "pesach_maze01": 244,
    "pesach_maze02": 245,
    "pesach_maze03": 246,
    "pesach_maze04": 247,
    "winter_games": 248,
    "pesach_maze05": 249,
    "train": 250,
    "gwheel_lobby": 251,
    "giant_wheel": 252,
    "water_park2": 253,
    "snow_city": 254,
    "snow_city2": 255,
    "snow_forest": 256,
    "snow_laboutside": 257,
    "camping": 258,
    "esc_cyborg_2": 259,
    "esc_flash_2": 260,
    "esc_wonder_2": 261,
    "esc_bat_2": 262,
    "newyork": 263,
    "subway": 264,
    "mexico": 265,
    "hawaii": 266,
    "esc_bd10": 267,
    "hanuka_room19": 268,
    "mikraft_room": 269,
    "train_reg": 270,
    "train_west": 271,
    "train_future": 272,
    "class_hebrew": 273,
    "class_science": 274,
    "class_geo": 275,
    "class_show": 276,
    "class_loby": 277,
    "millionaire": 278,
    "esc_jungle": 279,
    "motivation": 280,
    "esc_bd11": 281,
    "planet1": 282,
    "planet2": 283,
    "dubai1": 284,
    "dubai2": 285,
    "event_room": 286,
    "esc_egypt": 287,
    "stage": 288,
    "event_room2": 289,
}

# Reverse lookup: Room ID -> Room name
ROOM_NAMES: dict[int, str] = {v: k for k, v in ROOM_IDS.items()}


# Result class for functions that can return either a value or an error message. (mostly used for parsing functions)
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    ok: bool
    value: Optional[T] = None
    error: Optional[str] = None
