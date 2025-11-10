from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....models import User
from ....schemas import user as schemas

router = APIRouter()


@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    
    # Check if user exists
    existing = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user (in production, hash password properly)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=user.password,  # TODO: Hash password
        full_name=user.full_name
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or user.hashed_password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # TODO: Create JWT token
    token = "fake-token"
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db)):
    """Get current user profile"""
    # TODO: Get from JWT token
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=schemas.User)
def update_user(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user profile"""
    # TODO: Get user from JWT token
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

