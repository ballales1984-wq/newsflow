"""Celery tasks for background jobs"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import logging

from ..core.celery_app import celery_app
from ..core.database import SessionLocal
from ..models import Article, Source
from ..services.collectors import RSSCollector, APICollector, ScraperCollector
from ..services.nlp import NLPAnalyzer, ArticleClassifier
from ..core.config import settings
from slugify import slugify

logger = logging.getLogger(__name__)


@celery_app.task(name="app.services.tasks.collect_all_news")
def collect_all_news():
    """Collect news from all active sources"""
    logger.info("Starting news collection task")
    
    db = SessionLocal()
    try:
        # Get all active sources
        sources = db.query(Source).filter(Source.is_active == True).all()
        
        total_collected = 0
        for source in sources:
            try:
                count = collect_from_source(source.id)
                total_collected += count
            except Exception as e:
                logger.error(f"Error collecting from source {source.name}: {e}")
        
        logger.info(f"Collected {total_collected} articles total")
        return total_collected
        
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.collect_from_source")
def collect_from_source(source_id: int) -> int:
    """Collect news from specific source"""
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source:
            return 0
        
        articles_data = []
        
        if source.source_type == "rss" and source.rss_url:
            collector = RSSCollector()
            articles_data = collector.collect(
                source.rss_url,
                max_articles=settings.MAX_ARTICLES_PER_SOURCE
            )
        
        # Process and save articles
        count = 0
        for article_data in articles_data:
            try:
                if not article_data.get('url'):
                    continue
                
                # Check if article already exists
                existing = db.query(Article).filter(
                    Article.url == article_data['url']
                ).first()
                
                if existing:
                    continue
                
                # Create article
                article = Article(
                    title=article_data['title'],
                    slug=slugify(article_data['title'])[:500],
                    url=article_data['url'],
                    summary=article_data.get('summary'),
                    content=article_data.get('content'),
                    author=article_data.get('author'),
                    published_at=article_data.get('published_at'),
                    image_url=article_data.get('image_url'),
                    source_id=source.id,
                )
                
                db.add(article)
                db.commit()
                
                # Analyze article in background
                analyze_article.delay(article.id)
                
                count += 1
                
            except Exception as e:
                logger.error(f"Error saving article: {e}")
                db.rollback()
                continue
        
        # Update source last_collected_at
        source.last_collected_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Collected {count} new articles from {source.name}")
        return count
        
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.analyze_article")
def analyze_article(article_id: int):
    """Analyze article with NLP"""
    db = SessionLocal()
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            return
        
        # Perform NLP analysis
        analyzer = NLPAnalyzer()
        text = article.content or article.summary or ""
        
        if not text:
            return
        
        analysis = analyzer.analyze(text, article.title)
        
        # Update article with analysis results
        article.language = analysis['language']
        article.keywords = analysis['keywords']
        article.entities = analysis['entities']
        article.sentiment_score = analysis['sentiment_score']
        article.quality_score = analysis['quality_score']
        article.word_count = analysis['word_count']
        article.reading_time_minutes = analysis['reading_time_minutes']
        
        db.commit()
        
        logger.info(f"Analyzed article {article.id}")
        
    except Exception as e:
        logger.error(f"Error analyzing article {article_id}: {e}")
        db.rollback()
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.update_article_scores")
def update_article_scores():
    """Recalculate relevance scores for recent articles"""
    logger.info("Updating article scores")
    
    db = SessionLocal()
    try:
        # Get articles from last 30 days
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        articles = db.query(Article).filter(
            Article.collected_at >= cutoff_date
        ).all()
        
        count = 0
        for article in articles:
            try:
                # Recalculate quality score if needed
                if article.content and not article.quality_score:
                    analyze_article.delay(article.id)
                    count += 1
            except Exception as e:
                logger.error(f"Error updating article {article.id}: {e}")
        
        logger.info(f"Queued {count} articles for score update")
        return count
        
    finally:
        db.close()


@celery_app.task(name="app.services.tasks.cleanup_old_articles")
def cleanup_old_articles():
    """Archive or delete old articles"""
    logger.info("Cleaning up old articles")
    
    db = SessionLocal()
    try:
        # Archive articles older than MAX_ARTICLE_AGE_DAYS
        cutoff_date = datetime.utcnow() - timedelta(days=settings.MAX_ARTICLE_AGE_DAYS)
        
        result = db.query(Article).filter(
            Article.collected_at < cutoff_date,
            Article.is_archived == False
        ).update({
            'is_archived': True
        })
        
        db.commit()
        
        logger.info(f"Archived {result} old articles")
        return result
        
    finally:
        db.close()

