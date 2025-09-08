from typing import Any, Callable, Dict, List, Type


class EventBus:
    def __init__(self):
        self._subscribers: Dict[Type, List[Callable]] = {}

    def subscribe(self, event_type: Type, handler: Callable[[Any], None]):
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: Any):
        for handler in self._subscribers.get(type(event), []):
            handler(event)
