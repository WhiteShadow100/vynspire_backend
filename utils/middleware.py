import time
import logging

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    Middleware to log every request's method, path, and time taken in ms.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration_ms = (time.time() - start_time) * 1000
        method = request.method
        path = request.get_full_path()

        logger.info(f"{method} {path} completed in {duration_ms:.2f}ms")

        return response