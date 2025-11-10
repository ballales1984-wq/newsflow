"""API endpoint tests"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "version" in response.json()


def test_health():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_categories():
    """Test get categories endpoint"""
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_sources():
    """Test get sources endpoint"""
    response = client.get("/api/v1/sources")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_articles():
    """Test get articles endpoint"""
    response = client.get("/api/v1/articles")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data


def test_article_search():
    """Test article search endpoint"""
    response = client.post(
        "/api/v1/articles/search",
        json={"query": "technology"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data

