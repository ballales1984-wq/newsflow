from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from slugify import slugify

from ....core.database import get_db
from ....models import Category
from ....models.article import Article
from ....schemas import category as schemas


@router.get("/counts")
def get_category_counts(db: Session = Depends(get_db)):
    """Return article counts per category id."""
    from sqlalchemy import func
    rows = db.query(Article.category_id, func.count(Article.id)).group_by(Article.category_id).all()
    return {str(cid): count for cid, count in rows if cid is not None}

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all categories.

    Paginato con skip/limit (default skip=0, limit=100). Non ci sono filtri
    attivi; restituisce tutte le categorie. L'ordinamento non è garantito
    dal codice: il client deve considerare l'output come non ordinato a
    meno che il database non restituisca una scansione in ordine naturale
    (che spesso corrisponde all'ID).
    """
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories


@router.get("/{category_id}", response_model=schemas.Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get single category by ID. Restituisce 404 se non trovata."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create new category (admin only).

    Genera automaticamente lo slug dal nome usando `slugify`, per avere
    URL friendlies e unici. Se uno slug esiste già, restituisce 400.
    NOTA: nessuna autenticazione è applicata nonostante il commento "admin only".
    """
    
    # Create slug
    slug = slugify(category.name)
    
    # Check if exists
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

