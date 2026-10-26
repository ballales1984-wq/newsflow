from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from app.services.rag.service import RAGService
from app.core.config import settings

router = APIRouter()

_store_path = os.getenv("RAG_STORE_PATH", "rag_store.json")
_embed_model = os.getenv("EMBEDDING_MODEL", "")
_api_key = os.getenv("OPENAI_API_KEY", "")
_service = RAGService(_store_path, _embed_model, _api_key)


class IndexRequest(BaseModel):
    doc_id: str
    title: str
    text: str
    metadata: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/index")
def index_doc(req: IndexRequest):
    n = _service.index_document(req.doc_id, req.title, req.text, req.metadata or {})
    return {"indexed_chunks": n}


@router.post("/search")
def search(req: SearchRequest):
    results = _service.search(req.query, top_k=req.top_k)
    return {"results": results}


@router.delete("/document/{doc_id}")
def remove(doc_id: str):
    _service.remove_document(doc_id)
    return {"removed": doc_id}
