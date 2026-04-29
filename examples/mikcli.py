"""
MikMak interactive shell — move, chat, emote, warp.
"""

import sys, json, re, math, threading
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from mikmakpy.constants import LoggerLevel, Server, SafeChat, SafeChatEmoji, EmoteFace, Dance, ROOM_IDS, ROOM_NAMES
from mikmakpy.ingame import MikmakIngameClient

CREDS_PATH  = Path(__file__).parent / "creds.json"
RTL_RE      = re.compile(r"[\u0590-\u05FF]")
EMOTE_ENUMS = (SafeChatEmoji, SafeChat, EmoteFace, Dance)
COMMANDS    = ["move", "go", "chat", "emote", "help", "exit", "quit", "clear"]

rtl = lambda t: t[::-1] if RTL_RE.search(t) else t

def load_creds():
    if not CREDS_PATH.exists():
        CREDS_PATH.write_text(json.dumps({"username": "", "password": ""}, indent=2))
        sys.exit("Fill creds.json first.")
    d = json.loads(CREDS_PATH.read_text())
    return d["username"], d["password"]

def resolve_room(q):
    if q.isdigit(): return int(q) if int(q) in ROOM_NAMES else None
    return ROOM_IDS.get(q)

def resolve_emote(q):
    if q.isdigit(): return int(q)
    for enum in EMOTE_ENUMS:
        for e in enum:
            if e.name == q.upper(): return int(e.value)
    return None


class MikmakCompleter(Completer):
    def __init__(self, shell): self.shell = shell

    def get_completions(self, document, complete_event):
        text  = document.text_before_cursor
        parts = text.split()
        arg   = parts[-1] if not text.endswith(" ") else ""

        if len(parts) <= 1 and not text.endswith(" "):
            for cmd in COMMANDS:
                if cmd.startswith(arg): yield Completion(cmd, -len(arg))
            return

        cmd = parts[0]
        if cmd == "go":
            for r in list(ROOM_IDS) + list(map(str, ROOM_NAMES)):
                if str(r).startswith(arg): yield Completion(str(r), -len(arg))
        elif cmd == "move":
            for u in self.shell.get_users():
                if u.startswith(arg): yield Completion(u, -len(arg))
        elif cmd == "emote":
            for enum in EMOTE_ENUMS:
                for e in enum:
                    if e.name.startswith(arg.upper()): yield Completion(e.name, -len(arg))


class MikmakShell:
    def __init__(self, client):
        self.client    = client
        self.coords    = (0, 0)
        self.room_name = "?"
        self.username  = client._original_username
        self.completer = MikmakCompleter(self)

    def prompt_str(self): return f"{self.username}@{self.coords[0]},{self.coords[1]}:{self.room_name}$ "
    def get_users(self):  return [u.get("username") for u in self.client.ingame_state.get("users") or [] if u.get("username")]

    def cmd_move(self, args):
        if len(args) == 2:
            try: x, y = int(args[0]), int(args[1]); self.client.action.move(x, y); print(f"Moving to {x},{y}")
            except: print("Invalid coords")
        elif len(args) == 3:
            user = self.client.get_user_by_nickname(args[0])
            if not user or "position" not in user: print("User not found"); return
            try:
                dist, angle = int(args[1]), float(args[2])
                ux, uy = user["position"]
                nx, ny = int(ux + dist * math.cos(math.radians(angle))), int(uy + dist * math.sin(math.radians(angle)))
                self.client.action.move(nx, ny); print(f"Moving relative => {nx},{ny}")
            except: print("Invalid move params")

    def cmd_go(self, args):
        if not args: print("Usage: go <room>"); return
        rid = resolve_room(args[0])
        if rid is None: print("Room not found"); return
        self.client.action.warp(rid); print(f"Warping to {rid}")

    def cmd_chat(self, args):
        if not args: return
        msg = " ".join(args); self.client.action.unsafe_chat(msg); print(f"You: {rtl(msg)}")

    def cmd_emote(self, args):
        if not args: return
        eid = resolve_emote(args[0])
        if eid is None: print("Invalid emote"); return
        self.client.action.safe_chat(eid); print(f"Emote: {eid}")

    def run(self):
        CMDS = {"move": self.cmd_move, "go": self.cmd_go, "chat": self.cmd_chat, "emote": self.cmd_emote}
        while True:
            try: line = prompt(self.prompt_str(), completer=self.completer)
            except (KeyboardInterrupt, EOFError): break
            if not (parts := line.strip().split()): continue
            cmd, *args = parts
            if cmd in CMDS: CMDS[cmd](args)
            elif cmd in ("exit","quit"): break
            elif cmd == "clear": print("\033[H\033[J", end="")
            elif cmd == "help":  print("Commands:", ", ".join(COMMANDS))
            else: print("Unknown command")
        print("Bye.")


def register_handlers(shell):
    c = shell.client

    @c.on("room_join")
    def _(data):
        shell.room_name = ROOM_NAMES.get(data.get("room_id"), str(data.get("room_id")))
        print(f"\nJoined {rtl(shell.room_name)}")

    @c.on("user_chat_unsafe")
    def _(sender, msg): print(f"\n{rtl(sender)}: {rtl(msg)}")


def main():
    u, p = load_creds()
    client = MikmakIngameClient(u, p, logger_levels={LoggerLevel.ACTION_WARNING}, server_to_join=Server.KIWI)
    shell  = MikmakShell(client)
    register_handlers(shell)
    threading.Thread(target=client.connect, daemon=True).start()
    shell.run()

if __name__ == "__main__":
    main()