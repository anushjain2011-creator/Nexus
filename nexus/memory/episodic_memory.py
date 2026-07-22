from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class MemoryEntry:
    id: str = field(default_factory=lambda: str(uuid4()))

    timestamp: datetime = field(default_factory=datetime.utcnow)

    event_type: str = ""

    source: str = ""

    project_id: str | None = None

    importance: float = 0.5

    data: dict[str, Any] = field(default_factory=dict)

    tags: set[str] = field(default_factory=set)


class EpisodicMemory:

    def __init__(self):

        self._entries: list[MemoryEntry] = []

    def add(self, entry: MemoryEntry):

        self._entries.append(entry)

        self._entries.sort(
            key=lambda e: e.timestamp
        )

    def recent(self, limit: int = 20):

        return self._entries[-limit:]

    def by_project(self, project_id: str):

        return [
            e
            for e in self._entries
            if e.project_id == project_id
        ]

    def by_event(self, event_type: str):

        return [
            e
            for e in self._entries
            if e.event_type == event_type
        ]

    def search(self, text: str):

        text = text.lower()

        return [
            e
            for e in self._entries
            if text in str(e.data).lower()
        ]

    def important(self, threshold: float = 0.8):

        return [
            e
            for e in self._entries
            if e.importance >= threshold
        ]

    def timeline(self):

        return sorted(
            self._entries,
            key=lambda e: e.timestamp
        )

    def clear(self):

        self._entries.clear()

    def __len__(self):

        return len(self._entries)

    def __iter__(self):

        return iter(self._entries)
