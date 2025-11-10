from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from slugify import slugify

from ....core.database import get_db
from ....models import Source
from ....schemas import source as schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Source])
def get_sources(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    db: Session = Depends(get_db)
):
    """Get all sources"""
    query = db.query(Source)
    
    if is_active is not None:
        query = query.filter(Source.is_active == is_active)
    
    sources = query.offset(skip).limit(limit).all()
    return sources


@router.get("/{source_id}", response_model=schemas.Source)
def get_source(source_id: int, db: Session = Depends(get_db)):
    """Get single source by ID"""
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.post("/", response_model=schemas.Source)
def create_source(
    source: schemas.SourceCreate,
    db: Session = Depends(get_db)
):
    """Create new source (admin only)"""
    
    slug = slugify(source.name)
    
    existing = db.query(Source).filter(Source.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source already exists")
    
    db_source = Source(
        name=source.name,
        slug=slug,
        url=source.url,
        description=source.description,
        source_type=source.source_type,
        rss_url=source.rss_url,
        api_endpoint=source.api_endpoint,
        scraper_config=source.scraper_config,
        language=source.language,
        country=source.country,
        category=source.category
    )
    
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    
    return db_source


@router.put("/{source_id}", response_model=schemas.Source)
def update_source(
    source_id: int,
    source: schemas.SourceUpdate,
    db: Session = Depends(get_db)
):
    """Update source (admin only)"""
    
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    update_data = source.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_source, field, value)
    
    db.commit()
    db.refresh(db_source)
    
    return db_source


@router.delete("/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db)):
    """Delete source (admin only)"""
    
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    db.delete(source)
    db.commit()
    
    return {"message": "Source deleted"}

