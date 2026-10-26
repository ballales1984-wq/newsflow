import os
import tempfile
from app.services.rag.service import RAGService


def test_rag_index_and_search():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    os.remove(path)
    svc = RAGService(path)
    svc.index_document("d1", "AI model", "Large language models run on GPU with high VRAM. CPU inference is slower.")
    svc.index_document("d2", "Hardware", "RAM capacity affects local model execution. 8 GB RAM limits model size.")
    res = svc.search("local model RAM", top_k=2)
    assert len(res) >= 1
    assert any("RAM" in r["text"] or "model" in r["text"] for r in res)
    os.remove(path)
