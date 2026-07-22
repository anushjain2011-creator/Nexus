from .base import EmbeddingProvider


class EmbeddingManager:

    def __init__(self):

        self.provider: EmbeddingProvider | None = None

    def register(self, provider: EmbeddingProvider):

        self.provider = provider

    def embed(self, text: str) -> list[float]:

        if self.provider is None:
            raise RuntimeError(
                "No embedding provider registered."
            )

        return self.provider.embed(text)


embedding_manager = EmbeddingManager()
