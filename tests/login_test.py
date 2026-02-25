from mikmakpy.login import MikmakLoginClient
from mikmakpy.constants import LoggerLevel
from dotenv import load_dotenv
from os import getenv

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
        print(f"Received server list, {msg}")
        print("Login test successful, it should auto exit...")
    
    client.connect()
