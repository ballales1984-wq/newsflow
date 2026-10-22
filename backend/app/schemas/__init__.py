# Public surface of the schema layer. Three kinds of schema per entity, with a
# fixed convention:
#   *Create    - payload accepted to insert a new row,
#   *Update    - payload accepted to patch an existing row (all fields optional),
#   *<Entity>  - payload returned to the client, built from the ORM object.
# Importing them from here keeps the endpoints free of per-module imports.
from .article import Article, ArticleCreate, ArticleUpdate, ArticleList
from .category import Category, CategoryCreate, CategoryUpdate
from .source import Source, SourceCreate, SourceUpdate
from .user import (
    User,
    UserCreate,
    UserUpdate,
    UserLogin,
    Token,
    TokenRefresh,
    UserPreferences,
)
from .saved_article import SavedArticle, SavedArticleCreate
from .annotation import Annotation, AnnotationCreate, AnnotationUpdate

# Explicit __all__: it documents the public surface of the package and keeps
# `from app.schemas import *` deterministic.
__all__ = [
    "Article",
    "ArticleCreate",
    "ArticleUpdate",
    "ArticleList",
    "Category",
    "CategoryCreate",
    "CategoryUpdate",
    "Source",
    "SourceCreate",
    "SourceUpdate",
    "User",
    "UserCreate",
    "UserUpdate",
    "UserLogin",
    "Token",
    "TokenRefresh",
    "UserPreferences",
    "SavedArticle",
    "SavedArticleCreate",
    "Annotation",
    "AnnotationCreate",
    "AnnotationUpdate",
]
# Note: ArticleSearch is defined in schemas/article.py but is not re-exported
# here; the endpoints import it from the module directly.
