import logging
from django.utils import timezone
from django.conf import settings
import datetime
from tasks.tasks import log_session_timeout_info


logger = logging.getLogger(__name__)

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.session.get('last_activity'):
            last_activity_str = request.session['last_activity']
            last_activity = datetime.datetime.fromisoformat(last_activity_str)
            current_time = timezone.now()
            session_duration = (current_time - last_activity).total_seconds()
            session_timeout = settings.SESSION_COOKIE_AGE  # Session timeout in seconds
            remaining_time = session_timeout - session_duration

            if remaining_time > 0:
                logger.info(f'Remaining session time: {remaining_time:.2f} seconds')

            # Pass last_activity to the Celery task
            log_session_timeout_info.delay(last_activity)

        # Update the last activity timestamp in the session
        request.session['last_activity'] = timezone.now().isoformat()

        return response
