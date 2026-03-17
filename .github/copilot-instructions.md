# mikmakpy — Copilot Instructions

## Project overview

mikmakpy is a Python client library for the MikMak 1 game protocol. It has zero runtime dependencies and targets Python 3.14+.

## Architecture

- **`constants.py`** — Enums (`Server`, `LoggerLevel`, `SafeChat`, `SafeChatEmoji`, `MiktokSafeChat`, `EmoteFace`, `Dance`), the `Result` dataclass, room ID mappings (`ROOM_IDS`, `ROOM_NAMES`, `ROOM_DEFAULT_SPAWN_POSITIONS`), and `KNOWN_USER_VARS` for parsing user var XML elements.
- **`protocol.py`** — Stateless encode/decode/parse classes:
  - `encode` — builds outgoing `sys` (XML) and `xt` (JSON) message strings.
  - `decode` — splits raw byte buffers, parses JSON (`xt`) and XML (`xml`).
  - `parse` — extracts structured data from specific server responses (server list, room list, login, achievements, inventory, joinOK, uVarsUpdate, uER, userGone).
- **`connection.py`** — Low-level TLS socket wrapper (`MikmakConnection`).
- **`login.py`** — `MikmakLoginClient` — event-driven client handling handshake, server list, server switch, authentication, and room join. Has a nested `_SendInternal` class accessed via `self._send` with `.raw()`, `.xt()`, `.sys()` methods.
- **`ingame.py`** — `MikmakIngameClient(MikmakLoginClient)` — extends with in-game state tracking (`ingame_state` dict: `room_id`, `room_vars`, `users`, `session_id`) and a nested `_ActionInternal` class accessed via `self.action` with `.move()`, `.safe_chat()`, `.unsafe_chat()` methods.
- **`events.py`** — Event emitter mixin used by the client classes.

## Conventions

- All parse/decode functions return `Result(ok, value, error)` — never raise exceptions.
- Incoming messages dispatch on `action` (XML sys messages) or `cmd` (JSON xt messages) in `_handle_game_messages`.
- Parsers live in `protocol.py` as `@staticmethod` methods on the `parse` class.
- Event handlers in `ingame.py` follow the pattern: parse → check ok → update `ingame_state` → `self.emit(event_name, ...)`.
- On parse failure, log via `LoggerLevel.PARSING_ERROR` and return early.
- On action validation failure, log via `LoggerLevel.ACTION_WARNING` and return early.
- User var parsing uses `KNOWN_USER_VARS` dict mapping short keys (e.g. `'x'`, `'e'`, `'d'`) to `(field_name, cast_function)` tuples.
- The protocol uses two message formats: XML (`<msg t='sys'>...`) for sys messages and JSON for xt messages.
- `ROOM_DEFAULT_SPAWN_POSITIONS` is a `dict[int, tuple[int, int]]` — use `.get(room_id, (0, 0))` for safe access.

## Testing

- Tests live in `tests/` and use pytest.
- Run tests: `python3.14 -m pip install . && python3.14 -m pytest tests/ -v`
- Test data samples can be found in `tests/modify.xml`.
- Each parser should have a corresponding test in `tests/protocol_test.py`.

## Style

- No runtime dependencies — stdlib only.
- Imports from the package use relative imports (e.g. `from .protocol import parse, decode`).
- Never use inline/local imports — all imports go at the top of the file.
- Keep code minimal and direct — no over-engineering.
