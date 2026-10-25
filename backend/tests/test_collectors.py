"""Tests for all collector services (RSS, API, Scraper)

Network-dependent tests (real HTTP requests) are marked ``integration`` so
they can be excluded from fast unit-test runs:

    pytest -m "not integration"

The unit tests use mocks and never touch the network.
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime

from app.services.collectors.rss_collector import RSSCollector, RSS_SOURCES
from app.services.collectors.api_collector import APICollector
from app.services.collectors.scraper_collector import ScraperCollector


# ===========================================================================
# RSSCollector
# ===========================================================================

class TestRSSCollector:

    def test_initialization(self):
        collector = RSSCollector()
        assert collector is not None
        assert "NewsFlow" in collector.user_agent

    def test_collect_returns_list(self):
        collector = RSSCollector()
        result = collector.collect("https://invalid-feed-url-99999.example/feed", max_articles=5)
        assert isinstance(result, list)

    def test_collect_invalid_url_returns_empty(self):
        collector = RSSCollector()
        result = collector.collect("not-a-url", max_articles=5)
        assert result == []

    def test_collect_respects_max_articles(self):
        """Even if the feed returns 100 entries, max_articles is honoured."""
        collector = RSSCollector()

        # Build a fake feed with 20 entries
        fake_entry = MagicMock()
        fake_entry.get.side_effect = lambda key, default="": {
            "title": "Test", "link": "https://example.com", "summary": "", "author": ""
        }.get(key, default)
        fake_entry.published_parsed = None

        fake_feed = MagicMock()
        fake_feed.bozo = False
        fake_feed.entries = [fake_entry] * 20

        with patch("feedparser.parse", return_value=fake_feed):
            result = collector.collect("https://example.com/rss", max_articles=5)

        assert len(result) <= 5

    def test_parse_entry_basic_fields(self):
        """_parse_entry returns a dict with the expected keys."""
        collector = RSSCollector()

        entry = MagicMock()
        entry.get.side_effect = lambda key, default="": {
            "title": "  Article Title  ",
            "link": "  https://example.com/article  ",
            "summary": "A brief summary",
            "author": "Author Name",
        }.get(key, default)
        entry.published_parsed = (2024, 1, 15, 10, 30, 0, 0, 0, 0)
        # Avoid triggering content/description/summary attribute branch
        del entry.content
        del entry.description
        del entry.media_content
        del entry.media_thumbnail

        result = collector._parse_entry(entry)
        assert result is not None
        assert result["title"] == "Article Title"
        assert result["url"] == "https://example.com/article"
        assert isinstance(result["published_at"], datetime)

    def test_parse_entry_date_from_published_parsed(self):
        collector = RSSCollector()
        entry = MagicMock()
        entry.get.side_effect = lambda k, d="": {"title": "T", "link": "http://x.com", "summary": "", "author": ""}.get(k, d)
        entry.published_parsed = (2024, 6, 1, 12, 0, 0, 0, 0, 0)
        del entry.content
        del entry.description
        del entry.media_content
        del entry.media_thumbnail

        result = collector._parse_entry(entry)
        assert result["published_at"] == datetime(2024, 6, 1, 12, 0, 0)

    def test_parse_entry_date_fallback_string(self):
        """When published_parsed is None, the string date is parsed."""
        collector = RSSCollector()
        entry = MagicMock()
        entry.get.side_effect = lambda k, d="": {"title": "T", "link": "http://x.com", "summary": "", "author": ""}.get(k, d)
        entry.published_parsed = None
        entry.published = "Mon, 01 Jan 2024 12:00:00 GMT"
        del entry.content
        del entry.description
        del entry.media_content
        del entry.media_thumbnail

        result = collector._parse_entry(entry)
        assert result["published_at"] is not None

    def test_parse_entry_summary_truncated_at_500(self):
        collector = RSSCollector()
        long_summary = "x" * 600
        entry = MagicMock()
        entry.get.side_effect = lambda k, d="": {
            "title": "T", "link": "http://x.com", "summary": long_summary, "author": ""
        }.get(k, d)
        entry.published_parsed = None
        del entry.content
        del entry.description
        del entry.media_content
        del entry.media_thumbnail

        result = collector._parse_entry(entry)
        assert len(result["summary"]) <= 500

    def test_bozo_feed_still_returns_articles(self):
        """A bozo (malformed) feed should be processed, not aborted."""
        collector = RSSCollector()

        fake_entry = MagicMock()
        fake_entry.get.side_effect = lambda k, d="": {
            "title": "Bozo Article", "link": "http://x.com", "summary": "", "author": ""
        }.get(k, d)
        fake_entry.published_parsed = None
        del fake_entry.content
        del fake_entry.description
        del fake_entry.media_content
        del fake_entry.media_thumbnail

        fake_feed = MagicMock()
        fake_feed.bozo = True
        fake_feed.entries = [fake_entry]

        with patch("feedparser.parse", return_value=fake_feed):
            result = collector.collect("http://example.com/feed", max_articles=10)

        assert isinstance(result, list)

    def test_rss_sources_dict_not_empty(self):
        assert len(RSS_SOURCES) > 0
        for name, url in RSS_SOURCES.items():
            assert url.startswith("http")

    @pytest.mark.integration
    def test_real_feed(self):
        """Integration: actually fetch The Guardian tech RSS feed."""
        collector = RSSCollector()
        articles = collector.collect("https://www.theguardian.com/technology/rss", max_articles=5)
        assert isinstance(articles, list)
        if articles:
            assert "title" in articles[0]
            assert "url" in articles[0]


# ===========================================================================
# APICollector
# ===========================================================================

class TestAPICollector:

    def test_initialization(self):
        collector = APICollector()
        assert collector is not None
        assert collector.timeout == 30

    @pytest.mark.asyncio
    async def test_collect_newsapi_no_key_returns_empty(self):
        """When no API key is configured, collect_newsapi must return []."""
        collector = APICollector()
        collector.newsapi_key = ""
        result = await collector.collect_newsapi(query="test")
        assert result == []

    @pytest.mark.asyncio
    async def test_collect_guardian_no_key_returns_empty(self):
        """When no API key is configured, collect_guardian must return []."""
        collector = APICollector()
        collector.guardian_key = ""
        result = await collector.collect_guardian(query="test")
        assert result == []

    @pytest.mark.asyncio
    async def test_collect_newsapi_ok_response(self):
        """Mocked NewsAPI ok response should return parsed articles."""
        collector = APICollector()
        collector.newsapi_key = "fake-key"

        fake_article = {
            "title": "Test headline",
            "url": "https://example.com/test",
            "description": "A short description",
            "content": "Full content here",
            "author": "John Doe",
            "publishedAt": "2024-01-15T10:00:00Z",
            "urlToImage": "https://example.com/img.jpg",
        }
        fake_response = MagicMock()
        fake_response.raise_for_status = MagicMock()
        fake_response.json.return_value = {
            "status": "ok",
            "articles": [fake_article],
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = fake_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await collector.collect_newsapi(query="test")

        assert len(result) == 1
        assert result[0]["title"] == "Test headline"
        assert result[0]["url"] == "https://example.com/test"

    @pytest.mark.asyncio
    async def test_collect_newsapi_error_status_returns_empty(self):
        """A non-ok NewsAPI status body returns []."""
        collector = APICollector()
        collector.newsapi_key = "fake-key"

        fake_response = MagicMock()
        fake_response.raise_for_status = MagicMock()
        fake_response.json.return_value = {
            "status": "error",
            "message": "API key invalid",
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = fake_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await collector.collect_newsapi(query="test")

        assert result == []

    @pytest.mark.asyncio
    async def test_collect_newsapi_network_error_returns_empty(self):
        """A network exception returns [] without raising."""
        collector = APICollector()
        collector.newsapi_key = "fake-key"

        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("connection refused")
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await collector.collect_newsapi(query="test")

        assert result == []

    @pytest.mark.asyncio
    async def test_collect_guardian_ok_response(self):
        """Mocked Guardian ok response should return parsed articles."""
        collector = APICollector()
        collector.guardian_key = "fake-key"

        fake_item = {
            "webTitle": "Guardian Article",
            "webUrl": "https://theguardian.com/test",
            "webPublicationDate": "2024-01-15T10:00:00Z",
            "fields": {
                "trailText": "Trail text here",
                "bodyText": "Full body text",
                "byline": "Reporter Name",
                "thumbnail": "https://example.com/thumb.jpg",
            },
        }
        fake_response = MagicMock()
        fake_response.raise_for_status = MagicMock()
        fake_response.json.return_value = {
            "response": {
                "status": "ok",
                "results": [fake_item],
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value = fake_response
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await collector.collect_guardian(query="test")

        assert len(result) == 1
        assert result[0]["title"] == "Guardian Article"
        assert result[0]["author"] == "Reporter Name"

    def test_parse_newsapi_article_missing_date(self):
        """A NewsAPI article without publishedAt should parse to published_at=None."""
        collector = APICollector()
        item = {
            "title": "No date article",
            "url": "https://example.com/no-date",
            "description": "Some description",
            "content": "",
            "author": "",
        }
        result = collector._parse_newsapi_article(item)
        assert result is not None
        assert result["published_at"] is None

    def test_parse_newsapi_article_with_date(self):
        """A NewsAPI article with publishedAt should have a parsed datetime."""
        collector = APICollector()
        item = {
            "title": "Dated article",
            "url": "https://example.com/dated",
            "description": "desc",
            "content": "",
            "author": "",
            "publishedAt": "2024-03-15T09:00:00Z",
        }
        result = collector._parse_newsapi_article(item)
        assert result["published_at"] is not None
        assert isinstance(result["published_at"], datetime)

    def test_parse_guardian_article(self):
        """_parse_guardian_article maps fields correctly."""
        collector = APICollector()
        item = {
            "webTitle": "Guardian Title",
            "webUrl": "https://theguardian.com/article",
            "webPublicationDate": "2024-02-10T08:00:00Z",
            "fields": {
                "trailText": "Trail" * 100,  # more than 500 chars
                "bodyText": "Body text.",
                "byline": "Jane Smith",
                "thumbnail": "https://img.example.com/t.jpg",
            },
        }
        result = collector._parse_guardian_article(item)
        assert result is not None
        assert result["title"] == "Guardian Title"
        assert len(result["summary"]) <= 500
        assert result["author"] == "Jane Smith"


# ===========================================================================
# ScraperCollector
# ===========================================================================

class TestScraperCollector:

    def test_initialization(self):
        collector = ScraperCollector()
        assert collector is not None
        assert "NewsFlow" in collector.user_agent
        assert collector.timeout == 30

    def test_parse_europeana_item_list_fields(self):
        """_parse_europeana_item handles list fields (Europeana's style)."""
        collector = ScraperCollector()
        item = {
            "title": ["Europeana Article Title"],
            "guid": "https://europeana.eu/item/123",
            "dcDescription": ["Description of the item"],
            "dcCreator": ["Creator Name"],
            "edmPreview": ["https://example.com/preview.jpg"],
        }
        result = collector._parse_europeana_item(item)
        assert result is not None
        assert result["title"] == "Europeana Article Title"
        assert result["url"] == "https://europeana.eu/item/123"
        assert result["summary"] == "Description of the item"
        assert result["published_at"] is None

    def test_parse_europeana_item_string_fields(self):
        """_parse_europeana_item handles string (non-list) fields."""
        collector = ScraperCollector()
        item = {
            "title": "Single Title",
            "guid": "https://europeana.eu/item/456",
        }
        result = collector._parse_europeana_item(item)
        assert result is not None
        assert result["title"] == "Single Title"

    def test_parse_europeana_item_empty(self):
        """_parse_europeana_item handles a completely empty dict."""
        collector = ScraperCollector()
        result = collector._parse_europeana_item({})
        assert result is not None
        assert result["title"] == ""
        assert result["url"] == ""

    def test_parse_archive_item(self):
        """_parse_archive_item builds the correct details URL."""
        collector = ScraperCollector()
        item = {
            "identifier": "some-book-1970",
            "title": "Some Book from 1970",
            "description": "A public domain book.",
            "creator": "Famous Author",
        }
        result = collector._parse_archive_item(item)
        assert result is not None
        assert "some-book-1970" in result["url"]
        assert "some-book-1970" in result["image_url"]
        assert result["title"] == "Some Book from 1970"
        assert result["author"] == "Famous Author"
        assert result["published_at"] is None

    def test_parse_archive_item_no_identifier(self):
        """_parse_archive_item with no identifier produces empty url/image_url."""
        collector = ScraperCollector()
        item = {"title": "No ID Item"}
        result = collector._parse_archive_item(item)
        assert result is not None
        assert result["url"] == ""
        assert result["image_url"] is None

    @pytest.mark.asyncio
    async def test_collect_europeana_network_error(self):
        """Network errors from Europeana return [] without raising."""
        collector = ScraperCollector()

        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("timeout")
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await collector.collect_europeana("test query")

        assert result == []

    @pytest.mark.asyncio
    async def test_collect_internet_archive_network_error(self):
        """Network errors from Internet Archive return [] without raising."""
        collector = ScraperCollector()

        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("timeout")
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)

        with patch("httpx.AsyncClient", return_value=mock_client):
            result = await collector.collect_internet_archive("test query")

        assert result == []

    @pytest.mark.asyncio
    async def test_collect_from_url_error_returns_none(self):
        """If newspaper3k fails, collect_from_url returns None without raising."""
        collector = ScraperCollector()

        with patch("app.services.collectors.scraper_collector.NewspaperArticle") as mock_cls:
            mock_article = MagicMock()
            mock_article.download.side_effect = Exception("download failed")
            mock_cls.return_value = mock_article

            result = await collector.collect_from_url("https://example.com/article")

        assert result is None
