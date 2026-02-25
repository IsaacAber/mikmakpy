"""
mikmakpy.ingame
─────────────────

"""
from .login import MikmakLoginClient

class MikmakIngameClient(MikmakLoginClient):
    """
    MikmakIngameClient extends MikmakLoginClient to handle in-game events and interactions after successfully logging in and joining a game server. It provides additional functionality for parsing in-game messages, managing the game state, and responding to various in-game events such as room lists, inventory updates, and more. This class is designed to be used after the initial login process is complete and the client has switched to the game server.
    """
    