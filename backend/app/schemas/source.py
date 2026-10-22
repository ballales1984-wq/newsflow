from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SourceBase(BaseModel):
    """Base source schema"""
    name: str = Field(..., min_length=1, max_length=200)
    url: str
    description: Optional[str] = None
    # source_type is restricted to the three kinds of collector the app
    # implements, so a source that could never be polled cannot be created.
    source_type: str = Field(..., pattern=r'^(rss|api|scraper)$')
    # language and country are the metadata used to filter the feed by origin
    # of the article.
    language: Optional[str] = None
    country: Optional[str] = None
    category: Optional[str] = None


class SourceCreate(SourceBase):
    """Schema for creating source"""
    # Only the field matching source_type is expected to be filled: rss_url for
    # an rss source, api_endpoint for an api source, scraper_config for a
    # scraper. The schema does not enforce that relation, the collector does.
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    scraper_config: Optional[Dict[str, Any]] = None


class SourceUpdate(BaseModel):
    """Schema for updating source"""
    # url and source_type are intentionally not updatable: changing the kind of
    # a source would orphan the collector configuration that belongs to it.
    name: Optional[str] = None
    description: Optional[str] = None
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    scraper_config: Optional[Dict[str, Any]] = None
    # is_active lets an operator pause a source without deleting it.
    is_active: Optional[bool] = None


class Source(SourceBase):
    """Schema for source response"""
    # id, slug and the operational flags are read-only: they are produced by
    # the server and by the collector.
    id: int
    slug: str
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    is_active: bool
    is_verified: bool
    # last_collected_at tells how fresh the content of the source is.
    last_collected_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

