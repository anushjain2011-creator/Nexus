from __future__ import annotations

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """Base class for all embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        raise NotImplementedError


class EmbeddingManager:
    """
    Central embedding interface used throughout Nexus.

    Example:
        manager = EmbeddingManager()
        manager.register(OpenAIEmbedding(...))

        vector = manager.embed("Build an MVP")
    """

    def __init__(self):

        self._provider: EmbeddingProvider | None = None

    def register(self, provider: EmbeddingProvider):

        self._provider = provider

    def embed(self, text: str) -> list[float]:

        if self._provider is None:

            raise RuntimeError(
                "No embedding provider has been registered."
            )

        return self._provider.embed(text)

    @property
    def provider(self):

        return self._provider


embedding_manager = EmbeddingManager()
