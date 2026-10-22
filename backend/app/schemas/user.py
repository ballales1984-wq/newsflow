from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""

    # EmailStr validates the format of the address; it needs the
    # email-validator package listed in requirements.txt.
    email: EmailStr
    # username is the public handle, between 3 and 100 characters.
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating user"""

    # The plaintext password is accepted here and hashed with bcrypt by the
    # endpoint before it reaches the ORM. It never appears in a response
    # schema.
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user"""

    # Only the profile and the settings are part of the payload: email,
    # username and password have their own flows.
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

    # Read-only view of the account. hashed_password is deliberately absent
    # from this model, so the column of the ORM object can never be serialized
    # into a response.
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

    # from_attributes lets FastAPI read the values straight from the ORM
    # instance, so the endpoint does not have to convert them by hand.
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token"""

    # token_type is the scheme the client has to use in the Authorization
    # header ("bearer"), matching the OAuth2PasswordBearer dependency.
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    # The user is embedded in the answer, so the client does not need a second
    # request after the login.
    user: User


class TokenRefresh(BaseModel):
    """Schema for token refresh"""

    refresh_token: str


class UserPreferences(BaseModel):
    """Schema for user preferences"""

    # The preferences the frontend can set; the defaults mirror the ones
    # applied when an account is created.
    theme: str = "system"
    language: str = "it"
    reading_mode: str = "auto"
    # digest_*: the daily digest mail and the hour it is sent.
    digest_enabled: bool = True
    digest_time: str = "08:00"
    # Pydantic copies the default list for every instance, so the shared
    # default is never mutated between two requests.
    categories_preferred: list[str] = []
    notifications_enabled: bool = True
    email_notifications: bool = False
    push_notifications: bool = True
