"""
mikmakpy.connection
─────────────────
Low-level TCP socket wrapper. Handles connecting, sending, and a blocking
receive loop that splits null-terminated messages and dispatches them
via callbacks. Used internally by MikmakLoginClient.
"""

from collections.abc import Callable
from socket import socket, AF_INET, SOCK_STREAM, IPPROTO_TCP
import traceback
from .protocol import encode, decode


class Connection:
    def __init__(self, on_message: Callable, on_connect: Callable | None = None):
        self._on_message = on_message
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
        """Fire-and-forget: silently fails if socket is dead so callers don't need to guard every send."""
        if not self._sock:
            return
        try:
            self._sock.sendall(encode.raw(message))
        except Exception as e:
            print(f"[send error] {e}")

    def listen(self):
        """Blocking receive loop. Call after connect().

        Exception contract:
        - TimeoutError from recv()  → expected (settimeout), just retry.
        - Exception in on_message() → logged here so one bad message doesn't kill the connection.
        - Everything else (socket broken, KeyboardInterrupt, etc.) → propagates to caller.
        - finally → always closes the socket.
        """
        buffer = bytearray()
        try:
            while self._running:
                try:
                    chunk = self._sock.recv(8192)
                except TimeoutError:
                    continue  # settimeout(10) fires here regularly, just retry
                except OSError:
                    break  # socket closed from another thread (e.g. disconnect timer)

                if not chunk:
                    break  # server closed connection gracefully
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
                    try:  # isolate handler crashes so one bad message doesn't kill the connection
                        self._on_message(msg)
                    except Exception as e:
                        print(f"\n{'='*60}")
                        print(f"[ERROR] Message handler crashed!")
                        print(f"Exception: {type(e).__name__}: {e}")
                        print(
                            f"Message that caused error: '{msg[:200]}' {'(truncated 200 chars)' if len(msg) > 200 else ''}"
                        )
                        print(f"\nFull traceback:")
                        traceback.print_exc()
                        print(f"{'='*60}\n")
        finally:
            self.close()

    def close(self):
        """Idempotent — safe to call multiple times or on an already-dead socket."""
        self._running = False
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
