import requests

from .base import EmbeddingProvider


class LMStudioEmbedding(EmbeddingProvider):

    name = "lmstudio"

    def __init__(
        self,
        model: str,
        host: str = "http://localhost:1234/v1",
    ):

        self.model = model
        self.host = host

    def embed(self, text: str):

        response = requests.post(
            f"{self.host}/embeddings",
            json={
                "model": self.model,
                "input": text,
            },
            timeout=30,
        )

        response.raise_for_status()

        return response.json()["data"][0]["embedding"]
