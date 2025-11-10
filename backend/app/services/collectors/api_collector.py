import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dateutil import parser as date_parser
import logging
from ...core.config import settings

logger = logging.getLogger(__name__)


class APICollector:
    """Collector for news APIs"""
    
    def __init__(self):
        self.newsapi_key = settings.NEWSAPI_KEY
        self.guardian_key = settings.GUARDIAN_API_KEY
        self.timeout = 30
    
    async def collect_newsapi(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        language: str = "en",
        max_articles: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Collect articles from NewsAPI
        
        Args:
            query: Search query
            category: Category (technology, science, etc.)
            language: Language code
            max_articles: Maximum number of articles
            
        Returns:
            List of article dictionaries
        """
        if not self.newsapi_key:
            logger.warning("NewsAPI key not configured")
            return []
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                "apiKey": self.newsapi_key,
                "language": language,
                "pageSize": min(max_articles, 100),
            }
            
            if query:
                params["q"] = query
            if category:
                params["category"] = category
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            if data["status"] != "ok":
                logger.error(f"NewsAPI error: {data.get('message')}")
                return []
            
            articles = []
            for item in data.get("articles", []):
                article = self._parse_newsapi_article(item)
                if article:
                    articles.append(article)
            
            logger.info(f"Collected {len(articles)} articles from NewsAPI")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from NewsAPI: {e}")
            return []
    
    async def collect_guardian(
        self,
        query: Optional[str] = None,
        section: Optional[str] = None,
        max_articles: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Collect articles from The Guardian API
        
        Args:
            query: Search query
            section: Section (technology, science, etc.)
            max_articles: Maximum number of articles
            
        Returns:
            List of article dictionaries
        """
        if not self.guardian_key:
            logger.warning("Guardian API key not configured")
            return []
        
        try:
            url = "https://content.guardianapis.com/search"
            params = {
                "api-key": self.guardian_key,
                "page-size": min(max_articles, 50),
                "show-fields": "all",
                "order-by": "newest",
            }
            
            if query:
                params["q"] = query
            if section:
                params["section"] = section
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            if data["response"]["status"] != "ok":
                logger.error("Guardian API error")
                return []
            
            articles = []
            for item in data["response"].get("results", []):
                article = self._parse_guardian_article(item)
                if article:
                    articles.append(article)
            
            logger.info(f"Collected {len(articles)} articles from Guardian")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from Guardian: {e}")
            return []
    
    def _parse_newsapi_article(self, item: Dict) -> Optional[Dict[str, Any]]:
        """Parse NewsAPI article"""
        try:
            published_at = None
            if item.get('publishedAt'):
                published_at = date_parser.parse(item['publishedAt'])
            
            return {
                'title': item.get('title', '').strip(),
                'url': item.get('url', '').strip(),
                'summary': item.get('description', '').strip()[:500],
                'content': item.get('content', ''),
                'author': item.get('author', ''),
                'published_at': published_at,
                'image_url': item.get('urlToImage'),
            }
        except Exception as e:
            logger.error(f"Error parsing NewsAPI article: {e}")
            return None
    
    def _parse_guardian_article(self, item: Dict) -> Optional[Dict[str, Any]]:
        """Parse Guardian article"""
        try:
            fields = item.get('fields', {})
            published_at = None
            if item.get('webPublicationDate'):
                published_at = date_parser.parse(item['webPublicationDate'])
            
            return {
                'title': item.get('webTitle', '').strip(),
                'url': item.get('webUrl', '').strip(),
                'summary': fields.get('trailText', '').strip()[:500],
                'content': fields.get('bodyText', ''),
                'author': fields.get('byline', ''),
                'published_at': published_at,
                'image_url': fields.get('thumbnail'),
            }
        except Exception as e:
            logger.error(f"Error parsing Guardian article: {e}")
            return None

