from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    """Base category schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class CategoryCreate(CategoryBase):
    """Schema for creating category"""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating category"""
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class Category(CategoryBase):
    """Schema for category response"""
    id: int
    slug: str
    
    class Config:
        from_attributes = True

