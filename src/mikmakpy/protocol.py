"""
mikmakpy.protocol
─────────────────

"""

import ast
from json import dumps, loads
import re
from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET

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

    @staticmethod
    def xml(msg: str) -> Result[ET.Element]:
        """Try to parse an XML message. Returns the root Element or an error."""
        try:
            root = ET.fromstring(msg)
            return Result(ok=True, value=root)
        except Exception as e:
            return Result(ok=False, error=str(e))


class parse:
    @staticmethod
    def jsish_list(s: str) -> Any:
        # JS literals -> Python literals so literal_eval can parse
        s = re.sub(r"\btrue\b", "True", s)
        s = re.sub(r"\bfalse\b", "False", s)
        s = re.sub(r"\bnull\b", "None", s)
        return ast.literal_eval(s)

    @staticmethod
    def _to_int(x: Any) -> Optional[int]:
        try:
            return int(x)
        except Exception:
            return None

    @staticmethod
    def server_list(msg: str) -> Result[dict]:
        """Parse the server list from a raw xt message string. Returns dict with keys:
        - servers: list of dicts with keys id, name, ip, port, capacity, dt
        - safeChat: bool
        - rank: int
        - userName: str
        """

        data = decode.xt(msg)
        if not data.ok:
            return Result(ok=False, error=data.error)

        o = data.value.get("b", {}).get("o", {})
        if not isinstance(o, dict):
            return Result(ok=False, error="server_list: invalid 'b.o'")

        safe_chat = o.get("safeChat")
        rank = o.get("rank")
        user_name = o.get("userName")
        if not isinstance(safe_chat, bool):
            return Result(ok=False, error="server_list: 'safeChat' not bool")
        if not isinstance(rank, int):
            return Result(ok=False, error="server_list: 'rank' not int")
        if not isinstance(user_name, str) or not user_name:
            return Result(ok=False, error="server_list: 'userName' not str")

        raw_list = o.get("list")
        if not isinstance(raw_list, str) or not raw_list:
            return Result(ok=False, error="server_list: missing/invalid 'list'")

        try:
            servers = parse.jsish_list(raw_list)
        except Exception as e:
            return Result(ok=False, error=f"server_list: list parse failed: {e}")

        if not isinstance(servers, list):
            return Result(ok=False, error="server_list: parsed 'list' not list")

        for s in servers:
            if isinstance(s, dict) and isinstance(s.get("name"), str):
                s["name"] = s["name"].strip()

        return Result(
            ok=True,
            value={
                "servers": servers,
                "safeChat": safe_chat,
                "rank": rank,
                "userName": user_name,
            },
        )

    @staticmethod
    def room_list(msg: str, clean: bool) -> Result[List[Dict[str, Any]]]:
        """
        Parse:
          <msg><body action='rmList'><rmList><rm ...><n><![CDATA[name]]></n></rm>...</rmList></body></msg>

        Returns list of room dicts with keys:
          - id (int)
          - name (str)               # from <n>...</n>
          - usercount (int)          # ucnt
          - maxusercount (int)       # maxu

        Also includes guessed/extra fields when present:
          - is_private (bool)        # priv == '1'
          - is_temporary (bool)      # temp == '1'
          - is_game (bool)           # game == '1'
          - min_level (int|None)     # lmb (likely "level min bound")
          - max_spectators (int|None)# maxs (likely max spectators/secondary cap)
          
        if clean is True, will filter out rooms with 0 users.
        """
        try:
            root = ET.fromstring(msg)

            body = root.find("body")
            if body is None:
                return Result(ok=False, error="Missing <body>")

            rm_list = body.find("rmList")
            if rm_list is None:
                return Result(ok=False, error="Missing <rmList>")

            rooms: List[Dict[str, Any]] = []
            for rm in rm_list.findall("rm"):
                a = rm.attrib

                n = rm.findtext("n") or ""
                name = n.strip()

                def to_int(x: Optional[str]) -> Optional[int]:
                    if x is None:
                        return None
                    try:
                        return int(x)
                    except ValueError:
                        return None

                room: Dict[str, Any] = {
                    "id": to_int(a.get("id")),
                    "name": name,
                    "usercount": to_int(a.get("ucnt")) or 0,
                    "maxusercount": to_int(a.get("maxu")) or 0,
                }

                # extras (best-effort, based on attribute names)
                if "priv" in a:
                    room["is_private"] = a.get("priv") == "1"
                if "temp" in a:
                    room["is_temporary"] = a.get("temp") == "1"
                if "game" in a:
                    room["is_game"] = a.get("game") == "1"
                if "lmb" in a:
                    room["min_level"] = to_int(a.get("lmb"))
                if "maxs" in a:
                    room["max_spectators"] = to_int(a.get("maxs"))

                if not clean or room["usercount"] > 0:
                    rooms.append(room)

            return Result(ok=True, value=rooms)
        except Exception as e:
            return Result(ok=False, error=str(e))

    @staticmethod
    def inv_list(msg: str) -> Result[List[Dict[str, Any]]]:
        """Parse inventory list from xt message. Returns list of dicts with keys:
        - item_id: int
        - quantity: int
        """
        data = decode.xt(msg)
        if not data.ok:
            return Result(ok=False, error=data.error)

        o = data.value.get("b", {}).get("o", {})
        if not isinstance(o, dict):
            return Result(ok=False, error="inv_list: invalid 'b.o'")

        raw_list = o.get("list")
        if not isinstance(raw_list, str) or not raw_list:
            return Result(ok=False, error="inv_list: missing/invalid 'list'")

        items = []
        for part in raw_list.split(","):
            if "-" in part:
                item_id_str, quantity_str = part.split("-", 1)
                try:
                    item_id = int(item_id_str)
                    quantity = int(quantity_str)
                    items.append({"item_id": item_id, "quantity": quantity})
                except ValueError:
                    continue  # skip malformed entries
            else:
                try:
                    item_id = int(part)
                    items.append({"item_id": item_id, "quantity": 1})
                except ValueError:
                    continue  # skip malformed entries

        return Result(ok=True, value=items)

    @staticmethod
    def login_res(msg: str) -> Result[dict]:
        """Parse login response from xt message. Returns dict with keys:
        - date: str
        - c: int
        - time: str
        - k: int
        - resoulationCtg: int
        - resoulationVal: str
        """
        data = decode.xt(msg)
        if not data.ok:
            return Result(ok=False, error=data.error)

        o = data.value.get("b", {}).get("o", {})
        if not isinstance(o, dict):
            return Result(ok=False, error="login_res: invalid 'b.o'")

        return Result(ok=True, value=o)

    @staticmethod
    def achievement_res(msg: str) -> Result[Dict[str, Any]]:
        """
        Parse achievement response from xt message.

        Returns:
        {
          "user_id": int|None,
          "level": int|None,
          "points_total": int|None,
          "is_update": bool,
          "achievements": [
             {
               "achievement_id": int,"step_id": int,
               "progress": int,
               "points": int,
               "key": "ach:ass"
             }, ...
          ]
        }
        """
        data = decode.xt(msg)
        if not data.ok:
            return Result(ok=False, error=data.error)

        o = data.value.get("b", {}).get("o", {})
        if not isinstance(o, dict):
            return Result(ok=False, error="achievement_res: invalid 'b.o'")

        raw_list = o.get("list")
        if not isinstance(raw_list, str) or not raw_list.strip():
            return Result(ok=False, error="achievement_res: missing/invalid 'list'")

        # meta
        out: Dict[str, Any] = {
            "user_id": parse._to_int(o.get("userId")),
            "level": parse._to_int(o.get("level")),
            "points_total": parse._to_int(o.get("points")),
            "is_update": str(o.get("update", "")).lower() == "true",
            "achievements": [],
        }

        try:
            items = parse.jsish_list(raw_list)
        except Exception as e:
            return Result(ok=False, error=f"achievement_res: list parse failed: {e}")

        if not isinstance(items, list):
            return Result(ok=False, error="achievement_res: parsed 'list' not list")

        achievements: List[Dict[str, Any]] = []
        for it in items:
            if not isinstance(it, dict):
                continue

            ach = parse._to_int(it.get("ach"))
            ass = parse._to_int(it.get("ass"))
            p = parse._to_int(it.get("p"))
            prg = parse._to_int(it.get("prg"))

            # Require at least (ach, ass) to identify an entry
            if ach is None or ass is None:
                continue

            entry = {
                "achievement_id": ach,
                "step_id": ass,
                "progress": prg if prg is not None else 0,
                "points": p if p is not None else 0,
                "key": f"{ach}:{ass}",
            }
            achievements.append(entry)

        out["achievements"] = achievements
        return Result(ok=True, value=out)
