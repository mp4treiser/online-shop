import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('shop')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks([
    "shop.tasks.debug_task",
    "api.tasks.add"
])


app.conf.beat_schedule = {
    'hello-world-3-minutes-40-seconds': {
        'task': 'shop.tasks.debug_task',
        'schedule': 220.0, # каждые 3 мин 40 сек или 220 сек
        'args': (1,)
    },
    "create-random-product-hourly-19-to-21-only-3-times": {
        'task': 'api.tasks.debug_task',
        'schedule': crontab(hour='19-21', minute=0),  # Каждый час с 19:00 до 21:00,
        'args': (1,)
    }
}
