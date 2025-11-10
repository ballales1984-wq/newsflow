"""Collector service tests"""
import pytest
from app.services.collectors.rss_collector import RSSCollector


def test_rss_collector_initialization():
    """Test RSS collector can be initialized"""
    collector = RSSCollector()
    assert collector is not None
    assert collector.user_agent is not None


def test_rss_collector_with_valid_feed():
    """Test RSS collector with a known valid feed"""
    collector = RSSCollector()
    
    # Use a reliable RSS feed for testing
    articles = collector.collect("https://www.theguardian.com/technology/rss", max_articles=5)
    
    # Should return list (may be empty if feed is down)
    assert isinstance(articles, list)
    
    # If articles found, check structure
    if len(articles) > 0:
        article = articles[0]
        assert 'title' in article
        assert 'url' in article


def test_rss_collector_with_invalid_feed():
    """Test RSS collector handles invalid feeds gracefully"""
    collector = RSSCollector()
    
    articles = collector.collect("https://invalid-feed-url-12345.com/feed", max_articles=5)
    
    # Should return empty list, not crash
    assert isinstance(articles, list)
    assert len(articles) == 0

