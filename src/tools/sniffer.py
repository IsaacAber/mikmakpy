"""
mik_sniffer.py
──────────────
Packet sniffer for MikMak protocol traffic.

Features:
  • Buffers per-stream until null-byte terminator — full messages only
    • Parses messages with built-in local helpers (sys XML / xt JSON)
  • Writes a colorful HTML log (open in browser for easy reading)
  • Interactive CLI (curses):
      - Live packet feed
      - /<regex or string>   — filter/search live view
      - :clear               — clear the HTML log file
      - :quit / q            — exit
"""

import os
import re
import sys
import json
import time
import curses
import threading
import html as html_mod
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from datetime import datetime

# ── Optional scapy import ────────────────────────────────────────────────────
try:
    from scapy.all import sniff, TCP, Raw, IP
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

# ── Protocol helpers (local, no external protocol dependency) ───────────────
NULL_BYTE = b"\x00"


def split_buffer(buffer: bytearray) -> tuple[list[str], bytearray]:
    messages = []
    while NULL_BYTE in buffer:
        msg_bytes, buffer = buffer.split(NULL_BYTE, 1)
        messages.append(msg_bytes.decode("utf-8", errors="replace"))
    return messages, buffer


def decode_xt_message(msg: str) -> dict | None:
    try:
        return json.loads(msg)
    except Exception:
        return None


def parse_msg_e(msg: str) -> dict | None:
    data = decode_xt_message(msg)
    if not data:
        return None
    try:
        o = data.get("b", {}).get("o", {})
        return {"id": int(o.get("id", -1)), "room": data.get("b", {}).get("r", -1), "raw": msg}
    except Exception:
        return None


def parse_chat(msg: str) -> dict | None:
    data = decode_xt_message(msg)
    if not data:
        return None
    o = data.get("b", {}).get("o", {})
    room = data.get("b", {}).get("r", -1)
    if "sender" in o and "msg" in o:
        return {"username": o["sender"], "text": o["msg"], "room": room}
    return None


def parse_user_gone(msg: str) -> dict | None:
    try:
        root = ET.fromstring(msg)
        body = root.find("body")
        if body is None or body.get("action") != "userGone":
            return None
        user = root.find(".//user")
        return {
            "session_id": int(user.get("id", -1)) if user is not None else -1,
            "room": int(body.get("r", -1)),
        }
    except Exception:
        return None


def parse_login_res(msg: str) -> dict | None:
    data = decode_xt_message(msg)
    if not data:
        return None
    o = data.get("b", {}).get("o", {})
    return o if o.get("_cmd") == "login_res" else None


# ── Config ────────────────────────────────────────────────────────────────────
SERVER_IP  = "213.8.147.198"
LOG_FILE   = "packet.html"
MAX_FEED   = 500        # lines kept in live feed deque

# ── Shared state ──────────────────────────────────────────────────────────────
feed_lock   = threading.Lock()
feed_lines  = deque(maxlen=MAX_FEED)   # plain-text lines for TUI
html_lock   = threading.Lock()


# ══════════════════════════════════════════════════════════════════════════════
#  HTML LOG
# ══════════════════════════════════════════════════════════════════════════════

HTML_HEAD = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MikMak Packet Log</title>
<style>
  :root{--bg:#0d1117;--fg:#c9d1d9;--dim:#484f58;--border:#30363d;
        --sys:#388bfd;--xt:#3fb950;--chat:#e3b341;--event:#f78166;
        --login:#d2a8ff;--gone:#8b949e;--bin:#6e7681;--ts:#58a6ff;}
  *{box-sizing:border-box;margin:0;padding:0}
  body{background:var(--bg);color:var(--fg);font:13px/1.6 "Fira Code",monospace;padding:16px}
  h1{color:var(--ts);margin-bottom:12px;font-size:16px;letter-spacing:.05em}
  .entry{border:1px solid var(--border);border-radius:6px;margin-bottom:10px;overflow:hidden}
  .entry-header{display:flex;gap:12px;align-items:center;padding:6px 12px;
                background:#161b22;border-bottom:1px solid var(--border);font-size:11px}
  .ts{color:var(--ts)}
  .route{color:var(--dim)}
  .entry-header button{background:var(--border);color:var(--fg);border:none;padding:2px 6px;border-radius:3px;cursor:pointer;font-size:10px}
  .raw{display:none;padding:10px 14px;white-space:pre-wrap;word-break:break-all;font-size:12px;color:#8b949e;border-top:1px solid var(--border)}
  .badge{border-radius:4px;padding:1px 7px;font-weight:700;font-size:10px;letter-spacing:.06em}
  .badge-sys   {background:#1c3a6b;color:var(--sys)}
  .badge-xt    {background:#1a3825;color:var(--xt)}
  .badge-chat  {background:#3b2f00;color:var(--chat)}
  .badge-event {background:#3b1a1a;color:var(--event)}
  .badge-login {background:#2a1a4a;color:var(--login)}
  .badge-gone  {background:#1e2228;color:var(--gone)}
  .badge-bin   {background:#1c1f24;color:var(--bin)}
  .badge-raw   {background:#1c2128;color:#a0a8b0}
  .body{padding:10px 14px;white-space:pre-wrap;word-break:break-all;font-size:12px}
  .body-sys   {color:var(--sys)}
  .body-xt    {color:var(--xt)}
  .body-chat  {color:var(--chat)}
  .body-event {color:var(--event)}
  .body-login {color:var(--login)}
  .body-gone  {color:var(--gone)}
  .body-bin   {color:var(--bin)}
  .body-raw   {color:#8b949e}
  .kv{display:inline-block;margin-right:16px}
  .k{color:var(--dim)} .v{color:var(--fg)}
</style>
<script>
function toggleRaw(btn) {
    const entry = btn.closest('.entry');
    const raw = entry.querySelector('.raw');
    if (raw.style.display === 'none' || raw.style.display === '') {
        raw.style.display = 'block';
        btn.textContent = 'Hide Raw';
    } else {
        raw.style.display = 'none';
        btn.textContent = 'Show Raw';
    }
}
</script>
</head>
<body>
<h1>📡 MikMak Packet Log — started {started}</h1>
""".replace("{started}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

HTML_FOOT = "\n</body>\n</html>\n"


def _init_log():
    with html_lock:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(HTML_HEAD)
            f.write(HTML_FOOT)


def _append_html(block: str):
    """Insert block before closing </body></html>."""
    with html_lock:
        with open(LOG_FILE, "r+b") as f:
            # find position of the foot
            tail = len(HTML_FOOT.encode())
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - tail - 20))
            chunk = f.read()
            idx = chunk.rfind(b"</body>")
            if idx == -1:
                f.seek(0, 2)
            else:
                f.seek(max(0, size - tail - 20) + idx)
            f.write((block + "\n</body>\n</html>\n").encode("utf-8"))
            f.truncate()


def _badge(label: str) -> str:
    return f'<span class="badge badge-{label}">{label.upper()}</span>'


def _kv(k: str, v) -> str:
    return f'<span class="kv"><span class="k">{html_mod.escape(k)}=</span><span class="v">{html_mod.escape(str(v))}</span></span>'


def log_packet(timestamp: str, src: str, dst: str, msg: str,
               msg_type: str, parsed: dict | None, is_binary: bool = False):
    route = html_mod.escape(f"{src} → {dst}")
    ts    = html_mod.escape(timestamp)

    if is_binary:
        label   = "bin"
        body_txt = html_mod.escape(msg)
    else:
        label   = msg_type
        if parsed and msg_type in ("chat", "event", "login", "gone"):
            body_txt = "".join(_kv(k, v) for k, v in parsed.items() if k != "raw")
        elif msg_type == "xt":
            try:
                pretty = json.dumps(json.loads(msg), indent=2, ensure_ascii=False)
                body_txt = html_mod.escape(pretty)
            except Exception:
                body_txt = html_mod.escape(msg)
        else:
            body_txt = html_mod.escape(msg)

    block = (
        f'<div class="entry">'
        f'<div class="entry-header">'
        f'<span class="ts">{ts}</span>'
        f'{_badge(label)}'
        f'<span class="route">{route}</span>'
        f'<button onclick="toggleRaw(this)">Show Raw</button>'
        f'</div>'
        f'<div class="body body-{label}">{body_txt}</div>'
        f'<div class="raw">{html_mod.escape(msg)}</div>'
        f'</div>'
    )
    _append_html(block)


# ══════════════════════════════════════════════════════════════════════════════
#  PACKET PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

# Per-stream TCP reassembly buffers  {(src_ip, src_port, dst_ip, dst_port): bytearray}
_buffers: dict = defaultdict(bytearray)


def _classify(msg: str) -> tuple[str, dict | None]:
    """Return (type_label, parsed_dict_or_None)."""
    if msg.startswith("{"):
        data = decode_xt_message(msg)
        if data:
            cmd = data.get("b", {}).get("c", "")
            o   = data.get("b", {}).get("o", {})
            if cmd == "msg_e":
                return "event", parse_msg_e(msg)
            if cmd == "pubMsg" or "sender" in o:
                return "chat", parse_chat(msg)
            login = parse_login_res(msg)
            if login:
                return "login", login
            return "xt", data
    if msg.startswith("<"):
        if "userGone" in msg:
            return "gone", parse_user_gone(msg)
        return "sys", None
    return "raw", None


def _feed(line: str):
    with feed_lock:
        feed_lines.append(line)


def handle_message(timestamp: str, src: str, dst: str, msg: str):
    msg_type, parsed = _classify(msg)

    # Short plain-text line for TUI feed
    short = msg[:120].replace("\n", " ")
    _feed(f"[{timestamp}] [{msg_type.upper():5}] {src} → {dst}  {short}")

    log_packet(timestamp, src, dst, msg, msg_type, parsed)


def packet_callback(packet):
    if not (packet.haslayer(TCP) and packet.haslayer(Raw) and packet.haslayer(IP)):
        return
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    if src_ip != SERVER_IP and dst_ip != SERVER_IP:
        return

    src = f"{src_ip}:{packet[TCP].sport}"
    dst = f"{dst_ip}:{packet[TCP].dport}"
    key = (src_ip, packet[TCP].sport, dst_ip, packet[TCP].dport)

    payload = packet[Raw].load

    # Try UTF-8 text stream
    try:
        _buffers[key] += payload
    except Exception:
        return

    messages, _buffers[key] = split_buffer(_buffers[key])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for msg in messages:
        if msg.strip():
            handle_message(timestamp, src, dst, msg)





# ══════════════════════════════════════════════════════════════════════════════
#  INTERACTIVE TUI  (curses)
# ══════════════════════════════════════════════════════════════════════════════

HELP = (
    "  /<pattern>   filter feed (regex or plain string)  |  "
    "  :clear       clear HTML log  |  "
    "  :quit / q   exit"
)


def tui_main(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN,    -1)
    curses.init_pair(2, curses.COLOR_GREEN,   -1)
    curses.init_pair(3, curses.COLOR_YELLOW,  -1)
    curses.init_pair(4, curses.COLOR_RED,     -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_WHITE,   -1)

    TYPE_COLOR = {
        "SYS":   1, "XT": 2, "CHAT": 3,
        "EVENT": 4, "LOGIN": 5, "GONE": 6,
        "BIN":   6, "RAW": 6,
    }

    stdscr.nodelay(True)
    stdscr.keypad(True)

    search_pat = ""
    cmd_buf    = ""
    cmd_mode   = False     # True while typing a command/search
    scroll_off = 0         # lines from bottom (0 = follow tail)
    status_msg = ""

    def draw():
        nonlocal scroll_off
        h, w = stdscr.getmaxyx()

        # title bar
        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        title = f" 📡 MikMak Sniffer  |  log → {LOG_FILE}  |  {HELP} "
        stdscr.addstr(0, 0, title[:w].ljust(w))
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        # feed area  (rows 1 .. h-3)
        feed_h = h - 3
        with feed_lock:
            lines = list(feed_lines)

        # apply filter
        if search_pat:
            try:
                rx = re.compile(search_pat, re.IGNORECASE)
                lines = [l for l in lines if rx.search(l)]
            except re.error:
                lines = [l for l in lines if search_pat.lower() in l.lower()]

        # scroll
        total = len(lines)
        if scroll_off > total - feed_h:
            scroll_off = max(0, total - feed_h)
        visible_start = max(0, total - feed_h - scroll_off)
        visible       = lines[visible_start: visible_start + feed_h]

        for row, line in enumerate(visible, start=1):
            # detect type tag like [EVENT]
            color = 6
            for tag, cp in TYPE_COLOR.items():
                if f"[{tag}]" in line or f"[{tag} ]" in line:
                    color = cp
                    break
            try:
                stdscr.addstr(row, 0, line[:w - 1].ljust(w - 1),
                              curses.color_pair(color))
            except curses.error:
                pass

        # clear leftover rows
        for row in range(len(visible) + 1, feed_h + 1):
            try:
                stdscr.addstr(row, 0, " " * (w - 1))
            except curses.error:
                pass

        # status bar
        filter_txt = f"  filter: /{search_pat}" if search_pat else ""
        scroll_txt = f"  scroll↑{scroll_off}" if scroll_off else ""
        stat = (status_msg or f"  {total} packets{filter_txt}{scroll_txt}")
        stdscr.attron(curses.color_pair(3))
        try:
            stdscr.addstr(h - 2, 0, stat[:w - 1].ljust(w - 1))
        except curses.error:
            pass
        stdscr.attroff(curses.color_pair(3))

        # command / input line
        if cmd_mode:
            prompt = f"{'/' if not cmd_buf.startswith(':') else ''}{cmd_buf}"
        else:
            prompt = "  [/search  :command  ↑↓ scroll  q quit]"
        try:
            stdscr.addstr(h - 1, 0, prompt[:w - 1].ljust(w - 1),
                          curses.color_pair(1))
        except curses.error:
            pass

        stdscr.refresh()

    last_len = 0
    while True:
        # redraw when new packets arrive
        with feed_lock:
            cur_len = len(feed_lines)
        if cur_len != last_len:
            last_len = cur_len
            status_msg = ""
            draw()

        try:
            key = stdscr.get_wch()
        except curses.error:
            time.sleep(0.05)
            continue

        # ── scroll ────────────────────────────────────────────────────────
        if not cmd_mode:
            if key == curses.KEY_UP:
                scroll_off += 1
                draw()
                continue
            if key == curses.KEY_DOWN:
                scroll_off = max(0, scroll_off - 1)
                draw()
                continue
            if key in ("q", "Q"):
                break

        # ── enter command mode ────────────────────────────────────────────
        if not cmd_mode and isinstance(key, str) and key in (":", "/"):
            cmd_mode = True
            cmd_buf  = key if key == ":" else ""
            draw()
            continue

        if cmd_mode:
            if key in (curses.KEY_ENTER, "\n", "\r"):
                raw = cmd_buf.strip()
                if raw.startswith(":"):
                    cmd = raw[1:].strip()
                    if cmd in ("quit", "q", "exit"):
                        break
                    elif cmd == "clear":
                        _init_log()
                        with feed_lock:
                            feed_lines.clear()
                        status_msg = "  ✓ log cleared"
                    else:
                        status_msg = f"  unknown command: {raw}"
                else:
                    # treat as search pattern
                    search_pat = raw
                    status_msg = f"  filter: /{search_pat}"
                cmd_buf  = ""
                cmd_mode = False
                draw()

            elif key in (curses.KEY_BACKSPACE, "\x7f", 127):
                cmd_buf = cmd_buf[:-1]
                draw()

            elif key == "\x1b":   # ESC — cancel
                cmd_buf  = ""
                cmd_mode = False
                search_pat = ""
                draw()

            elif isinstance(key, str):
                cmd_buf += key
                draw()

        time.sleep(0.02)


# ══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    if not SCAPY_OK:
        print("[!] scapy is not installed. Install it with: pip install scapy")
        sys.exit(1)

    _init_log()
    print(f"[*] Log file : {os.path.abspath(LOG_FILE)}")
    print(f"[*] Live capture: host {SERVER_IP} port 443  (requires root/admin)")

    def _sniff():
        sniff(
            filter=f"host {SERVER_IP} and port 443",
            prn=packet_callback,
            store=0,
        )

    t = threading.Thread(target=_sniff, daemon=True)
    t.start()
    time.sleep(0.3)

    try:
        curses.wrapper(tui_main)
    except KeyboardInterrupt:
        pass

    print(f"\n[*] Exiting. Log saved to {os.path.abspath(LOG_FILE)}")


if __name__ == "__main__":
    main()