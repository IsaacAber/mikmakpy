"""
MikMak CLI — Interactive Shell
─────────────────────────────
A colorful interactive shell for MikMak, supporting login, movement, chat,
emotes, and room navigation. Credentials are loaded from creds.json.

This version keeps the prompt live: async game events print above the current
input line and the prompt redraws afterward. It also adds basic RTL-friendly
formatting for Hebrew output, plus readline tab completion for commands,
rooms, usernames, and emotes.
"""

import sys
import json
import re
import readline  # keeps input editing/history/completion on supported terminals
import threading
from pathlib import Path
from difflib import get_close_matches

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from mikmakpy.constants import (  # noqa: E402
    LoggerLevel,
    Server,
    SafeChat,
    SafeChatEmoji,
    EmoteFace,
    Dance,
    ROOM_IDS,
    ROOM_NAMES,
)
from mikmakpy.ingame import MikmakIngameClient  # noqa: E402

CREDS_PATH = Path(__file__).parent / "creds.json"
ANSI_CLEAR_LINE = "\r\033[2K"
RTL_RE = re.compile(r"[\u0590-\u05FF]")
FSI = "\u2068"  # First Strong Isolate
PDI = "\u2069"  # Pop Directional Isolate
EMOTE_ENUMS = (SafeChatEmoji, SafeChat, EmoteFace, Dance)
COMMANDS = ("move", "go", "chat", "emote", "help", "exit", "quit")


# --- Color helpers ---
def c(text, color, attrs=None):
    try:
        from termcolor import colored

        return colored(str(text), color, attrs=attrs)
    except ImportError:
        return str(text)


def info(msg):
    print(c("[INFO]", "cyan"), msg)


def warn(msg):
    print(c("[WARN]", "yellow", ["bold"]), msg)


def error(msg):
    print(c("[ERROR]", "red", ["bold"]), msg)


def event(msg):
    print(c("[EVENT]", "magenta", ["bold"]), msg)


def user_action(msg):
    print(c("[USER]", "green", ["bold"]), msg)


# --- Text helpers ---
def has_rtl(text: str) -> bool:
    return bool(RTL_RE.search(text))


def rtl_segment(text) -> str:
    """
    Wrap dynamic segments in directional isolates so mixed LTR/RTL output
    (English prompt labels + Hebrew usernames/messages) renders more sanely in
    common terminals.
    """
    text = str(text)
    if not text or not has_rtl(text):
        return text
    return text[::-1] 


# --- Credential loading ---
def load_creds():
    if not CREDS_PATH.exists():
        template = {"username": "your_username", "password": "your_password"}
        with open(CREDS_PATH, "w", encoding="utf-8") as f:
            json.dump(template, f, indent=2)
        error(
            f"creds.json not found. A template has been created at {CREDS_PATH}. "
            "Please edit it and rerun."
        )
        sys.exit(1)

    with open(CREDS_PATH, encoding="utf-8") as f:
        creds = json.load(f)

    if not creds.get("username") or not creds.get("password"):
        error("creds.json must contain 'username' and 'password'")
        sys.exit(1)

    return creds["username"], creds["password"]


# --- Fuzzy helpers ---
def fuzzy_enum(enum_cls, query):
    names = [e.name for e in enum_cls]
    matches = get_close_matches(query.upper(), names, n=1, cutoff=0.5)
    if matches:
        return getattr(enum_cls, matches[0])

    try:
        val = int(query)
        return enum_cls(val)
    except Exception:
        return None


def fuzzy_room(query):
    names = list(ROOM_IDS.keys())
    matches = get_close_matches(query.lower(), names, n=1, cutoff=0.5)
    if matches:
        return matches[0], ROOM_IDS[matches[0]]

    try:
        rid = int(query)
        if rid in ROOM_NAMES:
            return ROOM_NAMES[rid], rid
    except Exception:
        pass

    return None, None


def fuzzy_choices(query, choices, limit=12, cutoff=0.35):
    choices = list(dict.fromkeys(str(choice) for choice in choices if str(choice)))
    if not choices:
        return []
    if not query:
        return sorted(choices)[:limit]

    q = query.lower()
    prefix = [choice for choice in choices if choice.lower().startswith(q)]
    contains = [
        choice for choice in choices if q in choice.lower() and choice not in prefix
    ]

    upper_map = {choice.upper(): choice for choice in choices}
    fuzzy_upper = get_close_matches(
        query.upper(), list(upper_map), n=limit, cutoff=cutoff
    )
    fuzzy = [
        upper_map[key]
        for key in fuzzy_upper
        if upper_map[key] not in prefix and upper_map[key] not in contains
    ]

    return (prefix + contains + fuzzy)[:limit]


def resolve_emote(query):
    for enum_cls in EMOTE_ENUMS:
        emote = fuzzy_enum(enum_cls, query)
        if emote is not None:
            return emote
    return None


def emote_name(emote_id):
    for enum_cls in EMOTE_ENUMS:
        try:
            return enum_cls(emote_id).name
        except Exception:
            continue
    return str(emote_id)


def resolve_emote_name(query):
    query = str(query).strip()
    for enum_cls in EMOTE_ENUMS:
        emote = fuzzy_enum(enum_cls, query)
        if emote is not None:
            return emote
    return None


def parse_emote_query(query):
    query = str(query).strip()

    # raw numeric id: send as-is
    if re.fullmatch(r"[+-]?\d+", query):
        emote_id = int(query)
        named = resolve_emote_name(query)
        return emote_id, (named.name if named is not None else None)

    # string name: resolve only from enums
    named = resolve_emote_name(query)
    if named is None:
        return None, None
    return int(named.value), named.name


# --- CLI Shell ---
class MikmakShell:
    def __init__(self, client: MikmakIngameClient):
        self.client = client
        self.running = True
        self.username = (
            client._original_username
            if hasattr(client, "_original_username")
            else getattr(client, "username", "?")
        )
        self.coords = (0, 0)
        self.room_id = None
        self.room_name = None
        self.prompt = ""
        self._io_lock = threading.RLock()
        self._input_active = False
        self._setup_readline()
        self._update_prompt(initial=True)

    def _build_prompt(self):
        coords = f"{self.coords[0]},{self.coords[1]}" if self.coords else "?,?"
        room = self.room_name or (ROOM_NAMES.get(self.room_id) if self.room_id else "?")
        return c(f"{self.username}@{coords}:{room}$ ", "blue", ["bold"])

    def _setup_readline(self):
        try:
            readline.parse_and_bind("tab: complete")
            readline.set_completer_delims(" \t\n")
            readline.set_completer(self._complete)
            readline.set_completion_display_matches_hook(self._display_matches)
        except Exception:
            pass

    def _display_matches(self, substitution, matches, longest_match_length):
        with self._io_lock:
            if self._input_active:
                self._clear_current_line_locked()
            print()
            print("  " + "  ".join(matches), flush=True)
            self._redraw_input_locked()

    def _room_choices(self):
        return list(ROOM_IDS.keys()) + [str(room_id) for room_id in ROOM_NAMES]

    def _user_choices(self):
        users = self.client.ingame_state.get("users") or []
        return [str(user.get("username")) for user in users if user.get("username")]

    def _emote_choices(self):
        choices = []
        for enum_cls in EMOTE_ENUMS:
            choices.extend(member.name for member in enum_cls)
            choices.extend(str(int(member.value)) for member in enum_cls)
        return choices

    def _completion_candidates(self, buffer_text: str, text: str):
        stripped = buffer_text.lstrip()
        if not stripped or (" " not in stripped and not buffer_text.endswith(" ")):
            return fuzzy_choices(text, COMMANDS)

        parts = stripped.split()
        cmd = parts[0].lower()
        args = parts[1:]
        completing_new_arg = buffer_text.endswith(" ")

        if cmd == "go":
            return fuzzy_choices(text, self._room_choices())
        if cmd == "emote":
            return fuzzy_choices(text, self._emote_choices())
        if cmd == "help":
            return fuzzy_choices(text, COMMANDS)
        if cmd == "move" and (len(args) <= 1 or completing_new_arg):
            return fuzzy_choices(text, self._user_choices())
        return []

    def _complete(self, text, state):
        try:
            buffer_text = readline.get_line_buffer()
            matches = self._completion_candidates(buffer_text, text)
            return matches[state] if state < len(matches) else None
        except Exception:
            return None

    def _update_prompt(self, initial: bool = False):
        self.prompt = self._build_prompt()
        if not initial:
            self.refresh_input_line()

    def _clear_current_line_locked(self):
        sys.stdout.write(ANSI_CLEAR_LINE)
        sys.stdout.flush()

    def _redraw_input_locked(self):
        if not self._input_active:
            return
        buffer_text = readline.get_line_buffer()
        self._clear_current_line_locked()
        sys.stdout.write(self.prompt)
        sys.stdout.write(buffer_text)
        sys.stdout.flush()

    def refresh_input_line(self):
        with self._io_lock:
            self._redraw_input_locked()

    def _print_async(self, label: str, color: str, msg: str, attrs=None):
        with self._io_lock:
            if self._input_active:
                self._clear_current_line_locked()
            print(c(label, color, attrs), msg, flush=True)
            self._redraw_input_locked()

    def info(self, msg):
        self._print_async("[INFO]", "cyan", msg)

    def warn(self, msg):
        self._print_async("[WARN]", "yellow", msg, ["bold"])

    def error(self, msg):
        self._print_async("[ERROR]", "red", msg, ["bold"])

    def event(self, msg):
        self._print_async("[EVENT]", "magenta", msg, ["bold"])

    def user_action(self, msg):
        self._print_async("[USER]", "green", msg, ["bold"])

    def run(self):
        while self.running:
            try:
                with self._io_lock:
                    self._input_active = True
                    self._redraw_input_locked()
                line = input()
            except (EOFError, KeyboardInterrupt):
                print()
                self.running = False
                break
            finally:
                with self._io_lock:
                    self._input_active = False

            line = line.strip()
            if not line:
                continue

            self.handle_command(line)

    def handle_command(self, line):
        parts = line.split()
        if not parts:
            return

        cmd, *args = parts
        if cmd == "move":
            self.cmd_move(args)
        elif cmd == "go":
            self.cmd_go(args)
        elif cmd == "chat":
            self.cmd_chat(args)
        elif cmd == "emote":
            self.cmd_emote(args)
        elif cmd == "tp":
            self.info(rtl_segment(str(args[0])))
        elif cmd == "help":
            self.cmd_help(args)
        elif cmd in ("exit", "quit"):
            self.running = False
        elif cmd == "clear":
            with self._io_lock:
                self._clear_current_line_locked()
                print("\033[H\033[J", end="")  # ANSI clear screen
                self._redraw_input_locked()
        else:
            suggestions = fuzzy_choices(cmd, COMMANDS, limit=4)
            extra = ". Did you mean: " + ", ".join(suggestions) if suggestions else ""
            self.warn(f"Unknown command: {cmd}{extra}")

    def cmd_move(self, args):
        """
        move <x> <y>                     # Move to absolute coordinates
        move <username> <dist> <angle>  # Move to <dist> px at <angle> deg from <username>
        """
        import math

        if len(args) == 2:
            try:
                x, y = int(args[0]), int(args[1])
                self.client.action.move(x, y)
                self.info(f"Moving to ({x}, {y})")
            except Exception:
                self.error("Invalid coordinates")
        elif len(args) == 3:
            username, dist, angle = args[0], args[1], args[2]
            user = self.client.get_user_by_nickname(username)
            if not user or "position" not in user:
                self.warn(f"User not found or no position: {rtl_segment(username)}")
                suggestions = fuzzy_choices(username, self._user_choices(), limit=5)
                if suggestions:
                    self.info(
                        "Closest users: "
                        + ", ".join(rtl_segment(s) for s in suggestions)
                    )
                return
            try:
                dist = int(dist)
                angle = float(angle)
                ux, uy = user["position"]
                nx = int(ux + dist * math.cos(math.radians(angle)))
                ny = int(uy + dist * math.sin(math.radians(angle)))
                self.client.action.move(nx, ny)
                self.info(
                    f"Moving to {dist}px at {angle}° from {rtl_segment(username)} => ({nx}, {ny})"
                )
            except Exception:
                self.error("Invalid distance/angle")
        else:
            self.warn("Usage: move <x> <y> OR move <username> <distance> <angle>")
            self.info("Example: move 1200 800")
            self.info("Example: move mikmak2 32 90")

    def cmd_go(self, args):
        """
        go <room_id|room_name>  # Warp to a room (fuzzy search)
        """
        if not args:
            self.warn("Usage: go <room_id|room_name>")
            self.info("Example: go lobby")
            self.info("Example: go 3")
            return

        query = " ".join(args).strip()

        # direct numeric room id: send as-is
        if re.fullmatch(r"[+-]?\d+", query):
            rid = int(query)
            self.client.action.warp(rid)
            self.info(f"Warping to room id: {rid}")
            return

        # otherwise resolve by room name
        name, rid = fuzzy_room(query)
        if not name:
            suggestions = fuzzy_choices(query, self._room_choices(), limit=6)
            extra = ". Did you mean: " + ", ".join(suggestions) if suggestions else ""
            self.warn(f"Room not found: {rtl_segment(query)}{extra}")
            return

        self.client.action.warp(rid)
        self.info(f"Warping to room: {rtl_segment(name)} (id={rid})")

    def cmd_chat(self, args):
        """
        chat <text>  # Send unsafe chat message
        """
        if not args:
            self.warn("Usage: chat <text>")
            self.info("Example: chat hello world!")
            return

        msg = " ".join(args)
        self.client.action.unsafe_chat(msg)
        self.info(f"You: {rtl_segment(msg)}")

    def cmd_emote(self, args):
        """
        emote <id|name>  # Send any safe/face/dance emote
        """
        if not args:
            self.warn("Usage: emote <id|name>")
            self.info("Example: emote SMILE")
            self.info("Example: emote WAVE")
            self.info("Example: emote 3001")
            self.info("Example: emote 2001")
            return

        query = " ".join(args)
        emote_id, emote_label = parse_emote_query(query)
        if emote_id is None:
            suggestions = fuzzy_choices(query, self._emote_choices(), limit=6)
            extra = ". Did you mean: " + ", ".join(suggestions) if suggestions else ""
            self.warn(f"Emote not found: {rtl_segment(query)}{extra}")
            return

        self.client.action.safe_chat(emote_id)
        if emote_label:
            self.info(f"Emoted: {rtl_segment(emote_label)} ({emote_id})")
        else:
            self.info(f"Emoted ID: {emote_id}")

    def cmd_help(self, args):
        help_text = [
            c("Available commands:", "cyan", ["bold"]),
            c("  move <x> <y>", "yellow")
            + " — Move to absolute coordinates (ex: move 1200 800)",
            c("  move <username> <distance> <angle>", "yellow")
            + " — Move relative to user (ex: move mikmak2 32 90)",
            c("  go <room_id|room_name>", "yellow")
            + " — Warp to a room (ex: go lobby)",
            c("  chat <text>", "yellow")
            + " — Send unsafe chat (ex: chat hello world!)",
            c("  emote <id|name>", "yellow")
            + " — Send any safe/chat/face/dance emote (ex: emote SMILE, emote WAVE)",
            c("  help", "yellow") + " — Show this help message",
            c("  exit/quit", "yellow") + " — Exit the shell",
            c("Tab completion", "yellow")
            + " — Commands, rooms, users, and emotes autocomplete with Tab",
        ]
        with self._io_lock:
            if self._input_active:
                self._clear_current_line_locked()
            print("\n".join(help_text), flush=True)
            self._redraw_input_locked()


def register_event_handlers(shell: MikmakShell):
    client = shell.client

    @client.on("user_enter")
    def on_user_enter(user):
        shell.event(f"User entered: {rtl_segment(user.get('username', user))}")

    @client.on("user_leave")
    def on_user_leave(session_id, user):
        if user:
            shell.event(f"User left: {rtl_segment(user.get('username', user))}")
        else:
            shell.event(f"User left: session_id={session_id}")

    @client.on("user_chat_safe")
    def on_user_chat_safe(sender, emote_id):
        shell.user_action(
            f"{rtl_segment(sender)} emoted: {rtl_segment(emote_name(emote_id))}"
        )

    @client.on("user_chat_unsafe")
    def on_user_chat_unsafe(sender, msg):
        shell.user_action(f"{rtl_segment(sender)} says: {rtl_segment(msg)}")

    @client.on("room_join")
    def on_room_join(data):
        shell.room_id = data.get("room_id")
        shell.room_name = ROOM_NAMES.get(shell.room_id, str(shell.room_id))
        users = data.get("users", [])
        myuser = next((u for u in users if u.get("username") == shell.username), None)
        if myuser and "position" in myuser:
            shell.coords = myuser["position"]
        else:
            shell.coords = (0, 0)
        shell._update_prompt()
        shell.info(f"Joined room: {rtl_segment(shell.room_name)}")
        shell.info(
            "Users in room: "
            + (
                ", ".join(rtl_segment(u.get("username", "?")) for u in users)
                if users
                else ""
            )
        )

    @client.on("user_update")
    def on_user_update(data):
        if data.get("updated") and data.get(
            "session_id"
        ) == shell.client.ingame_state.get("session_id"):
            pos = data["updated"].get("position")
            if pos:
                shell.coords = pos
                shell._update_prompt()


def main():
    username, password = load_creds()
    client = MikmakIngameClient(
        username,
        password,
        logger_levels={LoggerLevel.ACTION_WARNING, LoggerLevel.CONNECTION_CHANGE},
        server_to_join=Server.KIWI,
    )
    info(f"Logging in as {username}...")

    shell = MikmakShell(client)
    register_event_handlers(shell)

    def connect_bg():
        try:
            client.connect()
        except Exception as e:
            shell.error(f"Connection error: {e}")

    threading.Thread(target=connect_bg, daemon=True).start()
    shell.run()


if __name__ == "__main__":
    main()
