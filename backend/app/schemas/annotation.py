from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AnnotationBase(BaseModel):
    """Base annotation schema"""
    title: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1)


class AnnotationCreate(AnnotationBase):
    """Schema for creating annotation"""
    article_id: int


class AnnotationUpdate(BaseModel):
    """Schema for updating annotation"""
    title: Optional[str] = None
    content: Optional[str] = None


class Annotation(AnnotationBase):
    """Schema for annotation response"""
    id: int
    user_id: int
    article_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

