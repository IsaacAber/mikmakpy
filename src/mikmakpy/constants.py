"""
mikmakpy.constants
─────────────────
Game constants and enums: server names, logger levels, emote/dance IDs,
safe-chat message IDs, and the Result type used throughout the library.
"""

from enum import IntEnum, StrEnum

# Result type — used by parse/decode functions to return a value or an error without exceptions.
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    ok: bool
    value: Optional[T] = None
    error: Optional[str] = None


class Server(StrEnum):
    """Servers available for auto-join after initial connection."""

    KIWI = "קיווי"
    KREMBO = "קרמבו"
    ADMINS = "מנהלים"


class LoggerLevel(StrEnum):
    """Log categories for the logger_levels set on MikmakLoginClient."""

    INCOMING = "incoming"
    CONNECTION_CHANGE = "connection_change"
    OUTGOING = "outgoing"
    PARSING_ERROR = "parsing_error"
    INTERNAL_ERROR = "internal_error"
    ACTION_WARNING = "action_warning"
    SERVER_DENY = "server_deny"


class EmoteFace(IntEnum):
    """Emote IDs (1000 series) - character expressions/animations."""

    # Row 1 (left to right)
    BLUSH_SMILE = 1005  # Blushing with smile
    COOL = 1006  # Sunglasses cool
    DEPRESSED = 1010  # Sad looking down depressed
    CRY = 1011  # Crying
    EVIL_SMILE = 1012  # Evil smile
    ANGRY = 1013  # Angry red face
    SICK = 1014  # Green sick face
    PARTY = 1015  # Party face with a party hat and blower
    QUESTINING = (
        1017  # Questioning with raised eyebrow and question marks above the head
    )
    # Row 2 (left to right)
    LOVE_CIRCLE = 1001  # Love face with a circle of hearts around the head
    SMILE = 1002  # Normal smile without teeth
    GRIN = 1003  # Grinning with teeth
    LOVE = 1007  # Love face with three hearts floating above the head and toungue sticking out
    SLEEPY = 1008  # Sleeping
    SHOCKED = 1009  # Shocked/surprised
    ANGEL = 1004  # Angel with halo
    SLEEPING = 1016  # Sleeping with Zzz above the head
    WINK = 1018  # Winking with a closed smile

    # who did this is such a weirdo!


class Dance(IntEnum):
    """Dance IDs (2000 series) - character dance/movement animations."""

    # Row 1 (top, left to right) Starting from the mikbits dance!
    MIKBIT_DANCE_1 = 2068  # Can't remember the name of the dance, feel free to rename it if you know it!
    MIKBIT_DANCE_2 = 2070  # Again, we do we have a gap? like the ID between 2068 and 2072 exist, but why they can't put them in some logical order? (not zigzag or inline or anything I can think of)
    MIKBIT_DANCE_3 = 2071
    OOPA_GANGAM_STYLE = 2030
    PYRAMID_LEVEL_UP = 2001
    KALINKA = 2002
    HEAD_NODDING = 2013  # Again, what about this gap? (They have crazy streak in breaking consistency with their dance/emote/ETC IDs)
    JUMP_AND_RAISE_LEFT_HAND = 2014
    JUMP_AND_ROTATE_360 = 2017  # It's a pain to write them one after another AI isn't that good, he has an observation of a kid in the age of 3 years old.
    # Row 2 (bottom, left to right)
    MIKBIT_DANCE_4 = 2073
    MIKBIT_ZOMBIE_5 = 2069
    MIKBIT_DANCE_6 = 2072
    NOT_SURE_PLUS_360_ROTATE_IN_THE_END = 2057
    FLOSS = 2003
    WAVE = 2004
    SPINING_ON_THE_HEAD_INFINITY = 2015
    KALINKA_PLUS_FLOSS = 2016
    SHY_UWU = 2026
    # Sitting directions (Clockwise from the top)
    SIT_UP = 2006
    SIT_UP_RIGHT = 2007
    SIT_RIGHT = 2009
    SIT_DOWN_RIGHT = 2012
    SIT_DOWN = 2011
    SIT_DOWN_LEFT = 2010
    SIT_LEFT = 2008
    SIT_UP_LEFT = 2005


class SafeChat(IntEnum):
    """Safe chat message IDs - predefined messages (Hebrew)."""

    # Tree-like layout (visual only):
    # GREETINGS(1), GOODBYE(15), FRIENDSHIP(29), JOIN_ME(43), QUESTIONS(53)
    # ANSWERS(73), GAMES(89), ENOUGH(100), I_LIKE(107), ACHIEVEMENTS(136)
    # UPGRADES(160), MISSIONS(167), TRADING(180)

    # +-- GREETINGS (שלום)
    GREETINGS = 1  # Parent menu
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

    # +-- GOODBYE (להתראות)
    GOODBYE = 15  # Parent menu
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

    # +-- FRIENDSHIP (חברות)
    FRIENDSHIP = 29  # Parent menu
    WANNA_BE_FRIENDS = 30  # רוצה להיות חבר שלי?
    SENT_FRIEND_REQUEST = 31  # שלחתי לך בקשת חברות
    FUN_BEING_FRIENDS = 33  # איזה כיף שאנחנו חברים
    FUN_PLAYING_WITH_YOU = 34  # כיף לי לשחק איתך
    PARTY_AT_MY_HOUSE = 35  # מסיבה בביתי

    # +-- JOIN_ME (הצטרף אליי)
    JOIN_ME = 43  # Parent menu
    COME_TO_MY_HOUSE = 44  # בוא/י לביתי
    JOIN_MY_GAME = 45  # הצטרף אליי למשחק
    JOIN_WORLD_TOUR = 46  # הצטרף אליי לסיבוב בעולם
    JOIN_MIKNION = 47  # הצטרף אליי למיקניון
    FOLLOW_ME = 48  # בוא/י אחרי

    # +-- QUESTIONS (שאלות)
    QUESTIONS = 53  # Parent menu
    WANNA_COME_WITH = 54  # רוצה לבוא איתי?
    WANNA_GO_SHOPPING = 55  # רוצה לבוא איתי לקניות?
    WANNA_GO_MIKNION = 56  # רוצה לבוא איתי למיקניון?
    WANNA_GO_MIKAFE = 57  # רוצה לבוא איתי למיקפה
    WHEN = 58  # Parent submenu
    WHEN_IS_YOUR_PARTY = 59  # מתי המסיבה שלך?
    WHEN_MEET_AGAIN = 60  # מתי ניפגש שוב?
    WHEN_YOU_COMING_BACK = 61  # מתי את/ה חוזר/ת?
    HOW_ARE_YOU = 62  # Parent submenu
    WHATS_UP = 63  # מה נשמע?
    WHATS_NEW = 64  # מה חדש?
    WHATS_HAPPENING = 65  # מה קורה?
    WHATS_MIKMAKKING = 66  # מה מתמקמק?
    IM_NEW_SHOW_AROUND = 67  # אני חדש– אתה יכול להכיר לי את העולם?
    READ_NEW_BLOG = 68  # קראת כבר את הבלוג החדש?!
    WHAT_WOULD_YOU_LIKE = 69  # מה תרצה להזמין?

    # +-- ANSWERS (תשובות)
    ANSWERS = 73  # Parent menu
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

    # +-- GAMES (משחקים)
    GAMES = 89  # Parent menu
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

    # +-- ENOUGH (מספיק)
    ENOUGH = 100  # Parent menu
    LEAVE_ME_ALONE = 101  # תניח לי בבקשה
    MOVING_TO_OTHER_AREA = 102  # אני עובר לאזור אחר
    NOT_COMFORTABLE = 103  # זה לא נעים לי
    NOT_NICE = 104  # זה לא נחמד
    UNFRIENDLY_BEHAVIOR = 105  # התנהגות לא חברית

    # +-- I_LIKE (אהבתי)
    I_LIKE = 107  # Parent menu
    NICE = 108  # יופי
    HOW_NICE = 109  # איזה יופי
    WELL_DONE = 110  # כל הכבוד!
    WONDERFUL = 111  # נהדר
    CONGRATS = 112  # Parent submenu
    CONGRATS_CLOTHES = 114  # תתחדש/י על הבגדים
    CONGRATS_HOUSE = 115  # תתחדש/י על הבית
    CONGRATS_FURNITURE = 116  # תתחדש/י על הרהיטים
    COOL_2 = 117  # מגניב
    ADORABLE = 123  # Parent submenu
    ADORABLE_CLOTHES = 124  # הבגדים שלך מקסימים
    ADORABLE_HOUSE = 125  # מקסים איך שעיצבת את הבית שלך
    PRETTIEST_MIKMAK = 126  # אתה המיקמק הכי יפה שראיתי
    CUTE_MIKMAK = 127  # איזה מיקמק חמוד
    STUNNING = 128  # מהמם
    MIKMAKKING_IT = 129  # מיקמקת אותה!

    # +-- ACHIEVEMENTS (הישגים)
    ACHIEVEMENTS = 136  # Parent menu
    LEVELED_UP = 137  # איזה כיף,עליתי רמה
    JOIN_ACHIEVEMENT_HILL = 138  # הצטרף אליי להר ההישגים
    HAVE_MANY_ACHIEVEMENTS = 139  # יש לי כבר מלא הישגים
    CONGRATS_ACHIEVEMENT = 140  # איזה כיף קיבלת הישג
    WHAT_LEVEL_ARE_YOU = 141  # באיזו דרגה את/ה?
    IM_LEVEL_FOUR = 142  # אני בדרגה רביעית
    IM_LEVEL_FIVE = 143  # אני בדרגה חמישית
    IM_LEVEL_TEN = 144  # אני בדרגה עשירית
    JOIN_ADMIN_SERVER = 145  # הצטרף אליי לשרת מנהלים (note: XML has duplicate id=144)

    # +-- UPGRADES (שדרוגים)
    UPGRADES = 160  # Parent menu
    GOT_NEW_UPGRADE = 161  # יש לך את השדרוג החדש?
    UNLOCK_TAXI = 162  # תפתחו מונית
    UNLOCK_JET_SKI = 163  # תפתח אופנוע ים
    UNLOCK_HELICOPTER = 159  # תפתח מסוק
    UNLOCK_SHIP = 189  # תפתח ספינה
    UNLOCK_YACHT = 131  # תפתח יאכטה (note: duplicate id with TRIVIA)
    UNLOCK_HEAD_TO_HEAD = 193  # תפתחו ראש בראש

    # +-- MISSIONS (משימות)
    MISSIONS = 167  # Parent menu
    WHERE_IS_FIRST = 168  # איפה הראשון?
    WHERE_IS_SECOND = 169  # איפה השני?
    WHERE_IS_THIRD = 170  # איפה השלישי?
    WHERE_IS_FOURTH = 171  # איפה הרביעי?
    WHERE_IS_LAST = 172  # איפה האחרון?
    FINISHED_MISSION = 173  # סיימתי את המשימה!
    NEW_MISSION = 174  # יש משימה חדשה!
    WHO_CAN_HELP = 175  # מי יכול לעזור לי?

    # +-- TRADING (החלפות)
    TRADING = 180  # Parent menu
    WANNA_TRADE = 181  # רוצה להחליף איתי?
    READY_TO_TRADE = 184  # אני מוכן/ה להחליף איתך
    ADD_MORE_ITEMS = 185  # הוסף עוד פריט
    CHANGE_ITEM_PLEASE = 186  # תחליף פריט בבקשה
    ALREADY_HAVE_ITEM = 187  # יש לי כבר את הפריט הזה
    ITEM_LOOKS_GREAT = 188  # הפריט הזה יראה מצוין בבית שלך
    I_APPROVED_TRADE = 190  # אני אישרתי את ההחלפה
    NOT_MY_TASTE = 191  # הפריט הזה לא לטעמי
    LOVELY_ITEM = 192  # איזה פריט מקסים!

    # +-- QUICK RESPONSES
    YES = 164  # כן
    NO = 165  # לא
    OK = 166  # OK


class SafeChatEmoji(IntEnum):
    """Emoji IDs (3000 series) - yellow smiley faces shown in chat bubble."""

    # Row 1
    SMILE = 3001
    LAUGH_TEETH_OUT = 3002
    UPSET_WITH_RAISED_EYEBROW = 3003
    SAD_LOOKING_DOWN = 3004
    WINK = 3005
    SHOCKED = 3006
    KISS = 3007
    SUPRISED = 3008
    FLUSHED_SMILE = 3009
    GRIMACING = 3010
    MAD_YELLOW = 3011
    RAISED_EYEBROW = 3012
    CLOSE_MOUTH_SMILING_EYES = 3013
    OPEN_MOUTH_SMILING_EYES = 3014
    NERD = 3015
    COOL_SUNGLASSES = 3016
    SMILE_TOUNGUE_OUT = 3017
    SMILING_EYES_TOUNGUE_OUT = 3018
    NERVE_PHEW_SMILE = 3019
    ADMIN_RANK_EMOJI = 3039
    # Row 2
    MAD_RED = 3020
    EVIL_SMILE = 3021
    NAUSEATED_GREEN = 3022
    SHOCKED_EYEBROW_RAISED = 3023
    SATISFIED_BLUSHED_SMILE = 3024
    HEARTS_IN_EYES = 3025
    SMILE_UPSIDE_DOWN = 3026
    SOBBING = 3027
    ANGEL = 3028
    RELIGIOUS_MAN = 3029
    COFFEE = 3030
    PIZZA_SLICE = 3031
    SUN = 3032
    CONFFETTI_CONE = 3033
    PARTY_CAKE = 3034
    HEART = 3035
    THUMBS_UP = 3036
    TAXI = 3037
    HANDS_UP = 3038
    MIKTOK_EMOJI = 3040
    

class MiktokSafeChat(IntEnum):
    """Miktok safe chat message IDs - predefined emojies and messages (Hebrew)."""
    # Ain't no way I'm iterating each of them and writing them down, there is more then 100+ of them!


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

ROOM_DEFAULT_SPAWN_POSITIONS: dict[int, tuple[int, int]] = dict(
    [
        (1, (560, 350)),
        (2, (450, 450)),
        (3, (340, 340)),
        (4, (558, 503)),
        (5, (346, 650)),
        (6, (885, 550)),
        (7, (800, 350)),
        (8, (550, 600)),
        (9, (600, 300)),
        (10, (540, 330)),
        (11, (385, 480)),
        (12, (480, 250)),
        (13, (480, 250)),
        (14, (890, 360)),
        (15, (600, 420)),
        (16, (600, 600)),
        (17, (720, 330)),
        (18, (1030, 260)),
        (19, (200, 400)),
        (20, (130, 750)),
        (21, (180, 420)),
        (22, (610, 550)),
        (23, (155, 277)),
        (24, (930, 350)),
        (25, (605, 131)),
        (26, (900, 450)),
        (27, (300, 680)),
        (28, (580, 620)),
        (29, (580, 250)),
        (30, (250, 330)),
        (31, (650, 330)),
        (32, (592, 210)),
        (33, (680, 429)),
        (34, (580, 620)),
        (35, (200, 680)),
        (36, (560, 205)),
        (37, (200, 680)),
        (38, (600, 650)),
        (39, (90, 280)),
        (41, (580, 630)),
        (42, (580, 630)),
        (43, (487, 400)),
        (44, (580, 630)),
        (45, (580, 630)),
        (46, (600, 400)),
        (48, (585, 580)),
        (49, (650, 590)),
        (50, (1155, 275)),
        (52, (180, 630)),
        (53, (950, 555)),
        (54, (1065, 665)),
        (55, (200, 700)),
        (56, (200, 700)),
        (57, (85, 334)),
        (58, (118, 669)),
        (59, (100, 260)),
        (60, (825, 187)),
        (61, (800, 550)),
        (62, (330, 390)),
        (63, (600, 400)),
        (64, (390, 600)),
        (65, (600, 260)),
        (66, (553, 700)),
        (67, (553, 700)),
        (68, (390, 600)),
        (69, (390, 600)),
        (70, (99, 590)),
        (71, (650, 330)),
        (72, (650, 330)),
        (73, (650, 330)),
        (74, (650, 330)),
        (75, (650, 330)),
        (76, (650, 330)),
        (77, (650, 330)),
        (78, (650, 330)),
        (79, (650, 330)),
        (80, (650, 330)),
        (81, (650, 330)),
        (82, (650, 330)),
        (83, (650, 330)),
        (84, (650, 330)),
        (85, (650, 330)),
        (86, (650, 330)),
        (87, (650, 330)),
        (88, (650, 330)),
        (89, (650, 330)),
        (90, (650, 330)),
        (91, (650, 330)),
        (92, (650, 330)),
        (93, (650, 330)),
        (94, (650, 330)),
        (95, (390, 600)),
        (96, (390, 600)),
        (97, (390, 600)),
        (98, (800, 700)),
        (99, (390, 600)),
        (700, (576, 507)),
        (701, (318, 468)),
        (702, (600, 400)),
        (703, (500, 600)),
        (704, (600, 400)),
        (705, (318, 468)),
        (706, (350, 400)),
        (707, (317, 574)),
        (708, (600, 400)),
        (709, (252, 506)),
        (710, (600, 400)),
        (711, (550, 600)),
        (712, (500, 600)),
        (713, (500, 600)),
        (714, (500, 600)),
        (715, (500, 600)),
        (716, (500, 600)),
        (717, (500, 600)),
        (718, (500, 600)),
        (719, (600, 600)),
        (720, (600, 600)),
        (721, (441, 350)),
        (722, (600, 600)),
        (723, (600, 600)),
        (724, (500, 600)),
        (725, (250, 365)),
        (726, (550, 550)),
        (727, (550, 550)),
        (728, (700, 550)),
        (729, (600, 600)),
        (800, (200, 200)),
        (801, (441, 350)),
        (802, (600, 600)),
        (803, (600, 600)),
        (804, (400, 200)),
        (805, (600, 600)),
        (806, (600, 600)),
        (807, (600, 600)),
        (808, (600, 600)),
        (809, (600, 600)),
        (810, (600, 600)),
        (811, (600, 600)),
        (812, (600, 600)),
        (813, (600, 600)),
        (814, (600, 600)),
        (815, (600, 600)),
        (816, (600, 600)),
        (817, (600, 600)),
        (818, (600, 600)),
        (819, (600, 600)),
        (820, (600, 600)),
        (821, (600, 600)),
        (822, (600, 600)),
        (823, (600, 600)),
        (824, (600, 600)),
        (825, (600, 600)),
        (826, (600, 600)),
        (827, (600, 600)),
        (900, (500, 600)),
        (901, (500, 600)),
        (902, (500, 600)),
        (903, (500, 600)),
        (904, (500, 600)),
        (905, (500, 600)),
        (906, (500, 600)),
        (907, (200, 700)),
        (908, (200, 700)),
        (909, (390, 480)),
        (910, (345, 680)),
        (911, (500, 600)),
        (912, (500, 600)),
        (913, (500, 600)),
        (914, (500, 600)),
        (915, (500, 600)),
        (916, (423, 481)),
        (917, (500, 600)),
        (918, (620, 684)),
        (919, (620, 684)),
        (920, (126, 620)),
        (921, (126, 620)),
        (922, (600, 400)),
        (923, (650, 600)),
        (924, (650, 600)),
        (925, (650, 600)),
        (926, (650, 600)),
        (927, (650, 600)),
        (928, (650, 600)),
        (929, (650, 600)),
        (930, (650, 600)),
        (931, (766, 350)),
        (932, (650, 600)),
        (933, (650, 600)),
        (934, (650, 600)),
        (935, (650, 600)),
        (936, (650, 600)),
        (937, (650, 600)),
        (938, (650, 600)),
        (939, (650, 600)),
        (940, (650, 600)),
        (941, (650, 600)),
        (942, (650, 600)),
        (943, (650, 600)),
        (944, (650, 600)),
        (945, (650, 600)),
        (946, (650, 600)),
        (947, (660, 540)),
        (949, (630, 660)),
        (950, (650, 600)),
        (951, (200, 700)),
        (952, (200, 700)),
        (953, (350, 500)),
        (954, (250, 450)),
        (955, (550, 550)),
        (956, (550, 550)),
        (957, (550, 550)),
        (958, (550, 550)),
        (959, (440, 110)),
        (960, (550, 550)),
        (961, (550, 550)),
        (962, (180, 450)),
        (963, (270, 720)),
        (964, (700, 500)),
        (965, (600, 600)),
        (966, (600, 450)),
        (967, (550, 550)),
        (969, (700, 400)),
        (970, (250, 580)),
        (971, (550, 550)),
        (972, (550, 550)),
        (973, (900, 380)),
        (974, (900, 380)),
        (976, (900, 380)),
        (978, (350, 500)),
        (979, (300, 700)),
        (980, (300, 700)),
        (981, (120, 500)),
        (982, (300, 700)),
        (983, (600, 600)),
        (984, (700, 500)),
        (985, (700, 500)),
        (986, (700, 500)),
        (987, (700, 500)),
        (988, (700, 500)),
        (989, (700, 500)),
        (990, (700, 500)),
        (991, (580, 642)),
        (992, (300, 600)),
        (993, (180, 720)),
        (994, (650, 600)),
        (996, (650, 600)),
        (997, (888, 648)),
        (998, (600, 500)),
        (999, (600, 500)),
        (1005, (600, 500)),
        (1006, (620, 90)),
        (1007, (350, 500)),
        (1008, (150, 620)),
        (1009, (650, 600)),
        (1014, (600, 600)),
        (1015, (350, 500)),
        (1016, (889, 158)),
        (1023, (700, 600)),
        (1024, (550, 500)),
        (1025, (550, 500)),
        (1026, (550, 500)),
        (1027, (550, 500)),
        (1028, (550, 500)),
        (1029, (700, 700)),
        (1030, (700, 700)),
        (1031, (700, 700)),
        (1032, (700, 700)),
        (1033, (700, 700)),
        (1034, (700, 700)),
        (1035, (700, 700)),
        (1036, (700, 700)),
        (1037, (700, 500)),
        (1040, (700, 700)),
        (1041, (700, 600)),
        (1042, (700, 500)),
        (1045, (700, 500)),
        (1046, (600, 600)),
        (1050, (700, 500)),
        (1052, (500, 700)),
        (1053, (700, 500)),
        (1054, (700, 500)),
        (1055, (700, 500)),
        (1056, (346, 650)),
        (1057, (441, 350)),
        (1058, (550, 600)),
        (1059, (390, 600)),
        (1060, (390, 600)),
        (1061, (390, 600)),
        (1062, (390, 600)),
        (1063, (390, 600)),
        (1064, (390, 600)),
        (1065, (390, 600)),
        (1066, (390, 600)),
        (1067, (390, 600)),
        (1068, (390, 600)),
        (1069, (390, 600)),
        (1070, (390, 600)),
        (4000, (99, 590)),
        (4001, (650, 330)),
        (4002, (650, 330)),
        (4003, (650, 330)),
        (4004, (650, 330)),
        (4005, (650, 330)),
        (4006, (650, 330)),
        (4007, (650, 330)),
        (4008, (650, 330)),
        (4009, (650, 330)),
        (4010, (650, 330)),
        (4011, (650, 330)),
        (4012, (650, 330)),
        (4013, (650, 330)),
        (4014, (650, 330)),
        (4015, (650, 330)),
        (4016, (650, 330)),
        (4017, (650, 330)),
        (4018, (650, 330)),
        (4019, (650, 330)),
        (4020, (650, 330)),
        (4021, (650, 330)),
        (4022, (650, 330)),
        (4023, (650, 330)),
        (4027, (650, 330)),
        (4029, (650, 620)),
        (4030, (650, 620)),
        (4031, (650, 620)),
        (4032, (650, 620)),
        (4033, (650, 620)),
        (4034, (600, 600)),
        (4035, (600, 600)),
        (4036, (600, 600)),
        (4037, (600, 600)),
        (4038, (600, 600)),
        (4039, (650, 330)),
        (4040, (300, 700)),
        (4041, (650, 330)),
        (4042, (650, 330)),
        (4043, (650, 330)),
        (4044, (650, 330)),
        (4045, (650, 330)),
        (4046, (650, 330)),
        (4047, (650, 330)),
        (50081, (650, 330)),
    ]
)

# user variables keys converted into normal format for cleaner access.
KNOWN_USER_VARS = {
    "d": ("age", int),
    "e": ("equipment", lambda v: list(map(int, v.split(",")))),
    "i": ("user_id", int),
    "l": ("rank", int),
    "x": ("position", lambda v: tuple(map(int, v.split(",")))),
}
