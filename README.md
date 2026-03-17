# mikmakpy

A Python client library for the MikMak 1 game protocol.

Handles the full login flow — handshake, server list, server switch, game-server authentication, and room join — plus in-game state tracking and actions, so you can focus on building bots, tools, or whatever you want on top of it.

## Install

Not there yet, might be!
```bash
pip install mikmakpy
```

Or from source:

```bash
git clone https://github.com/IsaacAber/mikmakpy.git
cd mikmakpy
pip install .
```

## Quick start

### Login only

```python
from mikmakpy.login import MikmakLoginClient
from mikmakpy.constants import LoggerLevel, Server

client = MikmakLoginClient(
    username="your_username",
    password="your_password",
    server_to_join=Server.KIWI,
    logger_levels={LoggerLevel.CONNECTION_CHANGE},
)

@client.on("server_list")
def on_servers(servers):
    print("Servers:", [s["name"] for s in servers])

@client.on("message")
def on_message(msg):
    print("Raw:", msg[:100])

client.connect()  # blocks until disconnected
```

Set `server_to_join=None` to stop after receiving the server list without joining a game server.

### In-game client

```python
from mikmakpy.ingame import MikmakIngameClient
from mikmakpy.constants import LoggerLevel, Server, SafeChat, SafeChatEmoji

client = MikmakIngameClient(
    username="your_username",
    password="your_password",
    server_to_join=Server.KIWI,
    logger_levels={LoggerLevel.CONNECTION_CHANGE, LoggerLevel.ACTION_WARNING},
)

@client.on("room_join")
def on_join(data):
    print(f"Joined room {data['room_id']} with {len(data['users'])} users")
    client.action.move(500, 400)

@client.on("user_enter")
def on_enter(user):
    print(f"{user['username']} entered the room")

@client.on("user_leave")
def on_leave(session_id, user):
    if user:
        print(f"{user['username']} left")

@client.on("user_update")
def on_update(data):
    print(f"Session {data['session_id']} updated: {data['updated']}")

@client.on("user_chat_safe")
def on_safe_chat(sender, msg_id):
    print(f"{sender} sent safe chat ID: {msg_id}")

@client.on("user_chat_unsafe")
def on_unsafe_chat(sender, text):
    print(f"{sender}: {text}")

client.connect()
```

## Events

### Login events (`MikmakLoginClient`)

| Event | Args | When |
|-------|------|------|
| `server_list` | `list[dict]` | Server list received (1st connection) |
| `room_list` | `list[dict]` | Room list received (2nd connection) |
| `login_res` | `dict` | Login response from game server |
| `achievement_res` | `list[dict]`, `bool` | Achievements + is_update flag |
| `message` | `str` | Every raw message (both connections) |

### In-game events (`MikmakIngameClient`)

| Event | Args | When |
|-------|------|------|
| `room_join` | `dict` | Joined a room (`room_id`, `room_vars`, `users`) |
| `user_enter` | `dict` | A user entered the room |
| `user_leave` | `int`, `dict\|None` | A user left (session_id, last known user object or None) |
| `user_update` | `dict` | A user's vars changed (`session_id`, `updated`, `unparsed`) |
| `user_chat_safe` | `str`, `int` | A user sent a safe chat message (sender, msg_id) |
| `user_chat_unsafe` | `str`, `str` | A user sent an unsafe chat message (sender, text) |

## Actions

`MikmakIngameClient` provides `client.action.*` methods:

| Method | Args | Description |
|--------|------|-------------|
| `move` | `x, y, instant=False` | Move to position. `instant=True` teleports. |
| `safe_chat` | `msg_id` | Send a safe chat message (accepts `SafeChat`, `SafeChatEmoji`, `MiktokSafeChat` enums or raw `int`) |
| `unsafe_chat` | `msg` | Send a free-text chat message (validated: max 34 chars, A-z/א-ת/.!? only) |

## User lookups

`MikmakIngameClient` provides user lookup methods on the current room's user list:

| Method | Args | Returns |
|--------|------|---------|
| `get_user_by_user_id` | `user_id: int` | `dict \| None` |
| `get_user_by_session_id` | `session_id: int` | `dict \| None` |
| `get_user_by_nickname` | `nickname: str` | `dict \| None` |

## Logger levels

Pass a set of `LoggerLevel` values to control output:

| Level | Shows |
|-------|-------|
| `INCOMING` | All messages from server |
| `OUTGOING` | All messages sent |
| `CONNECTION_CHANGE` | Connect/disconnect/switch events |
| `PARSING_ERROR` | Parse failures |
| `INTERNAL_ERROR` | Connection errors |
| `ACTION_WARNING` | Validation warnings from actions (e.g. chat too long) |
| `SERVER_DENY` | Server denial messages |

## Compatibility

- Should work on any Python 3 version. If it doesn't, open an issue.
- Developed on Python 3.14.3
- No runtime dependencies

## License

GPLv3
