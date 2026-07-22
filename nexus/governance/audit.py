from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class AuditEntry:

    timestamp: datetime = field(default_factory=datetime.utcnow)

    actor: str = ""

    action: str = ""

    result: str = ""

    details: dict = field(default_factory=dict)


class AuditLog:

    def __init__(self):

        self._entries = []

    def record(
        self,
        actor: str,
        action: str,
        result: str,
        details: dict | None = None,
    ):

        self._entries.append(
            AuditEntry(
                actor=actor,
                action=action,
                result=result,
                details=details or {},
            )
        )

    def all(self):

        return list(self._entries)

    def clear(self):

        self._entries.clear()
