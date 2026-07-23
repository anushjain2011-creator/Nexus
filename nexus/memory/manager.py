from __future__ import annotations

from .embedding import embedding_manager
from .episodic_memory import EpisodicMemory, MemoryEntry
from .retrieval import MemoryRetrieval
from .semantic_memory import SemanticMemory, MemoryFact
from .vector_store import VectorStore


class MemoryManager:

    def __init__(self):

        self.episodic = EpisodicMemory()

        self.semantic = SemanticMemory()

        self.vectors = VectorStore()

        self.retrieval = MemoryRetrieval(
            episodic=self.episodic,
            semantic=self.semantic,
            vectors=self.vectors,
            embedding_fn=embedding_manager.embed,
        )

    def remember_event(
        self,
        event: MemoryEntry,
    ):

        self.retrieval.remember_event(
            event
        )

    def remember_fact(
        self,
        fact: MemoryFact,
    ):

        self.retrieval.remember_fact(
            fact
        )

    def remember_text(
        self,
        text: str,
        metadata: dict | None = None,
    ):

        return self.retrieval.remember_vector(
            text=text,
            metadata=metadata,
        )

    def search(
        self,
        query: str,
        limit: int = 10,
    ):

        return self.retrieval.search(
            query=query,
            limit=limit,
        )

    def related(
        self,
        text: str,
        limit: int = 5,
    ):

        return self.retrieval.related(
            text=text,
            limit=limit,
        )

    def project_context(
        self,
        project_id: str,
    ):

        return self.retrieval.project_context(
            project_id
        )

    def timeline(
        self,
        project_id: str | None = None,
    ):

        return self.retrieval.timeline(
            project_id
        )

    def clear(self):

        self.retrieval.clear()
    
memory_manager = MemoryManager()
