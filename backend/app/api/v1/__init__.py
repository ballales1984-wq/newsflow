from fastapi import APIRouter
from .endpoints import articles, categories, sources, users, saved_articles, annotations

# Composizione del router v1: ogni sottorouter viene incluso con un prefix
# specifico (es. /articles) e un tag OpenAPI (es. "articles").
# Il tag serve a raggruppare gli endpoint nella documentazione interattiva
# (/api/docs), rendendo più semplice per i consumatori dell'API trovare le
# funzionalità correlate.
# Il prefix "/api/v1" viene applicato centralized in main.py quando si include
# questo router, così tutti gli endpoint del v1 sono raggiungibili come
# /api/v1/<endpoint-prefix>/<route>.
api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(saved_articles.router, prefix="/saved", tags=["saved-articles"])
api_router.include_router(annotations.router, prefix="/annotations", tags=["annotations"])

