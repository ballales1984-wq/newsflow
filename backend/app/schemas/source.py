from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SourceBase(BaseModel):
    """Base source schema"""
    name: str = Field(..., min_length=1, max_length=200)
    url: str
    description: Optional[str] = None
    source_type: str = Field(..., pattern=r'^(rss|api|scraper)$')
    language: Optional[str] = None
    country: Optional[str] = None
    category: Optional[str] = None


class SourceCreate(SourceBase):
    """Schema for creating source"""
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    scraper_config: Optional[Dict[str, Any]] = None


class SourceUpdate(BaseModel):
    """Schema for updating source"""
    name: Optional[str] = None
    description: Optional[str] = None
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    scraper_config: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class Source(SourceBase):
    """Schema for source response"""
    id: int
    slug: str
    rss_url: Optional[str] = None
    api_endpoint: Optional[str] = None
    is_active: bool
    is_verified: bool
    last_collected_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

