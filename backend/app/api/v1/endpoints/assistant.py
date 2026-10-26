from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from app.core.database import get_db
from app.models.article import Article
from app.services.rag.service import RAGService
import os

router = APIRouter()
_store_path = os.getenv("RAG_STORE_PATH", "rag_store.json")
_embed_model = os.getenv("EMBEDDING_MODEL", "")
_api_key = os.getenv("OPENAI_API_KEY", "")
_service = RAGService(_store_path, _embed_model, _api_key)


class AskRequest(BaseModel):
    question: str
    top_k: int = 5


@router.post("/ask")
def ask(req: AskRequest):
    results = _service.search(req.question, top_k=req.top_k)
    sources = [
        {"title": r["metadata"].get("title"), "doc_id": r["metadata"].get("doc_id"), "snippet": r["text"]}
        for r in results
    ]
    if not sources:
        return {"answer": "Nessuna informazione sufficiente nell'archivio.", "sources": []}
    # Build a grounded answer from retrieved passages
    answer = "Risposta basata sui passaggi recuperati:\n" + "\n".join(f"- {s['snippet']}" for s in sources[:3])
    return {"answer": answer, "sources": sources}


@router.post("/index-articles")
def index_articles(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    count = 0
    for a in articles:
        text = (a.summary or "") + "\n" + (a.content or "")
        _service.index_document(str(a.id), a.title, text, {"url": a.url, "category_id": a.category_id})
        count += 1
    return {"indexed_articles": count}
