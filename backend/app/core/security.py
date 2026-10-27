from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import secrets

from .config import settings
from .database import get_db
from ..models import User

# bcrypt is the only accepted scheme, and deprecated="auto" means that a hash
# written with any other scheme is treated as outdated and transparently
# re-hashed on the next successful verification.
# Note: passlib 1.7.4 probes `bcrypt.__about__`, an attribute removed in
# bcrypt 4.x, so a "(trapped) error reading bcrypt version" warning may be
# printed on the first hash. The result itself is unaffected.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# tokenUrl only drives the "Authorize" button of the Swagger UI, but it has to
# match the real login route (/api/v1/users/login, see api/v1/endpoints/users.py)
# for that button to work. The token itself is read from the
# "Authorization: Bearer <token>" header, and since auto_error defaults to True,
# a missing header is rejected by FastAPI before the endpoint code runs.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    # bcrypt only hashes the first 72 bytes of the password, so two passwords
    # sharing that prefix are equivalent for the hash.
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    # The payload is copied so the dict passed by the caller is not mutated.
    # `data` carries the subject only ({"sub": "<user id>"}), the expiry is
    # added here and the default lifetime comes from ACCESS_TOKEN_EXPIRE_MINUTES.
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # `exp` must be a numeric timestamp or datetime (RFC 7519) so python-jose
    # can decode and validate token expiration without JWTClaimsError.
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token (longer lasting)"""
    # Refresh tokens live 30 days and carry an extra "type": "refresh" claim, so
    # the /users/refresh endpoint can tell them apart from access tokens.
    # Note: get_current_user() never inspects the "type" claim, so a refresh
    # token would also pass the access token check.
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """Decode JWT token"""
    # Every JWTError (bad signature, expired token, invalid claims) is collapsed
    # into None, so the callers cannot tell the failure modes apart.
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token"""
    # The same 401 is returned for every failure, so the client cannot probe
    # whether a token exists, only that it was rejected.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # The subject is the user id stored as a string, so it has to be converted
    # before the lookup. The user is read from the database on every request:
    # a token of a deleted or disabled account stops working immediately.
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user from JWT token (optional - returns None if not authenticated)"""
    # Optional variant, for endpoints that serve anonymous and logged-in readers
    # alike: it returns None instead of raising, so the endpoint can branch on
    # the result.
    # Note: the scheme dependency runs with auto_error=True, so a completely
    # missing Authorization header is rejected before this function is reached;
    # the guard below only covers an empty bearer value.
    if not token:
        return None

    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


def generate_api_key() -> str:
    """Generate unique API key for user"""
    # 32 random bytes from the OS CSPRNG, encoded URL-safe (about 43 characters).
    # The "nf_" prefix makes the key recognisable in logs and in secret
    # scanners, so a leaked key can be traced back to its owner.
    # The endpoint stores the key in the preferences JSON of the user, there is
    # no dedicated column for it.
    return f"nf_{secrets.token_urlsafe(32)}"
