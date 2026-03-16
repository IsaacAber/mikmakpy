"""
mikmakpy.login
──────────────

"""

from signal import signal, SIGINT, SIGTERM
from time import sleep
from hashlib import md5
from uuid import getnode as get_mac

from .events import EventBus
from .constants import Server, LoggerLevel
from .connection import Connection
from .protocol import encode, parse


class MikmakLoginClient(EventBus):
    def __init__(
        self,
        username: str,
        password: str,
        logger_levels: set[LoggerLevel] = set(),
        mac_address: str = ":".join(
            f"{(get_mac() >> i) & 0xff:02x}" for i in range(40, -1, -8)
        ),
        server_to_join: Server | None = Server.KIWI,
        reconnection_delays: tuple[int] = (5, 0.5),
        max_retries: int = 2,
        clean_ingame: bool = True,
        starting_ip: str = "213.8.147.198",
        port: int = 443,
    ):
        """Initializes the MikmakLoginClient with the provided configuration.
        username: Your Mikmak username plain text
        password: Your Mikmak password plain text
        logger_levels: Set of LoggerLevel enums to control what kind of logs you want to see
        mac_address: The MAC address of your device, used for username derivation. By default it uses the actual MAC address of the device, but you can override it if neccessary
        server_to_join: The server to auto-join after login, if None it won't auto-join any server and just stop after receiving the server list
        reconnection_delays: A tuple of two integers, the first is the delay in seconds for reconnect and the second is for server switch.
        max_retries: The maximum number of reconnection attempts before giving up and disconnecting, set to 0 for infinite retries
        """
        super().__init__()
        self.username = username
        self.password = password
        self._original_username = username
        self._original_password = password

        self.username = f"[{md5((lambda u: u + u[0] + u[-1] + 'tryLORP983DkcAs@ybJnf')(mac_address.lower()).encode('latin-1')).hexdigest()}_{mac_address.lower()}]_src1_{username.lower()}"
        self.password = (
            "backLogin_"
            + md5(
                (
                    "_d32ERjhtp872msikj_"
                    + (
                        lambda s: s.translate(
                            str.maketrans(
                                {
                                    "א": "a",
                                    "ב": "b",
                                    "ג": "c",
                                    "ד": "d",
                                    "ה": "e",
                                    "ז": "f",
                                    "ח": "g",
                                    "ט": "h",
                                    "י": "i",
                                    "כ": "j",
                                    "ל": "k",
                                    "מ": "l",
                                    "נ": "m",
                                    "ס": "n",
                                    "ע": "o",
                                    "פ": "p",
                                    "צ": "q",
                                    "ק": "r",
                                    "ר": "s",
                                    "ש": "s",
                                    "ת": "t",
                                    "ם": "u",
                                    "ף": "v",
                                    "ך": "w",
                                    "ץ": "x",
                                    "ן": "y",
                                    "ו": "z",
                                }
                            )
                        )
                    )(self.password.lower())
                ).encode("latin-1")
            ).hexdigest()
        )

        self.logger_levels = logger_levels
        self.server_to_join = server_to_join
        self.reconnection_delays = reconnection_delays
        self.max_retries = max_retries
        self.clean_ingame = clean_ingame  # Try to make the game state as clean as possible, for example remove empty rooms from the room list, or servers with 0 capacity from the server list. This is just a quality of life thing for users of the client, it has no effect on the actual connection or login process. just remove data that is not useful while giving the option to keep it if someone wants to use it for something.
        self.starting_ip = starting_ip
        self.port = port

        # Connection state
        self._conn: Connection | None = None
        self._is_first_connection = True
        self._target_server: dict | None = None
        self._running = False
        self._switching_servers = False
        self._retry_count = 0

        # State collected from proccessing messages, can be used by subclass or event handlers or internal logic as needed
        self.ingame_state = {
            "username": None,
            "user_id": None,
            "rank": None,
            "xp": None,
            "safe_chat": None,
            "server_list": None,
            "room_list": None,
            "login_res": None,
            "achievements": None,
        }

        # ── nested namespaces ──────────────────────────────────────────────
        self._send = self._SendInternal(self)

    # Public API
    def connect(self):
        """Start the client. Blocks until stopped."""
        signal(SIGINT, self._exit_signal_handler)
        signal(SIGTERM, self._exit_signal_handler)
        self._running = True
        self._run()

    def disconnect(self):
        """Tear down the connection."""
        self._running = False
        if self._conn:
            self._conn.close()
            self._conn = None

    # Private methods
    class _SendInternal:
        """Low-level send primitives. Access via client._send.*"""

        def __init__(self, client: "MikmakLoginClient"):
            self._c = client

        def raw(self, message: str):
            if LoggerLevel.OUTGOING in self._c.logger_levels:
                print(f"[→] {message}")
            if self._c._conn:
                self._c._conn.send(message)

        def xt(self, cmd: str, p: dict, x: str = "ExtManager", r: int = -1):
            self.raw(encode.xt(cmd, p, x, r))

        def sys(self, action: str, body: str, r: int = 0):
            self.raw(encode.sys(action, body, r))

    # Connection cycle
    def _exit_signal_handler(self, signum, frame):
        if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
            print("[!] Signal received, shutting down...")
        self.disconnect()

    def _on_connect(self):
        if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
            ip = self.starting_ip
            port = self.port

            if not self._is_first_connection and self._target_server:
                ip = self._target_server.get("ip", self.starting_ip)
                port = int(self._target_server.get("port", self.port))
            print(f"\n[!] Connecting to {ip}:{port}{(" - " + self._target_server.get('name', '?')) if not self._is_first_connection and self._target_server else ''}...")
        
        if not self._is_first_connection:
            self._send.sys("verChk", "<ver v='165' />")

    def _on_disconnect(self):
        if self._running and (
            self._retry_count < self.max_retries or self.max_retries == 0
        ):
            if not self._switching_servers and self.max_retries > 0:
                self._retry_count += 1
                if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                    print(
                        f"[!] Disconnected. Attempting to reconnect ({self._retry_count}/{self.max_retries}) in {self.reconnection_delays[0]} seconds..."
                    )

            if self._switching_servers:
                self._switching_servers = False
                if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                    print(
                        f"[!] Waiting {self.reconnection_delays[1]} seconds before switching servers..."
                    )
                sleep(self.reconnection_delays[1])
            else:
                if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                    print(
                        f"[!] Waiting {self.reconnection_delays[0]} seconds before reconnecting..."
                    )
                sleep(self.reconnection_delays[0])
            self._run()
        else:
            if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                print("[!] Disconnected. No more reconnection attempts will be made.")
            self.disconnect()

    def _run(self):
        ip = self.starting_ip
        port = self.port

        if not self._is_first_connection and self._target_server:
            ip = self._target_server.get("ip", self.starting_ip)
            port = int(self._target_server.get("port", self.port))

        self._conn = Connection(
            on_message=self._on_message,
            on_disconnect=self._on_disconnect,
            on_connect=self._on_connect,
        )

        try:
            self._conn.connect(ip, port)
            self._conn.listen()
        except Exception as e:
            if LoggerLevel.INTERNAL_ERROR in self.logger_levels:
                print(f"[!] Connection error: {e}")
            self._on_disconnect()

    # ── Message handler ──────────────────────────────────────────────────────
    def _on_message(self, msg: str):
        if LoggerLevel.INCOMING in self.logger_levels:
            print(f"[←] {msg}")

        self._handle_login_messages(msg)
        self._handle_game_messages(msg)
        self.emit("message", msg)

    def _handle_login_messages(self, msg: str):
        """Handle messages relevant to the login process. in both connection phases."""
        if msg.startswith("<cross-domain-policy>"):
            if self._is_first_connection:
                self._send.sys("verChk", "<ver v='165' />")

        elif "action='apiOK'" in msg:
            pwd = (
                ("cluster_" + self.password)
                if not self._is_first_connection
                else self.password
            )
            self._send.sys(
                "login",
                f"<login z='VW'><nick><![CDATA[{self.username}]]></nick>"
                f"<pword><![CDATA[{pwd}]]></pword></login>",
            )

        elif self._is_first_connection and '"_cmd":"server_list"' in msg:
            parsed = parse.server_list(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"[!] Failed to parse server list: {parsed.error}")
                return

            self.ingame_state["username"] = parsed.value.get("userName")
            self.ingame_state["rank"] = parsed.value.get("rank")
            self.ingame_state["safe_chat"] = parsed.value.get("safeChat")
            self.ingame_state["server_list"] = parsed.value.get("servers")

            servers = parsed.value["servers"]
            self.emit("server_list", servers)

            if self.server_to_join:
                for srv in servers:
                    if self.server_to_join in str(srv.get("name", "")):
                        self._target_server = srv
                        self._is_first_connection = False
                        self._switching_servers = True
                        if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                            print(
                                f"[→] switching to '{self.server_to_join}' @ {srv['ip']}:{srv['port']}"
                            )
                        self._conn.close()
                        return

            # If we got here, we didn't find the server we wanted (or server_to_join was None), so we'll just exit.
            if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                print(
                    f"[!] Server '{self.server_to_join}' not found in server list: {[srv['name'] for srv in servers if 'name' in srv]}, Cannot auto-join, Disconnecting..."
                )
            self.disconnect()

        # here ends the first connection phase, the next messages are from the game server after we've logged in and switched servers, so we can handle them separately if we want
        elif "action='rmList'" in msg:
            self._retry_count = 0 # successful connection, reset retry count
            parsed = parse.room_list(msg, self.clean_ingame)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"[!] Failed to parse room list: {parsed.error}")
                return
            self.ingame_state["room_list"] = parsed.value
            self.emit("room_list", parsed.value)

        elif '"_cmd":"login_res"' in msg:
            parsed = parse.login_res(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"[!] Failed to parse login response: {parsed.error}")
                return
            self.ingame_state["login_res"] = parsed.value
            self.emit("login_res", parsed.value)

        # handle this on login logic too because, it's before the client can really do anything, so might as well have it here.
        elif '"_cmd":"achivment_res"' in msg:
            parsed = parse.achievement_res(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"[!] Failed to parse achievement response: {parsed.error}")
                return

            # local-only helper (used only here)
            def merge_achievements(existing, incoming, is_update):
                # snapshot or nothing to merge into
                if not is_update or not existing:
                    return incoming

                merged_by_key = {}
                for a in existing:
                    k = a.get("key")
                    if isinstance(k, str):
                        merged_by_key[k] = dict(a)

                for a in incoming:
                    k = a.get("key")
                    if not isinstance(k, str):
                        continue
                    if k in merged_by_key:
                        merged_by_key[k].update(a)  # patch progress/points/etc
                    else:
                        merged_by_key[k] = dict(a)

                # keep existing order, append new keys
                out, seen = [], set()
                for a in existing:
                    k = a.get("key")
                    if isinstance(k, str) and k in merged_by_key and k not in seen:
                        out.append(merged_by_key[k])
                        seen.add(k)
                for k, a in merged_by_key.items():
                    if k not in seen:
                        out.append(a)
                return out

            self.ingame_state["user_id"] = parsed.value.get("user_id")

            lvl = parsed.value.get("level")
            if (
                LoggerLevel.PARSING_ERROR in self.logger_levels
                and isinstance(self.ingame_state.get("rank"), int)
                and isinstance(lvl, int)
                and lvl != self.ingame_state["rank"]
            ):
                print(
                    f"[!] Warning: achievement level differs from login rank: {lvl} vs {self.ingame_state['rank']}"
                )

            if isinstance(lvl, int):
                self.ingame_state["rank"] = lvl

            pts = parsed.value.get("points_total")
            if isinstance(pts, int):
                self.ingame_state["xp"] = pts

            incoming_ach = parsed.value.get("achievements") or []
            is_update = bool(parsed.value.get("is_update"))
            self.ingame_state["achievements"] = merge_achievements(
                self.ingame_state.get("achievements"),
                incoming_ach,
                is_update,
            )

            self.emit("achievement_res", incoming_ach, is_update)

            # send the last login step packet which is to join the room
            self._send.xt("avt_joinRoom", {"auto": 1})
        
        else:
            pass

    # ── Hooks for subclass ───────────────────────────────────────────────────

    def _handle_game_messages(self, msg: str):
        pass
