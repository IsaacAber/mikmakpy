"""
mikmakpy.ingame
─────────────────
Extends MikmakLoginClient with in-game message handling (inventory, movement,
chat, etc.) for use after the login flow completes and the client has joined
a game server room.
"""

from uuid import getnode as get_mac

from .constants import LoggerLevel, Server, ROOM_DEFAULT_SPAWN_POSITIONS
from .login import MikmakLoginClient
from .protocol import parse


class MikmakIngameClient(MikmakLoginClient):
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
        super().__init__(
            username,
            password,
            logger_levels,
            mac_address,
            server_to_join,
            reconnection_delays,
            max_retries,
            clean_ingame,
            starting_ip,
            port,
        )

        self.ingame_state.update(
            {
                "room_id": None,
                "room_vars": None,
                "users": None,
                "session_id": None,
                "hasSentReadyAfterJoin": True,
            }
        )

    def _handle_game_messages(self, msg, action, cmd):
        if action == "joinOK":
            parsed = parse.join_ok(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"Failed to parse joinOK message: {parsed.error}")
                return

            self.ingame_state.update(
                {
                    "room_id": parsed.value["room_id"],
                    "room_vars": parsed.value["room_vars"],
                    "users": parsed.value["users"],
                }
            )

            for user in parsed.value["users"]:
                if user["username"] == self._original_username:
                    self.ingame_state["session_id"] = user["session_id"]
                    break


            self._send.xt(
                "avt_uvr",
                p={
                    "x": ",".join(
                        map(
                            str,
                            ROOM_DEFAULT_SPAWN_POSITIONS.get(
                                parsed.value["room_id"], (0, 0)
                            ),
                        )
                    ),
                },
                r=self.ingame_state["room_id"],
            )
            self.ingame_state["hasSentReadyAfterJoin"] = False

            self.emit("room_join", parsed.value)

        elif action == "uVarsUpdate":
            parsed = parse.u_vars_update(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"Failed to parse uVarsUpdate message: {parsed.error}")
                return

            session_id = parsed.value["session_id"]
            if self.ingame_state["users"] is not None:
                for user in self.ingame_state["users"]:
                    if user["session_id"] == session_id:
                        user.update(parsed.value["updated"])
                        user["unparsed"].update(parsed.value["unparsed"])

                        if not self.ingame_state["hasSentReadyAfterJoin"] and user["session_id"] == self.ingame_state["session_id"]:
                            self._send.xt(
                                "f_ready",
                                r=self.ingame_state["room_id"],
                            )
                            self.ingame_state["hasSentReadyAfterJoin"] = True

            self.emit("user_update", parsed.value)

        elif action == "uER":
            parsed = parse.u_enter_room(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"Failed to parse user enter room message: {parsed.error}")
                return

            if self.ingame_state["users"] is not None:
                self.ingame_state["users"].append(parsed.value)

            self.emit("user_enter", parsed.value)

        elif action == "userGone":
            parsed = parse.user_gone(msg)
            if not parsed.ok:
                if LoggerLevel.PARSING_ERROR in self.logger_levels:
                    print(f"Failed to parse userGone message: {parsed.error}")
                return

            session_id = parsed.value["session_id"]
            left_user = None
            if self.ingame_state["users"] is not None:
                for user in self.ingame_state["users"]:
                    if user["session_id"] == session_id:
                        left_user = user
                        break
                self.ingame_state["users"] = [
                    u for u in self.ingame_state["users"]
                    if u["session_id"] != session_id
                ]

            self.emit("user_leave", session_id, left_user)

