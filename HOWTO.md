# How-To

## Use the mikmakpy library

> ⚠️ Not yet in final shape — backward compatibility with older code structures is not guaranteed.

```sh
# Clone the repo
git clone https://github.com/IsaacAber/mikmakpy.git
cd mikmakpy

# Requires Python 3.14 or later
pip install .

python3.14 << 'EOF'
from mikmakpy.login import MikmakLoginClient
from mikmakpy.constants import LoggerLevel, Server

client = MikmakLoginClient(
    username="your_username",
    password="your_password",
    server_to_join=Server.KIWI,
    logger_levels={LoggerLevel.CONNECTION_CHANGE},
)

@client.on("server_list")
def on_servers(servers):
    print("Servers:", [s["name"] for s in servers])

@client.on("message")
def on_message(msg):
    print("Raw:", msg[:100])

client.connect()  # blocks until disconnected
EOF
```

For deeper examples and current usage patterns, browse the source directly at `src/mikmakpy/`.

---

## Install the MikMak 1 native Flash client

### Unix

1. Install [Bottles](https://usebottles.com/) via Flatpak:
   ```sh
   flatpak install com.usebottles.bottles
   ```
2. Create a new bottle (any type).
3. In the bottle's **Settings**, disable all Vulkan-related options (anything prefixed with `vk`, such as DXVK or VKD3D) — these break MikMak for obscure reasons.
4. If you're on a Wayland session and things don't work, try switching to an X11 session.
5. Also in **Settings**, scroll to **Environment Variables** and add:
   ```
   LANG=he_IL.UTF-8
   ```
   This enables Hebrew input inside the game client.
6. Under **Dependencies**, install `airruntime` and `allfonts` — these provide the Harman Flash SDK support and Hebrew font rendering. Skipping this step will cause the client to fail.
7. Download the MikMak 1 installer from:
   https://www.mikmak.co.il/apps/mikmakpc/
8. In Bottles, click **Install Programs** and select the downloaded `.exe`. A shortcut should appear automatically. If it doesn't, browse to:
   ```
   C:\Program Files (x86)\מיקמק\מיקמק.exe
   ```
   and add it manually via **Add Shortcuts**.

### Windows

1. Install the Harman Adobe AIR runtime:
   https://airsdk.harman.com/runtime
2. Download and install the MikMak 1 client:
   https://www.mikmak.co.il/apps/mikmakpc/

---

## Sniff, analyze & implement the protocol

An AI-generated sniffer script is included at `src/tools/sniffer.py` — it captures MikMak socket traffic exclusively and produces an HTML report you can open in the browser to inspect the full traffic flow with clarity.

Run it with admin privileges while the game client is open (or launch the client afterward). Once you've identified the structure of an `XT` or `SYS` packet, try decomposing it in line with the existing code style. A complete contribution covers three parts: a test, a parser, and a state-friendly emitted event or in-game state update.

If you get all three working — pull request it. Discord: `isaacaber`

Side note: if `sniffer.py` or `mikcli.py` isn't working that well, just take the version before this commit because I made claude shorten both of them to make them more elegant (I honestly can't tell what's going in my mind rn)
SAYONARA