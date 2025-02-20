import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure periodic tasks
app.conf.beat_schedule = {
    'check-stock-alerts': {
        'task': 'api.tasks.check_stock_alerts',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'update-portfolio-values': {
        'task': 'api.tasks.update_portfolio_values',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'cleanup-old-alerts': {
        'task': 'api.tasks.cleanup_old_alerts',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}
