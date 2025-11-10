from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SavedArticleBase(BaseModel):
    """Base saved article schema"""
    article_id: int


class SavedArticleCreate(SavedArticleBase):
    """Schema for saving article"""
    pass


class SavedArticle(SavedArticleBase):
    """Schema for saved article response"""
    id: int
    user_id: int
    saved_at: datetime
    is_read: bool
    is_favorite: bool
    read_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

