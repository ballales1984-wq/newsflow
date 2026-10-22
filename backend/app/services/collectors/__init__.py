"""
Collector package.

Four collection strategies are exposed: RSS feeds, generic JSON news APIs
(NewsAPI, The Guardian), Google News RSS, and an HTML scraper backed by
newspaper3k. Multiple strategies exist because no single source covers the
Italian news landscape completely: RSS gives structured feeds where
available, APIs fill gaps for sites without feeds, Google News acts as an
aggregator fallback, and the scraper reaches sites that expose neither.

Every collector normalises its output into the same article dictionary
shape and traps per-source errors so that one failing source never aborts
the whole collection run.
"""

from .rss_collector import RSSCollector
from .api_collector import APICollector
from .scraper_collector import ScraperCollector
from .google_news_collector import GoogleNewsCollector

__all__ = ["RSSCollector", "APICollector", "ScraperCollector", "GoogleNewsCollector"]

