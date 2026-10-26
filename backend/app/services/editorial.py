from app.services.rag.service import RAGService
import os


class EditorialService:
    def __init__(self, rag: RAGService):
        self.rag = rag

    def analyze(self, title: str, text: str) -> dict:
        # retrieve related
        related = self.rag.search(title + " " + text[:200], top_k=5)
        sources = [{"title": r["metadata"].get("title"), "doc_id": r["metadata"].get("doc_id")} for r in related]
        return {
            "topic": title,
            "facts": [],
            "related_sources": sources,
            "novelty": "Da verificare",
            "synthesis": f"Sintesi basata su {len(related)} fonti recuperate.",
            "status": "bozza",
            "missing": [],
        }
