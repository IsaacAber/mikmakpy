from mikmakpy.login import MikmakLoginClient
from mikmakpy.constants import LoggerLevel, Server

from dotenv import load_dotenv
from os import getenv
from time import sleep

load_dotenv()


def test_login_only():
    logger_levels = set()
    for loggingOption in LoggerLevel:
        logger_levels.add(loggingOption)

    client = MikmakLoginClient(
        username=getenv("USERNAME", ""),
        password=getenv("PASSWORD", ""),
        logger_levels=logger_levels,
        server_to_join=None,
    )

    @client.on("server_list")
    def handle_server_list(msg):
        print("Checking if the ingame state was updated with the server list info...")
        print(f"Ingame state: {client.ingame_state}")
        print("Login test successful, it should auto exit...")

    client.connect()


def test_login_to_end():
    print("Waiting 5 seconds before starting the second login test to avoid rate limits...")
    sleep(5)

    logger_levels = set()
    for loggingOption in LoggerLevel:
        logger_levels.add(loggingOption)

    client = MikmakLoginClient(
        username=getenv("USERNAME", ""),
        password=getenv("PASSWORD", ""),
        logger_levels=logger_levels,
        server_to_join=Server.KIWI,
    )

    @client.on("message")
    def handle_message(msg):
        if "action='joinOK'" in msg:
            print("Successfully joined the game server, login test to end successful!")
            print("Ingame state:", client.ingame_state)
            client.disconnect()

    client.connect()
