"""Tests for authentication/user endpoints (/api/v1/users/*)

Uses an in-memory SQLite database so tests are fully isolated.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import main  # noqa
from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app import models  # ensure models are registered

# ---------------------------------------------------------------------------
# In-memory DB setup (separate engine from test_articles_api.py to avoid
# conflicts when running the suite in parallel)
# ---------------------------------------------------------------------------

SQLALCHEMY_TEST_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _register(client, email="user@example.com", username="testuser",
              password="testpass123", full_name="Test User"):
    return client.post("/api/v1/users/register", json={
        "email": email,
        "username": username,
        "password": password,
        "full_name": full_name,
    })


def _login(client, email="user@example.com", password="testpass123"):
    return client.post("/api/v1/users/login", data={
        "username": email,
        "password": password,
    })


def _auth_headers(client, email="user@example.com", password="testpass123"):
    r = _login(client, email, password)
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

class TestRegistration:

    def test_register_success(self, client):
        r = _register(client)
        assert r.status_code == 201
        data = r.json()
        assert data["email"] == "user@example.com"
        assert data["username"] == "testuser"
        assert "hashed_password" not in data

    def test_register_duplicate_email(self, client):
        _register(client)
        r = _register(client)  # same email
        assert r.status_code == 400
        assert "Email" in r.json()["detail"]

    def test_register_duplicate_username(self, client):
        _register(client, email="first@example.com", username="samename")
        r = _register(client, email="second@example.com", username="samename")
        assert r.status_code == 400
        assert "Username" in r.json()["detail"]

    def test_register_missing_fields(self, client):
        r = client.post("/api/v1/users/register", json={"email": "x@x.com"})
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

class TestLogin:

    def test_login_success(self, client):
        _register(client)
        r = _login(client)
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        _register(client)
        r = _login(client, password="wrongpassword")
        assert r.status_code == 401

    def test_login_unknown_email(self, client):
        r = _login(client, email="nobody@example.com")
        assert r.status_code == 401

    def test_login_returns_user_data(self, client):
        _register(client)
        r = _login(client)
        assert r.json()["user"]["email"] == "user@example.com"


# ---------------------------------------------------------------------------
# /me profile
# ---------------------------------------------------------------------------

class TestProfile:

    def test_get_profile_authenticated(self, client):
        _register(client)
        headers = _auth_headers(client)
        r = client.get("/api/v1/users/me", headers=headers)
        assert r.status_code == 200
        assert r.json()["email"] == "user@example.com"

    def test_get_profile_unauthenticated(self, client):
        r = client.get("/api/v1/users/me")
        assert r.status_code == 401

    def test_update_profile(self, client):
        _register(client)
        headers = _auth_headers(client)
        r = client.put("/api/v1/users/me", headers=headers, json={
            "full_name": "Updated Name"
        })
        assert r.status_code == 200
        assert r.json()["full_name"] == "Updated Name"

    def test_update_profile_unauthenticated(self, client):
        r = client.put("/api/v1/users/me", json={"full_name": "Hacker"})
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Preferences
# ---------------------------------------------------------------------------

class TestPreferences:

    def test_get_default_preferences(self, client):
        _register(client)
        headers = _auth_headers(client)
        r = client.get("/api/v1/users/me/preferences", headers=headers)
        assert r.status_code == 200
        data = r.json()
        # Defaults set on registration
        assert data["theme"] == "system"
        assert data["language"] == "it"

    def test_update_preferences(self, client):
        _register(client)
        headers = _auth_headers(client)
        payload = {
            "theme": "dark",
            "language": "en",
            "reading_mode": "evening",
            "digest_enabled": False,
            "digest_time": "20:00",
            "categories_preferred": ["tech", "science"],
            "notifications_enabled": True,
            "push_notifications": False,
            "email_notifications": True,
        }
        r = client.put("/api/v1/users/me/preferences", headers=headers, json=payload)
        assert r.status_code == 200
        data = r.json()
        # Endpoint returns User object with preferences dict
        prefs = data.get("preferences") or {}
        assert prefs.get("theme") == "dark"
        assert prefs.get("language") == "en"


# ---------------------------------------------------------------------------
# API key generation
# ---------------------------------------------------------------------------

class TestAPIKey:

    def test_generate_api_key(self, client):
        _register(client)
        headers = _auth_headers(client)
        r = client.post("/api/v1/users/me/api-key", headers=headers)
        assert r.status_code == 200
        data = r.json()
        assert "api_key" in data
        assert data["api_key"].startswith("nf_")

    def test_generate_api_key_unauthenticated(self, client):
        r = client.post("/api/v1/users/me/api-key")
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------

class TestLogout:

    def test_logout_authenticated(self, client):
        _register(client)
        headers = _auth_headers(client)
        r = client.post("/api/v1/users/logout", headers=headers)
        assert r.status_code == 200
        assert "message" in r.json()

    def test_logout_unauthenticated(self, client):
        r = client.post("/api/v1/users/logout")
        assert r.status_code == 401
