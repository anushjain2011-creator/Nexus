"""Event bus for Nexus."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

EventListener = Callable[[Any], None]

class EventBus:
    def __init__(self) -> None:
        self.listeners: dict[str, list[EventListener]] = defaultdict(list)

    def subscribe(self, event_type: str, listener: EventListener) -> None:
        self.listeners[event_type].append(listener)

    def publish(self, event_type: str, event: Any) -> None:
        for listener in self.listeners.get(event_type, []):
            listener(event)
