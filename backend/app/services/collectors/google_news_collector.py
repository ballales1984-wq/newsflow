import feedparser
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import logging
import urllib.parse

logger = logging.getLogger(__name__)


class GoogleNewsCollector:
    """Collector for Google News RSS feeds"""
    
    def __init__(self):
        self.user_agent = "NewsFlow/1.0 (Intelligent News Curation)"
        self.base_url = "https://news.google.com/rss"
    
    def collect(
        self,
        query: Optional[str] = None,
        language: str = "it",
        country: str = "IT",
        max_articles: int = 20,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Collect articles from Google News RSS feed
        
        Args:
            query: Search query (optional)
            language: Language code (default: 'it' for Italian)
            country: Country code (default: 'IT' for Italy)
            max_articles: Maximum number of articles to collect
            topic: Topic/category (e.g., 'TECHNOLOGY', 'SCIENCE', 'WORLD', etc.)
            
        Returns:
            List of article dictionaries
        """
        try:
            # Build RSS URL
            rss_url = self._build_rss_url(query, language, country, topic)
            
            logger.info(f"Fetching Google News from: {rss_url}")
            
            # Parse feed
            feed = feedparser.parse(rss_url, agent=self.user_agent)
            
            if feed.bozo:
                logger.warning(f"Google News RSS feed has errors: {feed.bozo_exception}")
            
            articles = []
            
            for entry in feed.entries[:max_articles]:
                try:
                    article = self._parse_entry(entry, language)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Error parsing Google News entry: {e}")
                    continue
            
            logger.info(f"Collected {len(articles)} articles from Google News")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting Google News feed: {e}")
            return []
    
    def _build_rss_url(
        self,
        query: Optional[str],
        language: str,
        country: str,
        topic: Optional[str]
    ) -> str:
        """Build Google News RSS URL"""
        
        params = {
            'hl': language,
            'gl': country,
            'ceid': f"{country}:{language}"
        }
        
        if query:
            # Search query
            params['q'] = query
            url = f"{self.base_url}/search"
        elif topic:
            # Topic/category
            url = f"{self.base_url}/headlines/section/{topic}"
        else:
            # Top headlines
            url = f"{self.base_url}/headlines"
        
        # Build query string
        query_string = urllib.parse.urlencode(params)
        return f"{url}?{query_string}"
    
    def _parse_entry(self, entry: Any, language: str) -> Optional[Dict[str, Any]]:
        """Parse Google News RSS entry to article dictionary"""
        
        try:
            # Google News entries have a special format
            # The link is usually a redirect URL, we need to extract the actual URL
            link = entry.get('link', '').strip()
            
            # Get published date
            published_at = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_at = datetime(*entry.published_parsed[:6])
            elif hasattr(entry, 'published'):
                try:
                    published_at = date_parser.parse(entry.published)
                except:
                    pass
            
            # Get content/summary
            content = ""
            if hasattr(entry, 'content'):
                if isinstance(entry.content, list) and len(entry.content) > 0:
                    content = entry.content[0].value
                else:
                    content = str(entry.content)
            elif hasattr(entry, 'description'):
                content = entry.description
            elif hasattr(entry, 'summary'):
                content = entry.summary
            
            # Extract source from title (Google News format: "Title - Source")
            title = entry.get('title', '').strip()
            source_name = "Google News"
            
            # Try to extract source from title (format: "Title - Source Name")
            if ' - ' in title:
                parts = title.rsplit(' - ', 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    source_name = parts[1].strip()
            
            # Get image (if available in media tags)
            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                if isinstance(entry.media_content, list) and len(entry.media_content) > 0:
                    media_item = entry.media_content[0]
                    if isinstance(media_item, dict) and 'url' in media_item:
                        image_url = media_item['url']
            
            if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                if isinstance(entry.media_thumbnail, list) and len(entry.media_thumbnail) > 0:
                    thumb_item = entry.media_thumbnail[0]
                    if isinstance(thumb_item, dict) and 'url' in thumb_item:
                        image_url = thumb_item['url']
            
            return {
                'title': title,
                'url': link,
                'summary': content[:500] if content else '',
                'content': content[:5000] if content else '',
                'author': source_name,
                'published_at': published_at,
                'image_url': image_url,
                'source': 'Google News',
                'language': language,
            }
            
        except Exception as e:
            logger.error(f"Error parsing Google News entry: {e}")
            return None
    
    def collect_by_topics(
        self,
        topics: List[str],
        language: str = "it",
        country: str = "IT",
        max_articles_per_topic: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Collect articles from multiple Google News topics
        
        Args:
            topics: List of topic names (e.g., ['TECHNOLOGY', 'SCIENCE', 'WORLD'])
            language: Language code
            country: Country code
            max_articles_per_topic: Maximum articles per topic
            
        Returns:
            List of article dictionaries
        """
        all_articles = []
        
        for topic in topics:
            try:
                articles = self.collect(
                    query=None,
                    language=language,
                    country=country,
                    max_articles=max_articles_per_topic,
                    topic=topic
                )
                all_articles.extend(articles)
            except Exception as e:
                logger.error(f"Error collecting topic {topic}: {e}")
                continue
        
        return all_articles


# Predefined Google News topics/categories
GOOGLE_NEWS_TOPICS = {
    'TECHNOLOGY': 'TECHNOLOGY',
    'SCIENCE': 'SCIENCE',
    'WORLD': 'WORLD',
    'NATION': 'NATION',
    'BUSINESS': 'BUSINESS',
    'ENTERTAINMENT': 'ENTERTAINMENT',
    'SPORTS': 'SPORTS',
    'HEALTH': 'HEALTH',
    'POLITICS': 'POLITICS',
    'ENVIRONMENT': 'ENVIRONMENT',
}

# Predefined Google News queries for Italian news
GOOGLE_NEWS_QUERIES_IT = [
    'tecnologia',
    'scienza',
    'intelligenza artificiale',
    'cybersecurity',
    'innovazione',
    'startup',
    'economia',
    'politica',
    'sport',
    'salute',
    'ambiente',
    'cultura',
]

