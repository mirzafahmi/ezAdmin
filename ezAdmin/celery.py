import os
from celery import Celery

app = Celery('ezAdmin')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

# Celery broker settings (e.g., using Redis as a message broker)
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Celery beat schedule
app.conf.beat_schedule = {
    'log-session-timeout-info': {
        'task': 'ezAdmin.tasks.log_session_timeout_info',
        'schedule': 10.0,  # Adjust the interval as needed (e.g., every 2 minutes)
    },
}
