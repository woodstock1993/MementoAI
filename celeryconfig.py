from datetime import datetime, timedelta

from celery.schedules import crontab

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'UTC'

current_time = datetime.now()
scheduled_time = current_time + timedelta(seconds=10)

CELERY_BEAT_SCHEDULE = {
    'update-expired-urls': {
        'task': 'app.tasks.update_expired_urls',
        'schedule': timedelta(seconds=5),
    },
}