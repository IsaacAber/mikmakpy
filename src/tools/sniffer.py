"""
mik_sniffer.py — MikMak protocol packet sniffer.
Buffers TCP streams, parses SYS/XT packets, writes HTML log, curses TUI.
"""

import os, re, sys, json, time, curses, threading, html as H
import xml.etree.ElementTree as ET
from collections import defaultdict, deque
from datetime import datetime

try:
    from scapy.all import sniff, TCP, Raw, IP
    SCAPY_OK = True
except ImportError:
    SCAPY_OK = False

SERVER_IP = "213.8.147.198"
LOG_FILE  = "packet.html"
MAX_FEED  = 500

feed_lock  = threading.Lock()
feed_lines = deque(maxlen=MAX_FEED)
html_lock  = threading.Lock()
_buffers: dict = defaultdict(bytearray)

# ── Parsing ───────────────────────────────────────────────────────────────────

def split_buffer(buf):
    msgs = []
    while b"\x00" in buf:
        msg, buf = buf.split(b"\x00", 1)
        msgs.append(msg.decode("utf-8", errors="replace"))
    return msgs, buf

def decode_xt(msg):
    try: return json.loads(msg)
    except: return None

def classify(msg):
    if msg.startswith("{"):
        d = decode_xt(msg)
        if not d: return "raw", None
        cmd = d.get("b", {}).get("c", "")
        o   = d.get("b", {}).get("o", {})
        if cmd == "msg_e":   return "event", {"id": int(o.get("id",-1)), "room": d.get("b",{}).get("r",-1)}
        if "sender" in o:    return "chat",  {"user": o["sender"], "text": o.get("msg","")}
        if o.get("_cmd") == "login_res": return "login", o
        return "xt", d
    if msg.startswith("<"):
        if "userGone" in msg:
            try:
                root = ET.fromstring(msg)
                u = root.find(".//user")
                return "gone", {"session_id": int(u.get("id",-1)) if u is not None else -1}
            except: pass
        return "sys", None
    return "raw", None

# ── HTML log ──────────────────────────────────────────────────────────────────

# Types where the body IS the raw content — no point showing a redundant raw panel
RAW_TYPES = {"sys", "raw"}

HTML_HEAD = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>MikMak Packet Log</title><style>
:root{{--bg:#0d1117;--fg:#c9d1d9;--dim:#484f58;--br:#30363d;
      --sys:#388bfd;--xt:#3fb950;--chat:#e3b341;--event:#f78166;
      --login:#d2a8ff;--gone:#8b949e;--bin:#6e7681;--ts:#58a6ff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--fg);font:13px/1.6 "Fira Code",monospace;padding:16px}}
h1{{color:var(--ts);margin-bottom:12px;font-size:15px}}
.e{{border:1px solid var(--br);border-radius:6px;margin-bottom:10px;overflow:hidden}}
.eh{{display:flex;gap:10px;align-items:center;padding:5px 12px;background:#161b22;
     border-bottom:1px solid var(--br);font-size:11px}}
.ts{{color:var(--ts)}} .rt{{color:var(--dim)}}
.eh button{{background:var(--br);color:var(--fg);border:none;padding:2px 6px;
            border-radius:3px;cursor:pointer;font-size:10px}}
.raw{{display:none;padding:10px 14px;white-space:pre-wrap;word-break:break-all;
      font-size:12px;color:#8b949e;border-top:1px solid var(--br)}}
.b{{border-radius:4px;padding:1px 7px;font-weight:700;font-size:10px;letter-spacing:.06em}}
{chr(10).join(f'.b-{t}{{background:{bg};color:var(--{t})}}' for t, bg in
    [("sys","#1c3a6b"),("xt","#1a3825"),("chat","#3b2f00"),
     ("event","#3b1a1a"),("login","#2a1a4a"),("gone","#1e2228"),("raw","#1c2128")])}
.bd{{padding:10px 14px;white-space:pre-wrap;word-break:break-all;font-size:12px}}
{chr(10).join(f'.bd-{t}{{color:var(--{t})}}' for t in ["sys","xt","chat","event","login","gone","raw"])}
.k{{color:var(--dim)}} .v{{color:var(--fg)}}
</style>
<script>
function toggleRaw(btn){{
  const r=btn.closest('.e').querySelector('.raw');
  const show=r.style.display!=='block';
  r.style.display=show?'block':'none';
  btn.textContent=show?'Hide Raw':'Show Raw';
}}
</script></head><body>
<h1>📡 MikMak Packet Log — {datetime.now():%Y-%m-%d %H:%M:%S}</h1>
"""

def _init_log():
    with html_lock:
        open(LOG_FILE, "w", encoding="utf-8").write(HTML_HEAD + "</body></html>")

def _append_html(block):
    with html_lock:
        with open(LOG_FILE, "r+b") as f:
            f.seek(0, 2)
            pos = f.tell()
            f.seek(max(0, pos - 20))
            tail = f.read()
            cut = tail.rfind(b"</body>")
            f.seek(max(0, pos - 20) + cut)
            f.write((block + "\n</body></html>").encode())
            f.truncate()

def kv(k, v): return f'<span class="k">{H.escape(k)}=</span><span class="v">{H.escape(str(v))}</span> '

def log_packet(ts, src, dst, msg, msg_type, parsed):
    show_raw_btn = "" if msg_type in RAW_TYPES else '<button onclick="toggleRaw(this)">Show Raw</button>'
    raw_panel    = "" if msg_type in RAW_TYPES else f'<div class="raw">{H.escape(msg)}</div>'

    if parsed and msg_type in ("chat", "event", "login", "gone"):
        body = "".join(kv(k, v) for k, v in parsed.items())
    elif msg_type == "xt":
        try: body = H.escape(json.dumps(json.loads(msg), indent=2, ensure_ascii=False))
        except: body = H.escape(msg)
    else:
        body = H.escape(msg)

    _append_html(
        f'<div class="e">'
        f'<div class="eh"><span class="ts">{H.escape(ts)}</span>'
        f'<span class="b b-{msg_type}">{msg_type.upper()}</span>'
        f'<span class="rt">{H.escape(src)} → {H.escape(dst)}</span>'
        f'{show_raw_btn}</div>'
        f'<div class="bd bd-{msg_type}">{body}</div>'
        f'{raw_panel}</div>'
    )

# ── Packet handling ───────────────────────────────────────────────────────────

def packet_callback(pkt):
    if not (pkt.haslayer(TCP) and pkt.haslayer(Raw) and pkt.haslayer(IP)): return
    if pkt[IP].src != SERVER_IP and pkt[IP].dst != SERVER_IP: return

    src = f"{pkt[IP].src}:{pkt[TCP].sport}"
    dst = f"{pkt[IP].dst}:{pkt[TCP].dport}"
    key = (pkt[IP].src, pkt[TCP].sport, pkt[IP].dst, pkt[TCP].dport)
    _buffers[key] += pkt[Raw].load
    msgs, _buffers[key] = split_buffer(_buffers[key])
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for msg in msgs:
        if not msg.strip(): continue
        msg_type, parsed = classify(msg)
        with feed_lock:
            feed_lines.append(f"[{ts}] [{msg_type.upper():5}] {src} → {dst}  {msg[:120].replace(chr(10),' ')}")
        log_packet(ts, src, dst, msg, msg_type, parsed)

# ── TUI ───────────────────────────────────────────────────────────────────────

HELP = " /search  :clear  :quit  ↑↓ scroll  q quit"
TYPE_COLORS = {"SYS":1,"XT":2,"CHAT":3,"EVENT":4,"LOGIN":5,"GONE":6,"BIN":6,"RAW":6}

def tui_main(stdscr):
    curses.curs_set(1); curses.start_color(); curses.use_default_colors()
    for i, c in enumerate([curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW,
                            curses.COLOR_RED, curses.COLOR_MAGENTA, curses.COLOR_WHITE], 1):
        curses.init_pair(i, c, -1)

    stdscr.nodelay(True); stdscr.keypad(True)
    search, cmd_buf, cmd_mode, scroll_off, status = "", "", False, 0, ""

    def draw():
        h, w = stdscr.getmaxyx()
        feed_h = h - 3

        stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(0, 0, f" 📡 MikMak Sniffer | log→{LOG_FILE} |{HELP} "[:w].ljust(w))
        stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

        with feed_lock: lines = list(feed_lines)
        if search:
            try: rx = re.compile(search, re.I); lines = [l for l in lines if rx.search(l)]
            except: lines = [l for l in lines if search.lower() in l.lower()]

        total = len(lines)
        visible = lines[max(0, total - feed_h - scroll_off): max(0, total - feed_h - scroll_off) + feed_h]

        for row, line in enumerate(visible, 1):
            color = next((cp for tag, cp in TYPE_COLORS.items() if f"[{tag}]" in line or f"[{tag} ]" in line), 6)
            try: stdscr.addstr(row, 0, line[:w-1].ljust(w-1), curses.color_pair(color))
            except curses.error: pass

        for row in range(len(visible)+1, feed_h+1):
            try: stdscr.addstr(row, 0, " "*(w-1))
            except curses.error: pass

        stat = status or f"  {total} packets" + (f"  filter:/{search}" if search else "") + (f"  ↑{scroll_off}" if scroll_off else "")
        try: stdscr.addstr(h-2, 0, stat[:w-1].ljust(w-1), curses.color_pair(3))
        except curses.error: pass

        prompt = (f"{'/' if not cmd_buf.startswith(':') else ''}{cmd_buf}" if cmd_mode else "  [/search  :command  ↑↓ scroll  q quit]")
        try: stdscr.addstr(h-1, 0, prompt[:w-1].ljust(w-1), curses.color_pair(1))
        except curses.error: pass
        stdscr.refresh()

    last_len = 0
    while True:
        with feed_lock: cur_len = len(feed_lines)
        if cur_len != last_len:
            last_len = cur_len; status = ""; draw()

        try: key = stdscr.get_wch()
        except curses.error: time.sleep(0.05); continue

        if not cmd_mode:
            if key == curses.KEY_UP:   scroll_off += 1; draw(); continue
            if key == curses.KEY_DOWN: scroll_off = max(0, scroll_off-1); draw(); continue
            if key in ("q","Q"): break
            if isinstance(key, str) and key in (":", "/"):
                cmd_mode = True; cmd_buf = key if key == ":" else ""; draw(); continue

        if cmd_mode:
            if key in (curses.KEY_ENTER, "\n", "\r"):
                raw = cmd_buf.strip()
                if raw.startswith(":"):
                    cmd = raw[1:].strip()
                    if cmd in ("quit","q","exit"): break
                    elif cmd == "clear": _init_log(); feed_lines.clear(); status = "  ✓ cleared"
                    else: status = f"  unknown: {raw}"
                else:
                    search = raw; status = f"  filter:/{search}"
                cmd_buf = ""; cmd_mode = False; draw()
            elif key in (curses.KEY_BACKSPACE, "\x7f", 127): cmd_buf = cmd_buf[:-1]; draw()
            elif key == "\x1b": cmd_buf = ""; cmd_mode = False; search = ""; draw()
            elif isinstance(key, str): cmd_buf += key; draw()

        time.sleep(0.02)

# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    if not SCAPY_OK: sys.exit("[!] Install scapy: pip install scapy")
    _init_log()
    print(f"[*] Log: {os.path.abspath(LOG_FILE)}\n[*] Capturing host {SERVER_IP} port 443 (requires root)")
    threading.Thread(target=lambda: sniff(filter=f"host {SERVER_IP} and port 443", prn=packet_callback, store=0), daemon=True).start()
    time.sleep(0.3)
    try: curses.wrapper(tui_main)
    except KeyboardInterrupt: pass
    print(f"\n[*] Exiting. Log saved to {os.path.abspath(LOG_FILE)}")

if __name__ == "__main__":
    main()