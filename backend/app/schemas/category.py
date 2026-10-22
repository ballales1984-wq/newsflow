from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    """Base category schema"""
    # The slug is not part of the writable fields: it is derived from the name
    # on the server, so two callers cannot create the same category with two
    # different slugs.
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = None
    # color is restricted to a six digit hex triplet, which matches the
    # String(7) column of the model ('#' plus six hex digits).
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class CategoryCreate(CategoryBase):
    """Schema for creating category"""
    # Same fields as the base: a category is created with exactly the values it
    # exposes.
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating category"""
    # Partial update: all the fields are optional, and as for the other update
    # models the endpoint has to apply only the fields that were really sent
    # (exclude_unset) instead of overwriting the missing ones with null.
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class Category(CategoryBase):
    """Schema for category response"""
    # id and slug are added by the server and are read-only.
    id: int
    slug: str
    
    class Config:
        from_attributes = True

