"""Tests for the articles API endpoints (/api/v1/articles/*)

Uses an in-memory SQLite database so tests are fully isolated from the
production database.  The fixture `client` provides a TestClient with the
database dependency overridden.
"""
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db
from app.models.article import Article
from app.models.source import Source
from app.models.category import Category

# ---------------------------------------------------------------------------
# In-memory DB setup
# ---------------------------------------------------------------------------

SQLALCHEMY_TEST_URL = "sqlite://"  # in-memory

engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
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
    """Re-create all tables before each test and drop them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    """Provide a direct DB session for seeding data."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _seed_source(db) -> Source:
    source = Source(
        name="Test Source",
        slug="test-source",
        url="https://testsource.example.com",
        source_type="rss",
        is_active=True,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def _seed_article(db, source_id, title="Test Article", slug=None, is_archived=False,
                  is_featured=False, quality_score=None, published_at=None) -> Article:
    article = Article(
        title=title,
        slug=slug or title.lower().replace(" ", "-"),
        url=f"https://example.com/{slug or title.lower().replace(' ', '-')}",
        summary="Summary text",
        source_id=source_id,
        is_archived=is_archived,
        is_featured=is_featured,
        quality_score=quality_score,
        published_at=published_at or datetime.utcnow(),
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


# ---------------------------------------------------------------------------
# GET /api/v1/articles/
# ---------------------------------------------------------------------------

class TestGetArticles:

    def test_returns_200_with_empty_db(self, client):
        r = client.get("/api/v1/articles/")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 0
        assert data["items"] == []

    def test_returns_articles(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Article One", slug="article-one")
        _seed_article(db, src.id, title="Article Two", slug="article-two")

        r = client.get("/api/v1/articles/")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    def test_archived_articles_excluded(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Live", slug="live")
        _seed_article(db, src.id, title="Archived", slug="archived", is_archived=True)

        r = client.get("/api/v1/articles/")
        data = r.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Live"

    def test_pagination_page_calculation(self, client, db):
        src = _seed_source(db)
        for i in range(10):
            _seed_article(db, src.id, title=f"Article {i}", slug=f"article-{i}")

        # page 1, limit 3
        r = client.get("/api/v1/articles/?skip=0&limit=3")
        data = r.json()
        assert data["page"] == 1
        assert data["size"] == 3
        assert len(data["items"]) == 3

        # page 2
        r2 = client.get("/api/v1/articles/?skip=3&limit=3")
        data2 = r2.json()
        assert data2["page"] == 2

    def test_filter_by_featured(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Featured", slug="featured", is_featured=True)
        _seed_article(db, src.id, title="Normal", slug="normal")

        r = client.get("/api/v1/articles/?is_featured=true")
        data = r.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Featured"

    def test_filter_by_min_quality_score(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="High quality", slug="high", quality_score=0.9)
        _seed_article(db, src.id, title="Low quality", slug="low", quality_score=0.3)

        r = client.get("/api/v1/articles/?min_quality_score=0.8")
        data = r.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "High quality"

    def test_invalid_min_quality_score(self, client):
        """min_quality_score > 1 should fail validation."""
        r = client.get("/api/v1/articles/?min_quality_score=1.5")
        assert r.status_code == 422

    def test_invalid_limit_zero(self, client):
        r = client.get("/api/v1/articles/?limit=0")
        assert r.status_code == 422

    def test_invalid_limit_over_100(self, client):
        r = client.get("/api/v1/articles/?limit=101")
        assert r.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/v1/articles/{id}
# ---------------------------------------------------------------------------

class TestGetArticleById:

    def test_existing_article(self, client, db):
        src = _seed_source(db)
        article = _seed_article(db, src.id, title="By ID", slug="by-id")

        r = client.get(f"/api/v1/articles/{article.id}")
        assert r.status_code == 200
        assert r.json()["title"] == "By ID"

    def test_nonexistent_article_returns_404(self, client):
        r = client.get("/api/v1/articles/99999")
        assert r.status_code == 404

    def test_article_id_zero_not_found(self, client):
        r = client.get("/api/v1/articles/0")
        assert r.status_code in (404, 422)


# ---------------------------------------------------------------------------
# GET /api/v1/articles/slug/{slug}
# ---------------------------------------------------------------------------

class TestGetArticleBySlug:

    def test_existing_slug(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Slug Article", slug="my-unique-slug")

        r = client.get("/api/v1/articles/slug/my-unique-slug")
        assert r.status_code == 200
        assert r.json()["slug"] == "my-unique-slug"

    def test_unknown_slug_returns_404(self, client):
        r = client.get("/api/v1/articles/slug/does-not-exist")
        assert r.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/articles/search
# ---------------------------------------------------------------------------

class TestSearchArticles:

    def test_empty_search_returns_all(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Alpha", slug="alpha")
        _seed_article(db, src.id, title="Beta", slug="beta")

        r = client.post("/api/v1/articles/search", json={})
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 2

    def test_text_search_filters_by_title(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Python tutorial", slug="python-tutorial")
        _seed_article(db, src.id, title="JavaScript guide", slug="js-guide")

        r = client.post("/api/v1/articles/search", json={"query": "Python"})
        data = r.json()
        assert data["total"] == 1
        assert "Python" in data["items"][0]["title"]

    def test_search_archived_excluded(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Live Python", slug="live-py")
        _seed_article(db, src.id, title="Archived Python", slug="archived-py", is_archived=True)

        r = client.post("/api/v1/articles/search", json={"query": "Python"})
        data = r.json()
        assert data["total"] == 1

    def test_search_by_date_range(self, client, db):
        src = _seed_source(db)
        now = datetime.utcnow()
        _seed_article(db, src.id, title="Old", slug="old", published_at=now - timedelta(days=30))
        _seed_article(db, src.id, title="Recent", slug="recent", published_at=now)

        r = client.post("/api/v1/articles/search", json={
            "date_from": (now - timedelta(days=1)).isoformat()
        })
        data = r.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Recent"


# ---------------------------------------------------------------------------
# GET /api/v1/articles/featured/list
# ---------------------------------------------------------------------------

class TestFeaturedArticles:

    def test_returns_only_featured(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Featured A", slug="feat-a", is_featured=True)
        _seed_article(db, src.id, title="Regular B", slug="reg-b", is_featured=False)

        r = client.get("/api/v1/articles/featured/list")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        assert data[0]["title"] == "Featured A"

    def test_featured_excludes_archived(self, client, db):
        src = _seed_source(db)
        _seed_article(db, src.id, title="Featured Archived", slug="fa",
                      is_featured=True, is_archived=True)

        r = client.get("/api/v1/articles/featured/list")
        assert r.json() == []


# ---------------------------------------------------------------------------
# GET /api/v1/articles/recent/list
# ---------------------------------------------------------------------------

class TestRecentArticles:

    def test_recent_articles(self, client, db):
        src = _seed_source(db)
        now = datetime.utcnow()
        _seed_article(db, src.id, title="New", slug="new", published_at=now)
        _seed_article(db, src.id, title="Old", slug="old", published_at=now - timedelta(days=10))

        r = client.get("/api/v1/articles/recent/list?days=3")
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 1
        assert data[0]["title"] == "New"

    def test_invalid_days_range(self, client):
        r = client.get("/api/v1/articles/recent/list?days=31")
        assert r.status_code == 422
