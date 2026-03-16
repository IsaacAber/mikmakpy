"""
mikmakpy.ingame
─────────────────
Extends MikmakLoginClient with in-game message handling (inventory, movement,
chat, etc.) for use after the login flow completes and the client has joined
a game server room.
"""
from .login import MikmakLoginClient

class MikmakIngameClient(MikmakLoginClient):
    """Subclass of MikmakLoginClient that overrides _handle_game_messages()
    to process post-login in-game events (inventory, chat, room changes, etc.).
    """
    