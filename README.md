# mikmakpy

A Python client library for the MikMak 1 game protocol.

Handles the full login flow — handshake, server list, server switch, game-server authentication, and room join — so you can focus on building bots, tools, or whatever you want on top of it.

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

## Events

| Event | Args | When |
|-------|------|------|
| `server_list` | `list[dict]` | Server list received (1st connection) |
| `room_list` | `list[dict]` | Room list received (2nd connection) |
| `login_res` | `dict` | Login response from game server |
| `achievement_res` | `list[dict]`, `bool` | Achievements + is_update flag |
| `message` | `str` | Every raw message (both connections) |

## Logger levels

Pass a set of `LoggerLevel` values to control output:

| Level | Shows |
|-------|-------|
| `INCOMING` | All messages from server |
| `OUTGOING` | All messages sent |
| `CONNECTION_CHANGE` | Connect/disconnect/switch events |
| `PARSING_ERROR` | Parse failures |
| `INTERNAL_ERROR` | Connection errors |

## Compatibility

- Should work on any Python 3 version. If it doesn't, open an issue.
- Developed on Python 3.14.3
- No runtime dependencies

## License

GPLv3
