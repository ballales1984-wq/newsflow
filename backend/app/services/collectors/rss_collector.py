"""
RSS Feed Collector
===================
Collector for RSS and Atom feeds used to aggregate news from sources
that expose structured feeds.

Uses feedparser for feed parsing and BeautifulSoup for HTML content cleaning.
"""

import feedparser
from typing import List, Dict, Any
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import logging

logger = logging.getLogger(__name__)


class RSSCollector:
    """Collector for RSS feeds"""
    """Collector for RSS feeds"""
    
    def __init__(self):
        # User-Agent identifies this bot to feed servers so site operators
        # can tell who is fetching and contact us if needed.
        self.user_agent = "NewsFlow/1.0 (Intelligent News Curation)"
    
    def collect(self, rss_url: str, max_articles: int = 50) -> List[Dict[str, Any]]:
        """
        Collect articles from RSS feed
        
        Args:
            rss_url: RSS feed URL
            max_articles: Maximum number of articles to collect
            
        Returns:
            List of article dictionaries
        """
        try:
            # Parse feed
            feed = feedparser.parse(rss_url, agent=self.user_agent)
            
            # bozo is set when feedparser hit parsing errors; entries may
            # still be usable, so we log and keep processing rather than
            # aborting the whole feed.
            if feed.bozo:
                logger.warning(f"RSS feed has errors: {rss_url}")
            
            articles = []
            
            # Each entry is parsed in its own try block so one malformed
            # entry cannot abort the rest of the feed.
            for entry in feed.entries[:max_articles]:
                try:
                    article = self._parse_entry(entry)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Error parsing RSS entry: {e}")
                    continue
            
            logger.info(f"Collected {len(articles)} articles from {rss_url}")
            return articles
            
        # Any failure fetching or parsing this feed returns an empty
        # list: a dead or unreachable source must not abort the run.
        except Exception as e:
            logger.error(f"Error collecting RSS feed {rss_url}: {e}")
            return []
    
    def _parse_entry(self, entry: Any) -> Dict[str, Any]:
        """Parse RSS entry to article dictionary"""
        
        # Get published date
        # Date may be missing or in an unparseable format; published_at
        # stays None and callers must tolerate undated articles.
        published_at = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published_at = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'published'):
            try:
                published_at = date_parser.parse(entry.published)
            except:
                pass
        
        # Get content
        # RSS feeds disagree on which field carries the body, so fall back
        # from content to description to summary instead of losing it.
        content = ""
        if hasattr(entry, 'content'):
            content = entry.content[0].value
        elif hasattr(entry, 'description'):
            content = entry.description
        elif hasattr(entry, 'summary'):
            content = entry.summary
        
        # Get image
        # Image is optional: media_content/media_thumbnail are RSS
        # extensions absent on many feeds, so image_url may be None.
        image_url = None
        if hasattr(entry, 'media_content') and entry.media_content:
            image_url = entry.media_content[0].get('url')
        elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            image_url = entry.media_thumbnail[0].get('url')
        
        # Title and url are stripped to normalise feed whitespace; summary
        # is truncated to 500 chars to bound stored payload size.
        return {
            'title': entry.get('title', '').strip(),
            'url': entry.get('link', '').strip(),
            'summary': entry.get('summary', '').strip()[:500],
            'content': content,
            'author': entry.get('author', ''),
            'published_at': published_at,
            'image_url': image_url,
        }


# Predefined RSS sources
RSS_SOURCES = {
    'micromega': 'https://www.micromega.net/feed/',
    'ai4business': 'https://www.ai4business.it/feed/',
    'mit_tech_review': 'https://www.technologyreview.com/feed/',
    'ict_security': 'https://www.ictsecuritymagazine.com/feed/',
    'theguardian_tech': 'https://www.theguardian.com/technology/rss',
    'wired_it': 'https://www.wired.it/feed/rss',
    'agendadigitale': 'https://www.agendadigitale.eu/feed/',
    'punto_informatico': 'https://www.punto-informatico.it/feed/',
    'the_hacker_news': 'https://feeds.feedburner.com/TheHackersNews',
    'arxiv_cs': 'http://export.arxiv.org/rss/cs',
}

