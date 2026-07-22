from sentence_transformers import SentenceTransformer

from .base import EmbeddingProvider


class SentenceTransformerEmbedding(EmbeddingProvider):

    name = "sentence-transformers"

    def __init__(
        self,
        model: str = "all-MiniLM-L6-v2",
    ):

        self.model = SentenceTransformer(model)

    def embed(self, text: str):

        return self.model.encode(text).tolist()
