from fastapi import APIRouter
from .endpoints import articles, categories, sources, users, saved_articles, annotations

api_router = APIRouter()

api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(saved_articles.router, prefix="/saved", tags=["saved-articles"])
api_router.include_router(annotations.router, prefix="/annotations", tags=["annotations"])

