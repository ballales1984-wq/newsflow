from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag.service import RAGService
from app.services.editorial import EditorialService
import os

router = APIRouter()
_store_path = os.getenv("RAG_STORE_PATH", "rag_store.json")
_embed_model = os.getenv("EMBEDDING_MODEL", "")
_api_key = os.getenv("OPENAI_API_KEY", "")
_rag = RAGService(_store_path, _embed_model, _api_key)
_svc = EditorialService(_rag)


class EditorialRequest(BaseModel):
    title: str
    text: str


@router.post("/analyze")
def analyze(req: EditorialRequest):
    return _svc.analyze(req.title, req.text)
