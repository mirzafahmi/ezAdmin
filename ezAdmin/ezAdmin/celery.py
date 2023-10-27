from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ezAdmin.settings')

app = Celery('ezAdmin')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks(['ezAdmin'])

# Use Redis as the message broker
app.conf.broker_url = 'redis://localhost:6379/0'  # Adjust the URL if needed
