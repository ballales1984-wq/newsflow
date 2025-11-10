from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ....core.database import get_db
from ....models import Article
from ....schemas import article as schemas
from ....services.tasks import collect_from_source

router = APIRouter()


@router.get("/", response_model=schemas.ArticleList)
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category_id: Optional[int] = None,
    source_id: Optional[int] = None,
    language: Optional[str] = None,
    date_from: Optional[datetime] = None,
    is_featured: Optional[bool] = None,
    min_quality_score: Optional[float] = Query(None, ge=0, le=1),
    db: Session = Depends(get_db)
):
    """Get paginated list of articles with filters"""
    
    query = db.query(Article).filter(Article.is_archived == False)
    
    # Apply filters
    if category_id:
        query = query.filter(Article.category_id == category_id)
    if source_id:
        query = query.filter(Article.source_id == source_id)
    if language:
        query = query.filter(Article.language == language)
    if date_from:
        query = query.filter(Article.published_at >= date_from)
    if is_featured is not None:
        query = query.filter(Article.is_featured == is_featured)
    if min_quality_score is not None:
        query = query.filter(Article.quality_score >= min_quality_score)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "items": articles,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{article_id}", response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get single article by ID"""
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return article


@router.get("/slug/{slug}", response_model=schemas.Article)
def get_article_by_slug(slug: str, db: Session = Depends(get_db)):
    """Get single article by slug"""
    
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return article


@router.post("/search", response_model=schemas.ArticleList)
def search_articles(
    search: schemas.ArticleSearch,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search articles with advanced filters"""
    
    query = db.query(Article).filter(Article.is_archived == False)
    
    # Text search in title and content
    if search.query:
        search_term = f"%{search.query}%"
        query = query.filter(
            (Article.title.ilike(search_term)) |
            (Article.summary.ilike(search_term))
        )
    
    # Apply filters
    if search.category_id:
        query = query.filter(Article.category_id == search.category_id)
    if search.source_id:
        query = query.filter(Article.source_id == search.source_id)
    if search.language:
        query = query.filter(Article.language == search.language)
    if search.date_from:
        query = query.filter(Article.published_at >= search.date_from)
    if search.date_to:
        query = query.filter(Article.published_at <= search.date_to)
    if search.min_quality_score:
        query = query.filter(Article.quality_score >= search.min_quality_score)
    
    # Get total count
    total = query.count()
    
    # Get paginated results
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "items": articles,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }


@router.put("/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: int,
    article_update: schemas.ArticleUpdate,
    db: Session = Depends(get_db)
):
    """Update article (admin only)"""
    
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Update fields
    update_data = article_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    
    return article


@router.get("/featured/list", response_model=List[schemas.Article])
def get_featured_articles(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get featured articles"""
    
    articles = db.query(Article).filter(
        Article.is_featured == True,
        Article.is_archived == False
    ).order_by(Article.published_at.desc()).limit(limit).all()
    
    return articles


@router.get("/recent/list", response_model=List[schemas.Article])
def get_recent_articles(
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get recent articles from last N days"""
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    articles = db.query(Article).filter(
        Article.published_at >= cutoff_date,
        Article.is_archived == False
    ).order_by(Article.published_at.desc()).limit(limit).all()
    
    return articles


@router.post("/collect/{source_id}")
def trigger_collection(source_id: int):
    """Trigger news collection for specific source (admin only)"""
    
    # Trigger async task
    task = collect_from_source.delay(source_id)
    
    return {"message": "Collection started", "task_id": task.id}

