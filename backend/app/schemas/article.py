from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArticleBase(BaseModel):
    """Base article schema"""
    title: str = Field(..., min_length=1, max_length=500)
    url: str
    summary: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    image_url: Optional[str] = None


class ArticleCreate(ArticleBase):
    """Schema for creating article"""
    source_id: int
    category_id: Optional[int] = None


class ArticleUpdate(BaseModel):
    """Schema for updating article"""
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_archived: Optional[bool] = None


class Article(ArticleBase):
    """Schema for article response"""
    id: int
    slug: str
    source_id: int
    category_id: Optional[int] = None
    language: Optional[str] = None
    keywords: Optional[List[str]] = None
    entities: Optional[Dict[str, Any]] = None
    sentiment_score: Optional[float] = None
    relevance_score: Optional[float] = None
    quality_score: Optional[float] = None
    word_count: Optional[int] = None
    reading_time_minutes: Optional[int] = None
    tags: Optional[List[str]] = None
    is_featured: bool = False
    is_verified: bool = False
    is_archived: bool = False
    collected_at: datetime
    
    class Config:
        from_attributes = True


class ArticleList(BaseModel):
    """Schema for paginated article list"""
    items: List[Article]
    total: int
    page: int
    size: int
    pages: int


class ArticleSearch(BaseModel):
    """Schema for article search"""
    query: Optional[str] = None
    category_id: Optional[int] = None
    source_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_quality_score: Optional[float] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None

