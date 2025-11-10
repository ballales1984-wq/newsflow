from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....core.database import get_db
from ....models import Annotation, Article, User
from ....schemas import annotation as schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.Annotation])
def get_annotations(
    article_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get user's annotations"""
    # TODO: Get user from JWT
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    query = db.query(Annotation).filter(Annotation.user_id == user.id)
    
    if article_id:
        query = query.filter(Annotation.article_id == article_id)
    
    annotations = query.order_by(Annotation.created_at.desc()).offset(skip).limit(limit).all()
    return annotations


@router.post("/", response_model=schemas.Annotation)
def create_annotation(
    annotation: schemas.AnnotationCreate,
    db: Session = Depends(get_db)
):
    """Create annotation for article"""
    # TODO: Get user from JWT
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if article exists
    article = db.query(Article).filter(Article.id == annotation.article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db_annotation = Annotation(
        user_id=user.id,
        article_id=annotation.article_id,
        title=annotation.title,
        content=annotation.content
    )
    
    db.add(db_annotation)
    db.commit()
    db.refresh(db_annotation)
    
    return db_annotation


@router.put("/{annotation_id}", response_model=schemas.Annotation)
def update_annotation(
    annotation_id: int,
    annotation: schemas.AnnotationUpdate,
    db: Session = Depends(get_db)
):
    """Update annotation"""
    db_annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not db_annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    
    update_data = annotation.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_annotation, field, value)
    
    db.commit()
    db.refresh(db_annotation)
    
    return db_annotation


@router.delete("/{annotation_id}")
def delete_annotation(annotation_id: int, db: Session = Depends(get_db)):
    """Delete annotation"""
    annotation = db.query(Annotation).filter(Annotation.id == annotation_id).first()
    if not annotation:
        raise HTTPException(status_code=404, detail="Annotation not found")
    
    db.delete(annotation)
    db.commit()
    
    return {"message": "Annotation deleted"}

