# mikmakpy — AI Context

> **Keep this file up to date.** When you make architectural changes, add/remove
> modules, change the exception/connection strategy, or fix important bugs,
> update the relevant section below so future chats start with accurate context.

## What is this?

A Python client library for the MikMak 1 game protocol. Handles the full login
flow (handshake → server list → server switch → game-server login → room join)
and exposes an event bus so callers can react to server messages.

## Repo layout

```
src/mikmakpy/
  __init__.py        — public exports: protocol, MikmakLoginClient
  constants.py       — Result type, Server/LoggerLevel/EmoteFace/Dance/SafeChat enums
  events.py          — EventBus base class (@client.on decorator + emit)
  connection.py      — Low-level TCP socket wrapper (connect/send/listen/close)
  protocol.py        — encode (sys XML, xt JSON), decode (buffer split, JSON, XML),
                        parse (server_list, room_list, login_res, achievement_res, inv_list)
  login.py           — MikmakLoginClient (main class, extends EventBus)
  ingame.py          — MikmakIngameClient (subclass stub for post-login game messages)

src/tools/
  sniffer.py         — Packet sniffer tool (dev utility)
  packet.html        — Captured packet log (reference)

tests/
  login_test.py      — Integration tests (needs .env with USERNAME/PASSWORD)
  protocol_test.py   — Protocol parsing tests
```

## Architecture & key patterns

### Connection lifecycle (iterative, not recursive)

```
connect()                       ← blocks, try/finally ensures disconnect()
  while _running:
    _run()                      ← one TCP session (connect + listen)
    if _switching_servers → short delay, continue
    if retries exhausted → break
    else → increment retry, delay, continue
  finally: disconnect()
```

### Exception layers (who catches what)

| Layer | Catches | Purpose |
|-------|---------|---------|
| `connect()` finally | Everything (incl. KeyboardInterrupt) | Ensure socket cleanup on any exit |
| `_run()` except Exception + finally | TCP connect failures, broken socket | Log, always close, return to retry loop |
| `listen()` TimeoutError | Socket read timeout (10s settimeout) | Expected, just retry recv |
| `listen()` on_message except | Bug in message handler | Isolate so one bad message doesn't kill connection |
| `listen()` finally | — | Always close socket before returning |
| `send()` except | Write to dead socket | Fire-and-forget |
| `close()` except | Socket already gone | Defensive, idempotent |

- **No signal handlers.** Ctrl+C raises KeyboardInterrupt (BaseException), propagates
  naturally through recv/sleep, caught by `connect()`'s try/finally.

### Protocol flow (from packet captures)

**1st connection (login server):**
1. Server sends `<cross-domain-policy>` unsolicited on TCP connect
2. Client responds with `verChk`
3. Server sends `apiOK`
4. Client sends `login` (with hashed credentials)
5. Server sends `server_list` (xt JSON)

**2nd connection (game server):**
1. Client sends `verChk` immediately on connect (before any server message)
2. Server sends `<cross-domain-policy>` + `apiOK`
3. Client sends `login` (with `cluster_` prefix on password)
4. Server sends `rmList`, `login_res`, `achivment_res`
5. Client sends `avt_joinRoom`

### State

- `_is_first_connection` — flips to False after server switch
- `_switching_servers` — True between conn.close() and next _run()
- `_retry_count` — reset to 0 on successful game-server login (rmList)
- `ingame_state` dict — populated incrementally by message handlers

## Build & test

```bash
python3 -m pip install .          # install from source
python3 -m pytest -s              # run tests (needs .env)
./test.sh                         # shortcut (uses python3.14)
```

- Build system: setuptools + wheel
- No runtime dependencies
- Dev dependency: pytest
- Should work on any Python 3 version
- Developed on Python 3.14.3

## Past bugs & lessons learned

1. **Signal handler leak:** Don't use signal() for cleanup — stale handlers survive
   across test runs. Use try/finally instead.
2. **Recursive reconnect:** `_run → listen → _on_disconnect → _run` blows the stack
   with infinite retries. Use an iterative while loop.
3. **Double-close:** If listen() catches all exceptions AND the caller also catches,
   disconnect callbacks fire twice. Let listen() only catch expected errors
   (TimeoutError), let the rest propagate.
4. **Parse-error silent fallthrough:** `if not ok and LOGGER: return` only returns
   when logging is on. Always return on parse failure, log conditionally.
5. **Server switch via retry path:** Without a `_switching_servers` flag, planned
   server switches consume retries and sleep unnecessarily.
