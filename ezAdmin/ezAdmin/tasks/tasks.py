from celery import shared_task
from django.utils import timezone
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task
def log_session_timeout_info(session_last_activity):
    if session_last_activity:
        current_time = timezone.now()
        session_timeout = settings.SESSION_COOKIE_AGE  # Session timeout in seconds
        session_duration = (current_time - session_last_activity).total_seconds()
        remaining_time = session_timeout - session_duration

        if remaining_time > 0:
            logger.info(f'Remaining session time: {remaining_time:.2f} seconds')
