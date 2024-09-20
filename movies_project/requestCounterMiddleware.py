from django.core.cache import cache

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cache.get_or_set('request_count', 0)
        cache.incr('request_count')
        response = self.get_response(request)
        return response

    @staticmethod
    def get_request_count():
        return cache.get_or_set('request_count', 0)

    @staticmethod
    def reset_request_counter():
        cache.set('request_count', 0)
