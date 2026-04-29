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
        self._once_handlers = {}

    def on(self, event: str) -> callable:
        def deco(fn: callable) -> callable:
            self._handlers.setdefault(event, []).append(fn)
            return fn

        return deco

    def once(self, event: str) -> callable:
        def deco(fn: callable) -> callable:
            def wrapper(*args, **kwargs):
                fn(*args, **kwargs)
                self._once_handlers[event].remove(wrapper)

            self._once_handlers.setdefault(event, []).append(wrapper)
            return wrapper

        return deco


    def emit(self, event: str, *args, **kwargs):
        for fn in self._handlers.get(event, []):
            fn(*args, **kwargs)

        for fn in self._once_handlers.get(event, []):
            fn(*args, **kwargs)
        
        self._once_handlers[event] = []
