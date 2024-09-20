from movies_app.models import RequestCounterModel
from threading import Thread

class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        Thread(target=increase_count_by_one, args=()).start()
        response = self.get_response(request)
        return response

def increase_count_by_one():
    try:
        request_count, created = RequestCounterModel.objects.get_or_create()
        request_count.request_count += 1
        request_count.save()
    except Exception as err:
        print(err, '----err----')
