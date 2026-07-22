from __future__ import annotations

from openai import OpenAI

from memory.embedding import EmbeddingProvider


class OpenAIEmbedding(EmbeddingProvider):

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
    ):

        self.client = OpenAI(api_key=api_key)

        self.model = model

    def embed(self, text: str) -> list[float]:

        response = self.client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding
