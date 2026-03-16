"""
mikmakpy.events
─────────────────
Minimal event bus. Register handlers with @client.on('event_name')
and dispatch with client.emit('event_name', *args).
Base class for MikmakLoginClient.
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
