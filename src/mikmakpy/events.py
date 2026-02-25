"""
mikmakpy.events
─────────────────
Provides an event bus for handling in-game events and interactions.
"""


class EventBus:
    def __init__(self):
        self._handlers = {}

    def on(self, event: str):
        def decorator(fn):
            self._handlers.setdefault(event, []).append(fn)
            return fn

        return decorator

    def emit(self, event: str, *args, **kwargs):
        for fn in self._handlers.get(event, []):
            fn(*args, **kwargs)
