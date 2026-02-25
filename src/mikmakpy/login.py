"""
mikmakpy.login
──────────────

"""
from signal import signal, SIGINT, SIGTERM
from time import sleep

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
        server_to_join: Server | None = Server.KIWI,
        reconnection_delay: int = 5,
        max_retries: int = 2,
        starting_ip: str = "213.8.147.198",
        port: int = 443
    ):
        super().__init__()
        self.username = username
        self.password = password
        self.logger_levels = logger_levels
        self.server_to_join = server_to_join
        self.reconnection_delay = reconnection_delay
        self.max_retries = max_retries
        self.starting_ip = starting_ip
        self.port = port

        # Connection state
        self._conn: Connection | None = None
        self._is_first_connection = True
        self._target_server: dict | None = None
        self._running = False
        self._retry_count = 0

        # ── nested namespaces ──────────────────────────────────────────────
        self._send = self._SendInternal(self)

    # Public API
    def connect(self):
        """Start the client. Blocks until stopped."""
        signal(SIGINT,  self._exit_signal_handler)
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
        def __init__(self, client: MikmakLoginClient):
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
        print("[!] Signal received, shutting down...")
        self.disconnect()
    
    def _on_connect(self):
        if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
            print(f"[!] Connecting to {self.starting_ip}:{self.port} ...")
        self._send.sys("verChk", "<ver v='165' />")

    def _on_disconnect(self):
        if self._running and self._retry_count < self.max_retries:
            self._retry_count += 1
            if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                print(f"[!] Disconnected. Attempting to reconnect ({self._retry_count}/{self.max_retries}) in {self.reconnection_delay} seconds...")
            sleep(self.reconnection_delay)
            self._run()

    def _run(self):
        ip = self.starting_ip
        port = self.port

        if not self._is_first_connection and self._target_server:
            ip = self._target_server.get("ip", self.starting_ip)
            port = int(self._target_server.get("port", self.port))

        self._conn = Connection(on_message = self._on_message, on_disconnect = self._on_disconnect, on_connect = self._on_connect)

        try:
            self._conn.connect(ip, port)
            self._conn.listen()
        except Exception as e:
            print(f"[!] Connection error: {e}")
            self._on_disconnect()

    # ── Message handler ──────────────────────────────────────────────────────
    def _on_message(self, msg: str):
        if LoggerLevel.INCOMING in self.logger_levels:
            print(f"[←] {msg}")

        self._handle_login_message(msg)
        self._handle_game_message(msg)
        self.emit("message", msg)

    def _handle_login_message(self, msg: str):
        """Handle messages relevant to the login process. in both connection phases."""
        if msg.startswith("<cross-domain-policy>"):
            return
        
        if "action='apiOK'" in msg:
            pwd = ("cluster_" + self.password) if not self._is_first_connection else self.password
            self._send.sys(
                "login",
                f"<login z='VW'><nick><![CDATA[{self.username}]]></nick>"
                f"<pword><![CDATA[{pwd}]]></pword></login>",
            )
        
        if self._is_first_connection and '"_cmd":"server_list"' in msg:
            servers = parse.server_list(msg)
            if not servers.ok:
                print(f"[!] Failed to parse server list: {servers.error}")
                return
            servers = servers.value
            self.emit("server_list", servers)

            if self.server_to_join:
                for srv in servers:
                    if self.server_to_join in str(srv.get("name", "")):
                        self._target_server = srv
                        self._is_first_connection = False
                        if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                            print(f"[→] switching to '{self.server_to_join}' @ {srv['ip']}:{srv['port']}")
                        self._conn.close()
                        return
            
            # If we got here, we didn't find the server we wanted (or server_to_join was None), so we'll just exit.
            if LoggerLevel.CONNECTION_CHANGE in self.logger_levels:
                print(f"[!] Server '{self.server_to_join}' not found in server list: {[srv['name'] for srv in servers if 'name' in srv]}, Cannot auto-join, Disconnecting...")
            self.disconnect()

        # here ends the first connection phase, the next messages are from the game server after we've logged in and switched servers, so we can handle them separately if we want

        # if "action='rmList'" in msg:
        #     self._room_list_inital = MikMakProtocol.parse.room_list(msg)
        #     print(f"Got initial room list with {len(self._room_list_inital)} rooms")
        #     self.emit("room_list", self._room_list_inital)

        # if '"_cmd":"achivment_res"' in msg:
        #     self.emit("room_list", msg)
        #     self._on_login_complete()

        # if '"_cmd":"login_res"' in msg:
        #     self.login_res = MikMakProtocol.parse.login_res(msg)
        #     self.emit("logged_in", self.login_res)

    # ── Hooks for subclass ───────────────────────────────────────────────────

    def _handle_game_message(self, msg: str):
        pass

    def _on_login_complete(self):
        pass