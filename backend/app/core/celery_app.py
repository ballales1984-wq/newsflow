try:
    from celery import Celery
    from celery.schedules import crontab
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    Celery = None
    crontab = None

from .config import settings

# Create Celery app only if available
if CELERY_AVAILABLE:
    celery_app = Celery(
        "newsflow",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
    )
else:
    celery_app = None

# Configuration
if CELERY_AVAILABLE and celery_app:
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="Europe/Rome",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        worker_prefetch_multiplier=4,
        worker_max_tasks_per_child=1000,
    )

    # Scheduled tasks
    celery_app.conf.beat_schedule = {
        "collect-news-every-4-hours": {
            "task": "app.services.tasks.collect_all_news",
            "schedule": crontab(hour="*/4", minute=0),  # Every 4 hours
        },
        "update-article-scores": {
            "task": "app.services.tasks.update_article_scores",
            "schedule": crontab(hour="*/8", minute=30),  # Every 8 hours
        },
        "cleanup-old-articles": {
            "task": "app.services.tasks.cleanup_old_articles",
            "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
        },
    }

