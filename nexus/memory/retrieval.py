from __future__ import annotations

from typing import Callable

from .episodic_memory import EpisodicMemory, MemoryEntry
from .semantic_memory import SemanticMemory, MemoryFact
from .vector_store import VectorStore


class MemoryRetrieval:
    """
    Combines episodic, semantic, and vector memory.

    Search priority:
        1. Semantic facts
        2. Similar vectors
        3. Event history
    """

    def __init__(
        self,
        episodic: EpisodicMemory,
        semantic: SemanticMemory,
        vectors: VectorStore,
        embedding_fn: Callable[[str], list[float]] | None = None,
    ):
        self.episodic = episodic
        self.semantic = semantic
        self.vectors = vectors
        self.embedding_fn = embedding_fn

    def search(
        self,
        query: str,
        limit: int = 10,
    ) -> dict:

        results = {
            "facts": self.semantic.search(query)[:limit],
            "events": self.episodic.search(query)[:limit],
            "vectors": [],
        }

        if self.embedding_fn:

            embedding = self.embedding_fn(query)

            results["vectors"] = self.vectors.similarity_search(
                embedding,
                limit=limit,
            )

        return results

    def project_context(
        self,
        project_id: str,
    ) -> dict:

        return {
            "facts": self.semantic.by_project(project_id),
            "events": self.episodic.by_project(project_id),
        }

    def timeline(
        self,
        project_id: str | None = None,
    ):

        if project_id:

            return sorted(
                self.episodic.by_project(project_id),
                key=lambda e: e.timestamp,
            )

        return self.episodic.timeline()

    def remember_event(
        self,
        event: MemoryEntry,
    ):

        self.episodic.add(event)

    def remember_fact(
        self,
        fact: MemoryFact,
    ):

        self.semantic.add(fact)

    def remember_vector(
        self,
        text: str,
        metadata: dict | None = None,
    ):

        if not self.embedding_fn:

            raise RuntimeError(
                "No embedding function configured."
            )

        embedding = self.embedding_fn(text)

        return self.vectors.add(
            text=text,
            embedding=embedding,
            metadata=metadata,
        )

    def related(
        self,
        text: str,
        limit: int = 5,
    ):

        if not self.embedding_fn:

            return []

        embedding = self.embedding_fn(text)

        return self.vectors.similarity_search(
            embedding,
            limit,
        )

    def clear(self):

        self.episodic.clear()
        self.semantic.clear()
        self.vectors.clear()
