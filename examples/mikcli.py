import sys
import json
import re
import threading
from pathlib import Path

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from mikmakpy.constants import (
    LoggerLevel,
    Server,
    SafeChat,
    SafeChatEmoji,
    EmoteFace,
    Dance,
    ROOM_IDS,
    ROOM_NAMES,
)
from mikmakpy.ingame import MikmakIngameClient

CREDS_PATH = Path(__file__).parent / "creds.json"
RTL_RE = re.compile(r"[\u0590-\u05FF]")

EMOTE_ENUMS = (SafeChatEmoji, SafeChat, EmoteFace, Dance)
COMMANDS = ["move", "go", "chat", "emote", "help", "exit", "quit", "clear"]


# ---------- Helpers ----------

def has_rtl(text: str) -> bool:
    return bool(RTL_RE.search(text))


def rtl(text: str) -> str:
    if has_rtl(text):
        return text[::-1]
    return text


def load_creds():
    if not CREDS_PATH.exists():
        with open(CREDS_PATH, "w") as f:
            json.dump({"username": "", "password": ""}, f, indent=2)
        print("Fill creds.json first.")
        sys.exit(1)

    with open(CREDS_PATH) as f:
        data = json.load(f)

    return data["username"], data["password"]


def resolve_room(query):
    if query.isdigit():
        rid = int(query)
        return rid if rid in ROOM_NAMES else None

    for name, rid in ROOM_IDS.items():
        if name == query:
            return rid
    return None


def resolve_emote(query):
    if query.isdigit():
        return int(query)

    for enum in EMOTE_ENUMS:
        for e in enum:
            if e.name == query.upper():
                return int(e.value)
    return None


# ---------- Completer ----------

class MikmakCompleter(Completer):
    def __init__(self, shell):
        self.shell = shell

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        parts = text.split()

        # command completion
        if len(parts) <= 1 and not text.endswith(" "):
            for cmd in COMMANDS:
                if cmd.startswith(parts[0] if parts else ""):
                    yield Completion(cmd, start_position=-len(parts[0]) if parts else 0)
            return

        cmd = parts[0]
        arg = parts[-1] if not text.endswith(" ") else ""

        if cmd == "go":
            for r in list(ROOM_IDS.keys()) + list(map(str, ROOM_NAMES.keys())):
                if str(r).startswith(arg):
                    yield Completion(str(r), start_position=-len(arg))

        elif cmd == "move":
            for u in self.shell.get_users():
                if u.startswith(arg):
                    yield Completion(u, start_position=-len(arg))

        elif cmd == "emote":
            for enum in EMOTE_ENUMS:
                for e in enum:
                    name = e.name
                    if name.startswith(arg.upper()):
                        yield Completion(name, start_position=-len(arg))


# ---------- Shell ----------

class MikmakShell:
    def __init__(self, client):
        self.client = client
        self.running = True
        self.coords = (0, 0)
        self.room_id = None
        self.room_name = "?"
        self.username = client._original_username
        self.completer = MikmakCompleter(self)

    def prompt_str(self):
        return f"{self.username}@{self.coords[0]},{self.coords[1]}:{self.room_name}$ "

    def get_users(self):
        users = self.client.ingame_state.get("users") or []
        return [u.get("username") for u in users if u.get("username")]

    # ---------- Commands ----------

    def cmd_move(self, args):
        import math

        if len(args) == 2:
            try:
                x, y = int(args[0]), int(args[1])
                self.client.action.move(x, y)
                print(f"Moving to {x},{y}")
            except:
                print("Invalid coords")

        elif len(args) == 3:
            user = self.client.get_user_by_nickname(args[0])
            if not user or "position" not in user:
                print("User not found")
                return

            try:
                dist = int(args[1])
                angle = float(args[2])
                ux, uy = user["position"]

                nx = int(ux + dist * math.cos(math.radians(angle)))
                ny = int(uy + dist * math.sin(math.radians(angle)))

                self.client.action.move(nx, ny)
                print(f"Moving relative => {nx},{ny}")
            except:
                print("Invalid move params")

    def cmd_go(self, args):
        if not args:
            print("Usage: go <room>")
            return

        rid = resolve_room(args[0])
        if rid is None:
            print("Room not found")
            return

        self.client.action.warp(rid)
        print(f"Warping to {rid}")

    def cmd_chat(self, args):
        if not args:
            return
        msg = " ".join(args)
        self.client.action.unsafe_chat(msg)
        print(f"You: {rtl(msg)}")

    def cmd_emote(self, args):
        if not args:
            return

        eid = resolve_emote(args[0])
        if eid is None:
            print("Invalid emote")
            return

        self.client.action.safe_chat(eid)
        print(f"Emote: {eid}")

    # ---------- Loop ----------

    def run(self):
        while self.running:
            try:
                line = prompt(self.prompt_str(), completer=self.completer)
            except (KeyboardInterrupt, EOFError):
                break

            parts = line.strip().split()
            if not parts:
                continue

            cmd, *args = parts

            if cmd == "move":
                self.cmd_move(args)
            elif cmd == "go":
                self.cmd_go(args)
            elif cmd == "chat":
                self.cmd_chat(args)
            elif cmd == "emote":
                self.cmd_emote(args)
            elif cmd in ("exit", "quit"):
                break
            elif cmd == "clear":
                print("\033[H\033[J", end="")
            elif cmd == "help":
                print("Commands:", ", ".join(COMMANDS))
            else:
                print("Unknown command")

        print("Bye.")


# ---------- Events ----------

def register_handlers(shell):
    c = shell.client

    @c.on("room_join")
    def _(data):
        shell.room_id = data.get("room_id")
        shell.room_name = ROOM_NAMES.get(shell.room_id, str(shell.room_id))
        print(f"\nJoined {rtl(shell.room_name)}")

    @c.on("user_chat_unsafe")
    def _(sender, msg):
        print(f"\n{rtl(sender)}: {rtl(msg)}")


# ---------- Main ----------

def main():
    u, p = load_creds()

    client = MikmakIngameClient(
        u,
        p,
        logger_levels={LoggerLevel.ACTION_WARNING},
        server_to_join=Server.KIWI,
    )

    shell = MikmakShell(client)
    register_handlers(shell)

    threading.Thread(target=client.connect, daemon=True).start()
    shell.run()


if __name__ == "__main__":
    main()