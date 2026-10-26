import os
import uuid
from typing import List, Dict, Any

from .chunker import chunk_text
from .embedder import embed_texts
from .store import VectorStore
from .retriever import Retriever


class RAGService:
    def __init__(self, store_path: str, embed_model: str = "", api_key: str = ""):
        self.store = VectorStore(store_path)
        self.embed_model = embed_model
        self.api_key = api_key
        self.retriever = Retriever(self.store, embed_model, api_key)

    def index_document(self, doc_id: str, title: str, text: str, metadata: Dict[str, Any] = None) -> int:
        metadata = metadata or {}
        chunks = chunk_text(text)
        embeddings = embed_texts(chunks, self.embed_model, self.api_key)
        items = []
        for i, (c, e) in enumerate(zip(chunks, embeddings)):
            items.append({
                "id": f"{doc_id}::chunk::{i}",
                "text": c,
                "embedding": e,
                "metadata": {"doc_id": doc_id, "title": title, "chunk_index": i, **metadata},
            })
        self.store.add(items)
        return len(items)

    def remove_document(self, doc_id: str):
        ids = [d["id"] for d in []]
        # find ids
        target = [d["id"] for d in self.store._data if d["metadata"].get("doc_id") == doc_id]
        self.store.remove(target)

    def search(self, query: str, top_k: int = 5):
        return self.retriever.retrieve(query, top_k=top_k)
