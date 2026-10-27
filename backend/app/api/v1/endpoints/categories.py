from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from slugify import slugify

from ....core.database import get_db
from ....core.constants import DEFAULT_CATEGORIES
from ....models import Category
from ....models.article import Article
from ....schemas import category as schemas


router = APIRouter()


@router.get("/counts")
def get_category_counts(db: Session = Depends(get_db)):
    """Return article counts per category.
    
    Uses a GROUP BY query on category_id to get the number of articles
    in each category. Filters out NULL category_id to exclude uncategorized articles.
    """
    from sqlalchemy import func
    rows = db.query(Article.category_id, func.count(Article.id)).group_by(Article.category_id).all()
    return {str(cid): count for cid, count in rows if cid is not None}


@router.get("/", response_model=List[schemas.Category])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all categories with pagination.

    Args:
        skip: Number of elements to skip (offset)
        limit: Maximum number of elements to return
        db: Database session injected by FastAPI

    Returns:
        List of categories in the system
    """
    categories = db.query(Category).offset(skip).limit(limit).all()
    if not categories and skip == 0:
        return [schemas.Category(**c) for c in DEFAULT_CATEGORIES[:limit]]
    return categories


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a single category by ID.
    
    Args:
        category_id: Unique ID of the category
        db: Database session

    Returns:
        Category data

    Raises:
        HTTPException: 404 if category doesn't exist
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new category (admin only).

    Automatically generates a URL-friendly slug from the name using slugify.
    Checks if slug already exists.

    Args:
        category: Category data to create
        db: Database session

    Returns:
        Newly created category

    Raises:
        HTTPException: 400 if a category with the same slug already exists
    """
    
    # Generate URL-friendly slug from category name
    slug = slugify(category.name)
    
    # Check if category with same slug already exists
    existing = db.query(Category).filter(Category.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = Category(
        name=category.name,
        slug=slug,
        description=category.description,
        icon=category.icon,
        color=category.color
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryUpdate,
    db: Session = Depends(get_db)
):
    """Update category (admin only). Anche qui manca un auth dependency."""
    
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    # Update slug if name changed
    if 'name' in update_data:
        db_category.slug = slugify(update_data['name'])
    
    db.commit()
    db.refresh(db_category)
    
    return db_category


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete category (admin only). Anche qui manca un auth dependency.

    Restituisce 200 con un JSON di conferma, non 204 (nessun body).
    """
    
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted"}

