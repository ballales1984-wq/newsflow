from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating user"""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user"""

    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    notification_settings: Optional[Dict[str, Any]] = None
    reading_mode: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login"""

    email: EmailStr
    password: str


class User(UserBase):
    """Schema for user response"""

    id: int
    avatar_url: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    notification_settings: Optional[Dict[str, Any]] = None
    reading_mode: str
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token"""

    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    user: User


class TokenRefresh(BaseModel):
    """Schema for token refresh"""

    refresh_token: str


class UserPreferences(BaseModel):
    """Schema for user preferences"""

    theme: str = "system"
    language: str = "it"
    reading_mode: str = "auto"
    digest_enabled: bool = True
    digest_time: str = "08:00"
    categories_preferred: list[str] = []
    notifications_enabled: bool = True
    email_notifications: bool = False
    push_notifications: bool = True
