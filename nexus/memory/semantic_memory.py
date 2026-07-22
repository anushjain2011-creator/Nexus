from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class MemoryFact:
    id: str = field(default_factory=lambda: str(uuid4()))

    subject: str = ""

    predicate: str = ""

    object: str = ""

    confidence: float = 1.0

    source: str = ""

    project_id: str | None = None

    created_at: datetime = field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def statement(self) -> str:
        return f"{self.subject} {self.predicate} {self.object}"


class SemanticMemory:

    def __init__(self):

        self._facts: list[MemoryFact] = []

    def add(self, fact: MemoryFact):

        self._facts.append(fact)

    def remove(self, fact_id: str):

        self._facts = [
            f for f in self._facts
            if f.id != fact_id
        ]

    def all(self):

        return list(self._facts)

    def clear(self):

        self._facts.clear()

    def by_project(self, project_id: str):

        return [
            f
            for f in self._facts
            if f.project_id == project_id
        ]

    def by_subject(self, subject: str):

        return [
            f
            for f in self._facts
            if f.subject.lower() == subject.lower()
        ]

    def by_predicate(self, predicate: str):

        return [
            f
            for f in self._facts
            if f.predicate.lower() == predicate.lower()
        ]

    def search(self, text: str):

        text = text.lower()

        return [
            f
            for f in self._facts
            if (
                text in f.subject.lower()
                or text in f.predicate.lower()
                or text in f.object.lower()
            )
        ]

    def merge(self, facts: list[MemoryFact]):

        existing = {
            (
                f.subject,
                f.predicate,
                f.object,
            )
            for f in self._facts
        }

        for fact in facts:

            key = (
                fact.subject,
                fact.predicate,
                fact.object,
            )

            if key not in existing:

                self._facts.append(fact)

                existing.add(key)

    def top_confidence(
        self,
        minimum: float = 0.8,
    ):

        return [
            f
            for f in self._facts
            if f.confidence >= minimum
        ]

    def __len__(self):

        return len(self._facts)

    def __iter__(self):

        return iter(self._facts)
