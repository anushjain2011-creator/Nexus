from __future__ import annotations

import requests

from memory.embedding import EmbeddingProvider


class OllamaEmbedding(EmbeddingProvider):

    def __init__(
        self,
        model: str = "nomic-embed-text",
        host: str = "http://localhost:11434",
    ):

        self.model = model

        self.host = host

    def embed(self, text: str) -> list[float]:

        response = requests.post(
            f"{self.host}/api/embeddings",
            json={
                "model": self.model,
                "prompt": text,
            },
        )

        response.raise_for_status()

        return response.json()["embedding"]
