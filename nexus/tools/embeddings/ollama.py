import requests

from .base import EmbeddingProvider


class OllamaEmbedding(EmbeddingProvider):

    def __init__(
        self,
        host="http://localhost:11434",
        model="nomic-embed-text",
    ):

        self.host = host

        self.model = model

    def embed(self, text: str):

        r = requests.post(
            f"{self.host}/api/embeddings",
            json={
                "model": self.model,
                "prompt": text,
            },
        )

        r.raise_for_status()

        return r.json()["embedding"]
