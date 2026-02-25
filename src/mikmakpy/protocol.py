"""
mikmakpy.protocol
─────────────────

"""
import ast
from json import dumps, loads
import re
from typing import Any

from .constants import Result

class encode:
    @staticmethod
    def raw(message: str) -> bytes:
        """Encode a string message for transmission (appends null terminator)."""
        return (message + "\x00").encode("utf-8")

    @staticmethod
    def xt(cmd: str, p: dict, x: str = "ExtManager", r: int = -1) -> str:
        """Build a raw xt JSON string."""
        return dumps(
            {"b": {"c": cmd, "p": p, "r": r, "x": x}, "t": "xt"},
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @staticmethod
    def sys(action: str, body: str, r: int = 0) -> str:
        """Build a raw sys XML string."""
        return f"<msg t='sys'><body action='{action}' r='{r}'>{body}</body></msg>"
    
class decode:
    @staticmethod
    def buffer(buffer: bytearray) -> Result[tuple[list[str], bytearray]]:
        """
        Split a raw byte buffer on null bytes.
        Returns (list_of_complete_messages, remaining_buffer).
        """
        messages = []
        while b"\x00" in buffer:
            msg_bytes, buffer = buffer.split(b"\x00", 1)
            try:
                messages.append(msg_bytes.decode("utf-8", errors="replace"))
            except Exception as e:
                return Result(ok=False, error=str(e))
        return Result(ok=True, value=(messages, buffer))

    @staticmethod
    def xt(msg: str) -> Result[dict]:
        """Try to parse a JSON xt message. Returns dict or None."""
        try:
            return Result(ok=True, value=loads(msg))
        except Exception as e:
            return Result(ok=False, error=str(e))
        
class parse:
    @staticmethod
    def jsish_list(s: str) -> Any:
        # JS literals -> Python literals so literal_eval can parse
        s = re.sub(r'\btrue\b', 'True', s)
        s = re.sub(r'\bfalse\b', 'False', s)
        s = re.sub(r'\bnull\b', 'None', s)
        return ast.literal_eval(s)

    @staticmethod
    def server_list(msg: str) -> Result[list[dict]]:
        """Parse the server list from a login response xt message. Returns list of dicts with server info."""
        data = decode.xt(msg)
        if not data.ok:
            return Result(ok=False, error=data.error)

        o = data.value.get("b", {}).get("o", {})
        raw_list = o.get("list")

        if not isinstance(raw_list, str) or not raw_list:
            return Result(ok=False, error="server_list: missing or invalid 'list' field")

        try:
            parsed = parse.jsish_list(raw_list)
        except Exception as e:
            return Result(ok=False, error=f"server_list: failed to parse list: {e}")

        if not isinstance(parsed, list):
            return Result(ok=False, error="server_list: parsed 'list' is not a list")

        # Fixing server names by stripping whitespace (some have trailing spaces, e.g. "קרמבו ") which is kinda stupid of the game but whatever
        for s in parsed:
            if isinstance(s, dict) and isinstance(s.get("name"), str):
                s["name"] = s["name"].strip()

        return Result(ok=True, value=parsed)