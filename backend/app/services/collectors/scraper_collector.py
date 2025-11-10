import httpx
from bs4 import BeautifulSoup
from newspaper import Article as NewspaperArticle
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ScraperCollector:
    """Collector for web scraping (ethical)"""
    
    def __init__(self):
        self.user_agent = "NewsFlow/1.0 (Intelligent News Curation; +https://newsflow.app)"
        self.timeout = 30
    
    async def collect_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Collect article from single URL using newspaper3k
        
        Args:
            url: Article URL
            
        Returns:
            Article dictionary or None
        """
        try:
            article = NewspaperArticle(url)
            article.download()
            article.parse()
            article.nlp()
            
            return {
                'title': article.title,
                'url': url,
                'summary': article.summary[:500] if article.summary else '',
                'content': article.text,
                'author': ', '.join(article.authors) if article.authors else '',
                'published_at': article.publish_date,
                'image_url': article.top_image,
                'keywords': article.keywords[:10] if article.keywords else [],
            }
            
        except Exception as e:
            logger.error(f"Error scraping article {url}: {e}")
            return None
    
    async def collect_europeana(
        self,
        query: str,
        max_articles: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Collect from Europeana Collections
        
        Args:
            query: Search query
            max_articles: Maximum number of articles
            
        Returns:
            List of article dictionaries
        """
        try:
            url = "https://www.europeana.eu/api/v2/search.json"
            params = {
                "wskey": "api2demo",  # Replace with actual key
                "query": query,
                "rows": max_articles,
                "profile": "rich",
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            articles = []
            for item in data.get("items", []):
                article = self._parse_europeana_item(item)
                if article:
                    articles.append(article)
            
            logger.info(f"Collected {len(articles)} items from Europeana")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from Europeana: {e}")
            return []
    
    async def collect_internet_archive(
        self,
        query: str,
        collection: str = "opensource",
        max_articles: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Collect from Internet Archive
        
        Args:
            query: Search query
            collection: Collection name
            max_articles: Maximum number of items
            
        Returns:
            List of article dictionaries
        """
        try:
            url = "https://archive.org/advancedsearch.php"
            params = {
                "q": f"collection:{collection} AND ({query})",
                "fl[]": ["identifier", "title", "description", "date", "creator"],
                "rows": max_articles,
                "output": "json",
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            
            articles = []
            for item in data.get("response", {}).get("docs", []):
                article = self._parse_archive_item(item)
                if article:
                    articles.append(article)
            
            logger.info(f"Collected {len(articles)} items from Internet Archive")
            return articles
            
        except Exception as e:
            logger.error(f"Error collecting from Internet Archive: {e}")
            return []
    
    def _parse_europeana_item(self, item: Dict) -> Optional[Dict[str, Any]]:
        """Parse Europeana item"""
        try:
            return {
                'title': item.get('title', [''])[0] if isinstance(item.get('title'), list) else item.get('title', ''),
                'url': item.get('guid', ''),
                'summary': item.get('dcDescription', [''])[0] if isinstance(item.get('dcDescription'), list) else '',
                'content': '',
                'author': item.get('dcCreator', [''])[0] if isinstance(item.get('dcCreator'), list) else '',
                'published_at': None,
                'image_url': item.get('edmPreview', [''])[0] if isinstance(item.get('edmPreview'), list) else '',
            }
        except Exception as e:
            logger.error(f"Error parsing Europeana item: {e}")
            return None
    
    def _parse_archive_item(self, item: Dict) -> Optional[Dict[str, Any]]:
        """Parse Internet Archive item"""
        try:
            identifier = item.get('identifier', '')
            url = f"https://archive.org/details/{identifier}" if identifier else ''
            
            return {
                'title': item.get('title', ''),
                'url': url,
                'summary': item.get('description', ''),
                'content': '',
                'author': item.get('creator', ''),
                'published_at': None,
                'image_url': f"https://archive.org/services/img/{identifier}" if identifier else None,
            }
        except Exception as e:
            logger.error(f"Error parsing Archive item: {e}")
            return None

