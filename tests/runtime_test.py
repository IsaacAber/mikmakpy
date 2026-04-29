from mikmakpy.ingame import MikmakIngameClient
from mikmakpy.login import MikmakLoginClient
from mikmakpy.constants import LoggerLevel, Server

from dotenv import load_dotenv
from os import getenv
from time import sleep
from threading import Timer


load_dotenv()


# def test_login_only():
#     logger_levels = set()
#     for loggingOption in LoggerLevel:
#         logger_levels.add(loggingOption)

#     client = MikmakLoginClient(
#         username=getenv("USERNAME"),
#         password=getenv("PASSWORD"),
#         logger_levels=logger_levels,
#         mac_address="00:11:22:33:44:55",  # Use a fixed MAC address for testing to ensure consistent username derivation
#         server_to_join=None,
#     )

#     @client.on("server_list")
#     def handle_server_list(msg):
#         print("Checking if the ingame state was updated with the server list info...")
#         print(f"Ingame state: {client.ingame_state}")
#         print("Login test successful, it should auto exit...")

#     client.connect()


# def test_login_to_end():
#     print(
#         "Waiting 1 seconds before starting the second login test to avoid rate limits..."
#     )
#     sleep(1)

#     logger_levels = set()
#     for loggingOption in LoggerLevel:
#         logger_levels.add(loggingOption)

#     client = MikmakLoginClient(
#         username=getenv("USERNAME"),
#         password=getenv("PASSWORD"),
#         logger_levels=logger_levels,
#         mac_address="00:11:22:33:44:55",  # Use a fixed MAC address for testing to ensure consistent username derivation
#         server_to_join=Server.KIWI,
#     )

#     @client.on("message")
#     def handle_message(msg):
#         if "action='joinOK'" in msg:
#             print("Successfully joined the game server, login test to end successful!")
#             print("Ingame state:", client.ingame_state)
#             client.disconnect()

#     client.connect()


# def test_login_limit_loop():
#     """This test checks how many login attempts can be made before rate limiting."""

#     successful_logins = 0

#     while True:
#         logger_levels = set(LoggerLevel)

#         client = MikmakLoginClient(
#             username=getenv("USERNAME"),
#             password=getenv("PASSWORD"),
#             logger_levels=logger_levels,
#             mac_address="00:11:22:33:44:55",
#             server_to_join=Server.KIWI,
#         )

#         @client.on("message")
#         def handle_message(msg):
#             nonlocal successful_logins

#             if "action='joinOK'" in msg:
#                 print(
#                     "Successfully joined the game server, login test to end successful!"
#                 )
#                 successful_logins += 1
#                 print(f"Successful logins so far: {successful_logins}")
#                 client.disconnect()
#                 sleep(
#                     1
#                 )  # Sleep for a short time to avoid hitting the server too rapidly

#         client.connect()


# def test_ingame_client():
#     """This test checks that the MikmakIngameClient can be instantiated and that
#     the _handle_game_messages method can be called without errors.
#     """
#     client = MikmakIngameClient(
#         username=getenv("USERNAME"),
#         password=getenv("PASSWORD"),
#         logger_levels=set(LoggerLevel),
#         server_to_join=Server.KIWI,
#     )

#     Timer(120, lambda: client.disconnect()).start()
#     print(
#         "Connecting with MikmakIngameClient, it should auto disconnect after 120 seconds..."
#     )

#     client.connect()
 