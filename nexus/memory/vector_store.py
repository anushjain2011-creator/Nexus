from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class VectorRecord:
    id: str = field(default_factory=lambda: str(uuid4()))

    text: str = ""

    embedding: list[float] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)


class VectorStore:
    """
    Simple in-memory vector store.

    Replace this later with:
        - FAISS
        - ChromaDB
        - Pinecone
        - Weaviate
        - pgvector
    """

    def __init__(self):

        self._vectors: dict[str, VectorRecord] = {}

    def add(
        self,
        text: str,
        embedding: list[float],
        metadata: dict[str, Any] | None = None,
    ) -> str:

        record = VectorRecord(
            text=text,
            embedding=embedding,
            metadata=metadata or {},
        )

        self._vectors[record.id] = record

        return record.id

    def get(self, vector_id: str) -> VectorRecord | None:

        return self._vectors.get(vector_id)

    def delete(self, vector_id: str):

        self._vectors.pop(vector_id, None)

    def clear(self):

        self._vectors.clear()

    def all(self):

        return list(self._vectors.values())

    def similarity_search(
        self,
        embedding: list[float],
        limit: int = 5,
    ):

        scored = []

        for record in self._vectors.values():

            score = self.cosine_similarity(
                embedding,
                record.embedding,
            )

            scored.append((score, record))

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            record
            for _, record in scored[:limit]
        ]

    @staticmethod
    def cosine_similarity(
        a: list[float],
        b: list[float],
    ) -> float:

        if len(a) != len(b):

            raise ValueError(
                "Embedding dimensions must match."
            )

        dot = sum(x * y for x, y in zip(a, b))

        mag_a = sqrt(sum(x * x for x in a))

        mag_b = sqrt(sum(y * y for y in b))

        if mag_a == 0 or mag_b == 0:

            return 0.0

        return dot / (mag_a * mag_b)

    def __len__(self):

        return len(self._vectors)

    def __iter__(self):

        return iter(self._vectors.values())
