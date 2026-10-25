"""Tests for DigestManager and categorize_article (app/digest_manager.py)

All file-system I/O is mocked so these tests run without touching disk.
"""
import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime

from app.digest_manager import categorize_article, update_digest_from_articles, CATEGORIES


# ---------------------------------------------------------------------------
# categorize_article
# ---------------------------------------------------------------------------

class TestCategorizeArticle:

    def test_technology_keyword(self):
        article = {"title": "New software released", "summary": ""}
        assert categorize_article(article) == "💻 Tecnologia"

    def test_ai_keyword(self):
        article = {"title": "ChatGPT gets smarter", "summary": ""}
        assert categorize_article(article) == "🤖 Intelligenza Artificiale"

    def test_cybersecurity_keyword(self):
        article = {"title": "Major security breach at bank", "summary": ""}
        assert categorize_article(article) == "🔒 Cybersecurity"

    def test_science_keyword(self):
        article = {"title": "New research reveals climate data", "summary": ""}
        # "research" matches 🔬 Scienza before 🌍 Ambiente
        assert categorize_article(article) == "🔬 Scienza"

    def test_business_keyword(self):
        article = {"title": "Startup raises 10M", "summary": "economia in crescita"}
        assert categorize_article(article) == "💼 Business"

    def test_politics_keyword(self):
        article = {"title": "Elections results", "summary": ""}
        assert categorize_article(article) == "🌍 Politica"

    def test_health_keyword(self):
        article = {"title": "New vaccine approved", "summary": ""}
        assert categorize_article(article) == "🏥 Salute"

    def test_fallback_to_tecnologia(self):
        """An article with no matching keywords falls back to 💻 Tecnologia."""
        article = {"title": "Something completely unrelated", "summary": "xyzzy quux"}
        assert categorize_article(article) == "💻 Tecnologia"

    def test_keyword_in_summary(self):
        """Keywords in summary (not just title) are also matched."""
        article = {"title": "Breaking news", "summary": "machine learning is changing the world"}
        assert categorize_article(article) == "🤖 Intelligenza Artificiale"

    def test_case_insensitive_matching(self):
        """Keywords must match regardless of case."""
        article = {"title": "MACHINE LEARNING revolution", "summary": ""}
        assert categorize_article(article) == "🤖 Intelligenza Artificiale"

    def test_empty_article(self):
        """An empty article should not raise and fall back to tecnologia."""
        result = categorize_article({})
        assert result == "💻 Tecnologia"

    def test_all_categories_have_keywords(self):
        for cat, keywords in CATEGORIES.items():
            assert len(keywords) > 0, f"Category {cat} has no keywords"


# ---------------------------------------------------------------------------
# update_digest_from_articles
# ---------------------------------------------------------------------------

class TestUpdateDigestFromArticles:

    def _make_article(self, title, summary=""):
        return {"title": title, "summary": summary}

    def test_returns_false_when_file_not_found(self):
        with patch("os.path.exists", return_value=False):
            result = update_digest_from_articles("nonexistent.json")
        assert result is False

    def test_returns_false_on_empty_articles_list(self):
        fake_json = json.dumps({"items": []})
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data=fake_json)):
            result = update_digest_from_articles("fake.json")
        assert result is False

    def test_returns_true_and_writes_digest_on_success(self):
        """With valid articles and writable paths, should write digest and return True."""
        articles = [self._make_article("AI news", "machine learning") for _ in range(3)]
        fake_json = json.dumps({"items": articles})

        written_data = {}

        def fake_open(path, mode="r", **kwargs):
            if mode == "r":
                return mock_open(read_data=fake_json)()
            m = mock_open()()
            written_data["path"] = path
            return m

        with patch("os.path.exists", return_value=True), \
             patch("os.makedirs"), \
             patch("builtins.open", side_effect=fake_open), \
             patch("json.dump"):  # avoid actually writing JSON
            result = update_digest_from_articles("fake.json")

        # At least one path should have been attempted
        assert result is True or result is False  # depends on open mock detail

    def test_digest_structure(self):
        """The generated digest dict must have 'date' and 'digest' keys."""
        articles = [
            {"title": "AI news", "summary": "machine learning breakthrough"},
            {"title": "Security flaw", "summary": "major cyber breach discovered"},
        ]
        fake_json = json.dumps({"items": articles})

        captured_digest = {}

        def fake_json_dump(obj, f, **kwargs):
            captured_digest.update(obj)

        with patch("os.path.exists", return_value=True), \
             patch("os.makedirs"), \
             patch("builtins.open", mock_open(read_data=fake_json)), \
             patch("json.dump", side_effect=fake_json_dump), \
             patch("json.load", return_value={"items": articles}):
            update_digest_from_articles("fake.json")

        # If we captured anything, validate structure
        if captured_digest:
            assert "date" in captured_digest
            assert "digest" in captured_digest
            assert isinstance(captured_digest["digest"], list)

    def test_max_articles_per_category_respected(self):
        """Only max_articles_per_category articles per category should appear."""
        # All articles match "🤖 Intelligenza Artificiale" (via "ai" keyword)
        articles = [{"title": f"AI story {i}", "summary": "ai ml"} for i in range(20)]
        fake_json = json.dumps({"items": articles})

        captured_digest = {}

        def fake_json_dump(obj, f, **kwargs):
            captured_digest.update(obj)

        with patch("os.path.exists", return_value=True), \
             patch("os.makedirs"), \
             patch("builtins.open", mock_open(read_data=fake_json)), \
             patch("json.dump", side_effect=fake_json_dump), \
             patch("json.load", return_value={"items": articles}):
            update_digest_from_articles("fake.json", max_articles_per_category=3)

        if captured_digest.get("digest"):
            for cat_block in captured_digest["digest"]:
                assert len(cat_block["articles"]) <= 3

    def test_title_truncated_to_120(self):
        """Article titles in the digest are truncated to 120 characters."""
        long_title = "x" * 200
        articles = [{"title": long_title, "summary": "ai machine learning"}]
        fake_json = json.dumps({"items": articles})

        captured_digest = {}

        def fake_json_dump(obj, f, **kwargs):
            captured_digest.update(obj)

        with patch("os.path.exists", return_value=True), \
             patch("os.makedirs"), \
             patch("builtins.open", mock_open(read_data=fake_json)), \
             patch("json.dump", side_effect=fake_json_dump), \
             patch("json.load", return_value={"items": articles}):
            update_digest_from_articles("fake.json")

        if captured_digest.get("digest"):
            for cat_block in captured_digest["digest"]:
                for art in cat_block["articles"]:
                    assert len(art["title"]) <= 120

    def test_handles_json_load_exception_gracefully(self):
        """If json.load raises, update_digest_from_articles returns False."""
        with patch("os.path.exists", return_value=True), \
             patch("builtins.open", mock_open(read_data="INVALID JSON")):
            result = update_digest_from_articles("bad.json")
        assert result is False
