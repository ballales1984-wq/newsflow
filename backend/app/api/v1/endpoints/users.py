from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    generate_api_key,
)
from ....core.config import settings
from ....models import User
from ....schemas import user as schemas

router = APIRouter()


@router.post(
    "/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED
)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    existing = db.query(User).filter(User.email == user.email).first()
    # 400: the email is already taken; registration fails fast instead of
    # creating a duplicate account.
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        reading_mode="morning",
        preferences={"theme": "system", "language": "it", "categories_preferred": []},
        notification_settings={
            "digest_enabled": True,
            "push_enabled": True,
            "email_enabled": False,
        },
        # Preferences live in a JSON blob alongside theme and language; this
        # same blob later stores the user's API key.
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Login user with email/password"""
    user = db.query(User).filter(User.email == form_data.username).first()

    # 401: credentials invalid or user missing; WWW-Authenticate header
    # prompts the client to retry with fresh credentials.
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 403: the account exists but is disabled, distinct from bad credentials
    # (401) so clients can surface the right message.
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled"
        )

    access_token = create_access_token(
        # Access token is short-lived (minutes, from settings); the refresh
        # token is longer-lived and is used to obtain new access tokens
        # without re-entering the password.
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    # Refresh token issued at login; it is rotated (replaced) on every
    # /refresh call so a stolen refresh token has a limited lifespan.

    # Records the last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(token_data: schemas.TokenRefresh, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    payload = decode_token(token_data.refresh_token)

    # Only tokens typed "refresh" are accepted here; an access token cannot
    # be used to refresh, limiting the damage of a leaked token.
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user or not user.is_active:
        # 401: invalid refresh token, or the user is missing/disabled.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or disabled",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    # Rotate the refresh token on every use: issue a new one so the old
    # value should be discarded by the client, shrinking the theft window.
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "user": user,
    }


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    # Stateless JWT logout: the server only tells the client to discard its
    # tokens; there is no token blacklist or revocation here.
    """Logout user (client should discard tokens)"""
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=schemas.User)
def get_profile(current_user: User = Depends(get_current_user)):
    # get_current_user resolves the caller from the JWT, so a user can only
    # read their own profile; ownership is enforced by the dependency.
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=schemas.User)
def update_profile(
    user_update: schemas.UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user profile"""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.avatar_url is not None:
        current_user.avatar_url = user_update.avatar_url
    if user_update.preferences is not None:
        current_user.preferences = user_update.preferences
    if user_update.notification_settings is not None:
        current_user.notification_settings = user_update.notification_settings
    if user_update.reading_mode is not None:
        current_user.reading_mode = user_update.reading_mode

    db.commit()
    db.refresh(current_user)

    return current_user


@router.put("/me/preferences", response_model=schemas.User)
def update_preferences(
    prefs: schemas.UserPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update user preferences"""
    # The preferences JSON blob is overwritten wholesale with the schema
    # fields, including digest and notification toggles.
    current_user.preferences = {
        "theme": prefs.theme,
        "language": prefs.language,
        "reading_mode": prefs.reading_mode,
        "categories_preferred": prefs.categories_preferred,
        "digest_enabled": prefs.digest_enabled,
        "digest_time": prefs.digest_time,
        "notifications_enabled": prefs.notifications_enabled,
        "push_notifications": prefs.push_notifications,
        "email_notifications": prefs.email_notifications,
    }
    current_user.reading_mode = prefs.reading_mode

    db.commit()
    db.refresh(current_user)

    return current_user


@router.get("/me/preferences", response_model=schemas.UserPreferences)
def get_preferences(current_user: User = Depends(get_current_user)):
    """Get user preferences"""
    prefs = current_user.preferences or {}
    return schemas.UserPreferences(
        theme=prefs.get("theme", "system"),
        language=prefs.get("language", "it"),
        reading_mode=current_user.reading_mode or "morning",
        digest_enabled=prefs.get("digest_enabled", True),
        digest_time=prefs.get("digest_time", "08:00"),
        categories_preferred=prefs.get("categories_preferred", []),
        notifications_enabled=prefs.get("notifications_enabled", True),
        push_notifications=prefs.get("push_notifications", True),
        email_notifications=prefs.get("email_notifications", False),
    )


@router.post("/me/api-key")
def generate_new_api_key(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Generate new API key for user"""
    # The API key is stored inside the preferences JSON blob rather than a
    # dedicated column; it is returned in the response, the only time it is
    # ever shown to the client.
    api_key = generate_api_key()
    current_user.preferences = current_user.preferences or {}
    current_user.preferences["api_key"] = api_key
    db.commit()

    return {"api_key": api_key}
