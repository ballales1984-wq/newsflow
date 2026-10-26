from fastapi import APIRouter
from .endpoints import articles, categories, sources, users, saved_articles, annotations, rag, assistant, editorial

# Main router for API v1
# All endpoints are mounted under /api/v1 (defined in main.py)
api_router = APIRouter()

# Register routers for each resource
# Each router handles CRUD operations for a specific entity
api_router.include_router(articles.router, prefix="/articles", tags=["articles"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(saved_articles.router, prefix="/saved", tags=["saved-articles"])
api_router.include_router(editorial.router, prefix="/editorial", tags=["editorial"])
