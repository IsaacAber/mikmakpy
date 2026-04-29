"""
Waiter bot — follows anyone who says "מלצר" in chat.
Keeps 64px distance and stays within screen bounds (1200×800).
"""

import math
from mikmakpy.ingame import MikmakIngameClient
from mikmakpy.constants import LoggerLevel, Server, ROOM_NAMES

SCREEN_W, SCREEN_H, FOLLOW_DISTANCE = 1200, 800, 64

client = MikmakIngameClient(
    username="your_username",
    password="your_password",
    server_to_join=Server.KIWI,
    logger_levels={LoggerLevel.ACTION_WARNING, LoggerLevel.CONNECTION_CHANGE},
)

following = None  # session_id of the user we're following


@client.on("room_join")
def on_join(data):
    global following
    following = None
    print(f"Joined room {ROOM_NAMES.get(data['room_id'], data['room_id'])} with {len(data['users'])} users")


@client.on("user_chat_unsafe")
def on_chat(sender, text):
    global following
    if "מלצר" in text and (user := client.get_user_by_nickname(sender)):
        following = user["session_id"]
        print(f"Now following {sender} (session {following})")
        move_toward(user)
    if text.startswith("בוא"):
        dest = text[len("בוא"):].strip()
        {"עיר": lambda: client.action.warp("city"), "קרחת היער": lambda: client.action.warp("clearing"), "הביתה": client.disconnect}.get(dest, lambda: None)()


@client.on("user_update")
def on_update(data):
    if data["session_id"] != following or "position" not in data.get("updated", {}): return
    if user := client.get_user_by_session_id(following): move_toward(user)


@client.on("user_leave")
def on_leave(session_id, user):
    global following
    if session_id == following:
        following = None
        print(f"Stopped following {user.get('nickname', session_id)} (left)")


def move_toward(target):
    if not (pos := target.get("position")) or len(pos) < 2: return
    tx, ty = pos
    me = client.get_user_by_session_id(client.ingame_state["session_id"])
    if not me or not me.get("position"):
        client.action.move(clamp(tx, SCREEN_W), clamp(ty, SCREEN_H))
        return
    mx, my = me["position"]
    dist = math.hypot(dx := tx - mx, dy := ty - my)
    if dist <= FOLLOW_DISTANCE: return
    r = (dist - FOLLOW_DISTANCE) / dist
    client.action.move(clamp(int(mx + dx * r), SCREEN_W), clamp(int(my + dy * r), SCREEN_H))


def clamp(v, limit): return max(0, min(v, limit))


client.connect()