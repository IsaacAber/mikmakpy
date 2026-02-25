"""
mikmakpy.connection
─────────────────
Provides the Connection class for managing low-level socket communication with the Mikmak servers.
"""

from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP
import traceback
from .protocol import encode, decode


class Connection:
    def __init__(self, on_message, on_disconnect, on_connect=None):
        self._on_message = on_message
        self._on_disconnect = on_disconnect
        self._on_connect = on_connect
        self._sock: socket | None = None
        self._running = False

    def connect(self, ip: str, port: int):
        self._running = True
        self._sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self._sock.settimeout(10.0)
        self._sock.connect((ip, port))
        if self._on_connect:
            self._on_connect()

    def send(self, message: str):
        if not self._sock:
            return
        try:
            self._sock.sendall(encode.raw(message))
        except Exception as e:
            print(f"[send error] {e}")

    def listen(self):
        """Blocking receive loop. Call after connect()."""
        buffer = bytearray()
        while self._running:
            try:
                chunk = self._sock.recv(8192)
                if not chunk:
                    break
                buffer.extend(chunk)

                res = decode.buffer(buffer)
                if not res.ok:
                    print(f"\n{'='*60}")
                    print(f"[DECODE ERROR] Failed to decode buffer!")
                    print(f"Exception: {res.error}")
                    print(
                        f"Buffer content (truncated 500 chars): '{buffer[:500]}' {'(truncated)' if len(buffer) > 500 else ''}"
                    )
                    print(f"{'='*60}\n")
                    continue

                messages, buffer = res.value
                for msg in messages:
                    try:
                        self._on_message(msg)
                    except Exception as e:
                        print(f"\n{'='*60}")
                        print(f"[ERROR] Message handler crashed!")
                        print(f"{'='*60}")
                        print(f"Exception: {type(e).__name__}: {e}")
                        print(
                            f"Message that caused error: '{msg[:200]}' {'(truncated 200 chars)' if len(msg) > 200 else ''}"
                        )
                        print(f"\nFull traceback:")
                        traceback.print_exc()
                        print(f"{'='*60}\n")
            except TimeoutError:
                continue
            except Exception as e:
                print(f"\n{'='*60}")
                print(f"[RECV ERROR] Connection broken!")
                print(f"Exception: {type(e).__name__}: {e}")
                traceback.print_exc()
                print(f"{'='*60}\n")
                break

        self.close()
        self._on_disconnect()

    def close(self):
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
