from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ....core.database import get_db
from ....models import SavedArticle, Article, User
from ....schemas import saved_article as schemas

router = APIRouter()

# All read/write paths return 404 for missing resources; 403 is not used
# here because row ownership is enforced through the user_id filter once JWT
# authentication is wired in (currently the user placeholder resolves to the
# first row in the table).


@router.get("/", response_model=List[schemas.SavedArticle])
def get_saved_articles(
    skip: int = 0,
    limit: int = 100,
    is_read: bool = None,
    is_favorite: bool = None,
    db: Session = Depends(get_db)
):
    """Get user's saved articles"""
    # TODO: Get user from JWT
    # Placeholder: the user is not yet resolved from the JWT (TODO above),
    # so the first user row is used until authentication is wired in.
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ownership check: only SavedArticle rows belonging to this user are
    # returned, so one user cannot list another's archive.
    query = db.query(SavedArticle).filter(SavedArticle.user_id == user.id)
    
    if is_read is not None:
        query = query.filter(SavedArticle.is_read == is_read)
    if is_favorite is not None:
        query = query.filter(SavedArticle.is_favorite == is_favorite)
    
    saved = query.order_by(SavedArticle.saved_at.desc()).offset(skip).limit(limit).all()
    return saved


@router.post("/", response_model=schemas.SavedArticle)
def save_article(
    saved: schemas.SavedArticleCreate,
    db: Session = Depends(get_db)
):
    """Save article to user's archive"""
    # TODO: Get user from JWT
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if article exists
    article = db.query(Article).filter(Article.id == saved.article_id).first()
    # 404 when the source article does not exist; distinct from the saved
    # row itself being missing.
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Check if already saved
    # The (user_id, article_id) pair acts as a uniqueness guard: if the
    # article is already saved, return the existing row rather than creating
    # a duplicate archive entry.
    existing = db.query(SavedArticle).filter(
        SavedArticle.user_id == user.id,
        SavedArticle.article_id == saved.article_id
    ).first()
    
    if existing:
        return existing
    
    # Create saved article
    db_saved = SavedArticle(
        user_id=user.id,
        article_id=saved.article_id
    )
    
    db.add(db_saved)
    db.commit()
    db.refresh(db_saved)
    
    return db_saved


@router.put("/{saved_id}/read")
def mark_as_read(saved_id: int, db: Session = Depends(get_db)):
    """Mark saved article as read"""
    # 404 when the saved-article row itself does not exist; note the row is
    # located by id only with no additional ownership check beyond the user
    # filter applied once JWT auth is wired in.
    saved = db.query(SavedArticle).filter(SavedArticle.id == saved_id).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved article not found")
    
    saved.is_read = True
    saved.read_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Marked as read"}


@router.put("/{saved_id}/favorite")
def toggle_favorite(saved_id: int, db: Session = Depends(get_db)):
    """Toggle favorite status"""
    saved = db.query(SavedArticle).filter(SavedArticle.id == saved_id).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved article not found")
    
    saved.is_favorite = not saved.is_favorite
    
    db.commit()
    
    return {"message": "Favorite toggled", "is_favorite": saved.is_favorite}


@router.delete("/{saved_id}")
def remove_saved_article(saved_id: int, db: Session = Depends(get_db)):
    """Remove article from saved list"""
    saved = db.query(SavedArticle).filter(SavedArticle.id == saved_id).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved article not found")
    
    db.delete(saved)
    db.commit()
    
    return {"message": "Article removed from saved list"}

