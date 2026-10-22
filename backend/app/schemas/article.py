from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime


class ArticleBase(BaseModel):
    """Base article schema"""
    # Fields shared by the create and the response schema. The limits of title
    # mirror the String(500) column of the model, so a request can never
    # produce a value the database would reject.
    title: str = Field(..., min_length=1, max_length=500)
    # url is declared as a plain string (the HttpUrl type is imported in this
    # module but not used), so the schema does not enforce an http(s) URL here.
    url: str
    summary: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    image_url: Optional[str] = None


class ArticleCreate(ArticleBase):
    """Schema for creating article"""
    # source_id is mandatory: an article without a publisher cannot be
    # attributed nor re-collected.
    source_id: int
    # category_id is optional because the classification happens after the
    # insert.
    category_id: Optional[int] = None


class ArticleUpdate(BaseModel):
    """Schema for updating article"""
    # Every field is optional, so this model describes a partial update. A
    # field that was simply not sent is indistinguishable from a field that
    # was explicitly sent as null, so the endpoint has to work with
    # model_dump(exclude_unset=True) to know what to apply.
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_archived: Optional[bool] = None


class Article(ArticleBase):
    """Schema for article response"""
    # Read-only part of the response: identifiers, computed NLP values and the
    # editorial flags are produced by the server and are never accepted from
    # the client.
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
    
    # from_attributes lets FastAPI read the values straight from the ORM
    # instance, so the endpoint does not have to convert them by hand.
    class Config:
        from_attributes = True


class ArticleList(BaseModel):
    """Schema for paginated article list"""
    # Envelope of the paginated feed: items holds the page, total the number of
    # matching rows, page and size the echo of the requested window and pages
    # the number of pages derived from them.
    items: List[Article]
    total: int
    page: int
    size: int
    pages: int


class ArticleSearch(BaseModel):
    """Schema for article search"""
    # Filter-only model: every criterion is optional, so an empty search is a
    # valid request and returns the unfiltered feed.
    # min_quality_score is compared with Article.quality_score, whose range is
    # 0 to 1.
    query: Optional[str] = None
    category_id: Optional[int] = None
    source_id: Optional[int] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_quality_score: Optional[float] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None

