from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

# Create a Celery instance
app = Celery('dashboard')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all Django apps
app.autodiscover_tasks()

# Optional: If you want to configure periodic tasks using Celery Beat
from celery.schedules import crontab

app.conf.beat_schedule = {
    'collect_data_task': {
        'task': 'sentiment_dashboard.tasks.collect_data_task',
        'schedule': crontab(minute='*/15'),  # Run every 15 minutes
        # 'args': (api_key, api_secret_key, access_token, access_token_secret, keyword),
    },
}
