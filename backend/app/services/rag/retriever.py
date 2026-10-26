from .store import VectorStore
from .embedder import embed_texts


class Retriever:
    def __init__(self, store: VectorStore, embed_model: str = "", api_key: str = ""):
        self.store = store
        self.embed_model = embed_model
        self.api_key = api_key

    def retrieve(self, query: str, top_k: int = 5):
        qv = embed_texts([query], self.embed_model, self.api_key)[0]
        return self.store.search(qv, top_k=top_k)
