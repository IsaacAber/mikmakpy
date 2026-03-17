"""
Waiter bot — follows anyone who says "מלצר" in chat.
Keeps 64px distance and stays within screen bounds (1200×800).
"""

from dotenv import load_dotenv
from os import getenv
import math

from mikmakpy.ingame import MikmakIngameClient
from mikmakpy.constants import LoggerLevel, Server

SCREEN_W = 1200
SCREEN_H = 800
FOLLOW_DISTANCE = 64

load_dotenv()

client = MikmakIngameClient(
    username=getenv("USERNAME"),
    password=getenv("PASSWORD"),
    server_to_join=Server.KIWI,
    logger_levels={LoggerLevel.CONNECTION_CHANGE, LoggerLevel.ACTION_WARNING},
)

following: dict[str, int] = {}  # sender name -> session_id


@client.on("room_join")
def on_join(data):
    following.clear()
    print(f"Joined room {data['room_id']} with {len(data['users'])} users")


@client.on("user_chat_unsafe")
def on_chat(sender, text):
    if "מלצר" in text:
        user = client.get_user_by_nickname(sender)
        if user:
            following[sender] = user["session_id"]
            print(f"Now following {sender} (session {user['session_id']})")
            move_toward(user)

    if text.startswith("בוא"):
        destination = text[len("בוא"):].strip()
        print(f"Received warp command to {destination} from {sender}")
        if destination == "עיר":
            client.action.warp("city")
        elif destination == "קרחת היער":
            client.action.warp("clearing")
        elif destination == "הביתה":
            print("Going home — disconnecting!")
            client.disconnect()


@client.on("user_update")
def on_update(data):
    session_id = data["session_id"]
    if session_id not in following.values():
        return
    if "position" not in data.get("updated", {}):
        return
    user = client.get_user_by_session_id(session_id)
    if user:
        move_toward(user)


@client.on("user_leave")
def on_leave(session_id, user):
    to_remove = [name for name, sid in following.items() if sid == session_id]
    for name in to_remove:
        del following[name]
        print(f"Stopped following {name} (left)")


def move_toward(target_user):
    pos = target_user.get("position")
    if not pos or len(pos) < 2:
        return

    tx, ty = pos
    my_user = client.get_user_by_session_id(client.ingame_state["session_id"])
    if not my_user or not my_user.get("position"):
        client.action.move(clamp_x(tx), clamp_y(ty))
        return

    mx, my = my_user["position"]
    dx = tx - mx
    dy = ty - my
    dist = math.hypot(dx, dy)

    if dist <= FOLLOW_DISTANCE:
        return

    # Move to FOLLOW_DISTANCE away from target
    ratio = (dist - FOLLOW_DISTANCE) / dist
    nx = mx + dx * ratio
    ny = my + dy * ratio

    client.action.move(clamp_x(int(nx)), clamp_y(int(ny)))


def clamp_x(x):
    return max(0, min(x, SCREEN_W))


def clamp_y(y):
    return max(0, min(y, SCREEN_H))


client.connect()
