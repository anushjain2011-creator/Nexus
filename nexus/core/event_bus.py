"""
EventBus — lets agents react to things other agents (or the system) did,
without being directly wired together. This is what powers cascades like:

    BudgetExceeded -> Finance Agent -> Risk Agent -> Planning Agent

Deliberately synchronous and in-process for the hackathon MVP. Swappable
later for a real broker (e.g. Sub0 events, Redis streams, etc.) behind the
same publish/subscribe interface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass
class Event:
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)
    at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


Handler = Callable[[Event], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = {}
        self._history: list[Event] = []

    def subscribe(self, kind: str, handler: Handler) -> None:
        """Register a handler for a given event kind, e.g. 'task.blocked'.
        Use '*' to subscribe to all events."""
        self._handlers.setdefault(kind, []).append(handler)

    def publish(self, kind: str, **payload: Any) -> Event:
        event = Event(kind=kind, payload=payload)
        self._history.append(event)

        for handler in self._handlers.get(kind, []):
            handler(event)
        for handler in self._handlers.get("*", []):
            handler(event)

        return event

    @property
    def history(self) -> list[Event]:
        return list(self._history)
