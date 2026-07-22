import voyageai

from .base import EmbeddingProvider


class VoyageEmbedding(EmbeddingProvider):

    name = "voyage"

    def __init__(
        self,
        api_key: str,
        model: str = "voyage-3-lite",
    ):

        self.client = voyageai.Client(api_key=api_key)
        self.model = model

    def embed(self, text: str):

        response = self.client.embed(
            [text],
