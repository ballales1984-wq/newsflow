# Celery is an optional dependency: the API has to start even in a minimal
# deployment where the worker packages are not installed. When the import fails
# the module still exposes CELERY_AVAILABLE and a None application, so every
# consumer can check the flag before using the app. crontab is set to None as
# well, otherwise the beat schedule below would raise a NameError at import.
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
    # The same Redis instance plays both roles: broker (the task queue) and
    # result backend (task states and results). REDIS_URL is the only knob, and
    # it is used nowhere else in the codebase.
    # The broker connection is opened lazily, so an unreachable Redis does not
    # break the import of this module: it only breaks the workers and any
    # attempt to dispatch a task.
    celery_app = Celery(
        "newsflow",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
    )
else:
    celery_app = None

# Configuration
if CELERY_AVAILABLE and celery_app:
    # JSON only: no pickle payloads, so a message sitting in the queue cannot
    # execute arbitrary code on the worker.
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        # The schedules below are expressed in Rome local time, while
        # enable_utc keeps the worker clock itself on UTC.
        timezone="Europe/Rome",
        enable_utc=True,
        # task_track_started stores the "started" state, so a long task is
        # visible as running instead of only as pending.
        task_track_started=True,
        # Hard limit of 30 minutes per task: a collector blocked on a slow feed
        # is killed together with its worker child process instead of blocking
        # the queue forever. No soft limit is configured, so the task gets no
        # in-process interrupt before it is killed.
        task_time_limit=30 * 60,  # 30 minutes
        # Each worker keeps 4 messages in flight, so one slow task does not
        # leave the other workers idle.
        worker_prefetch_multiplier=4,
        # Children are recycled after 1000 tasks to bound the memory growth of
        # a long lived worker process.
        worker_max_tasks_per_child=1000,
    )

    # Scheduled tasks
    # The task names must match the ones registered by the decorator in
    # app/services/tasks.py, which registers them as
    # "app.services.tasks.<function name>". A typo here leaves the schedule
    # pointing at a task that does not exist.
    # The schedule is only executed by a running "celery -A ... beat" process,
    # the API process never triggers it.
    celery_app.conf.beat_schedule = {
        "collect-news-every-4-hours": {
            # The key is only the label of the entry.
            "task": "app.services.tasks.collect_all_news",
            # Minute 0 of every 4th hour: the collectors run on the full hour
            # and do not compete with the score update of the next entry.
            "schedule": crontab(hour="*/4", minute=0),  # Every 4 hours
        },
        "update-article-scores": {
            "task": "app.services.tasks.update_article_scores",
            # Offset of 30 minutes to spread the load of the beat scheduler.
            "schedule": crontab(hour="*/8", minute=30),  # Every 8 hours
        },
        "cleanup-old-articles": {
            "task": "app.services.tasks.cleanup_old_articles",
            # The cleanup runs at night, when the collectors are idle.
            "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
        },
    }

