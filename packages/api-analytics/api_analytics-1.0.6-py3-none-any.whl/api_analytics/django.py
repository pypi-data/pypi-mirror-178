import threading
from time import time

from api_analytics.core import log_request
from django import conf
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse


class Analytics:
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_key = getattr(conf.settings, "ANALYTICS_API_KEY", None)

    def __call__(self, request: WSGIRequest):
        start = time()
        response: HttpResponse = self.get_response(request)
        elapsed = time() - start

        json = {
            'api_key': self.api_key,
            'hostname': request.get_host(),
            'path': request.path,
            'user_agent': request.headers['user-agent'],
            'method': request.method,
            'status': response.status_code,
            'response_time': int(elapsed * 1000),
            'framework': 'Flask'
        }

        threading.Thread(target=log_request, args=(json,)).start()

        return response