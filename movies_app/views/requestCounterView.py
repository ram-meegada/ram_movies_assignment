from rest_framework.views import APIView
from rest_framework.response import Response
from movies_app.services.RequestsCounter.requestsCounterService import RequestCounterService

requests_counter_obj = RequestCounterService()

class RequestsToServerView(APIView):
    def get(self, request):
        result = requests_counter_obj.requests_to_server(request)
        return Response(result, status=result["status"])


class ResetRequestsToServerView(APIView):
    def put(self, request):
        result = requests_counter_obj.reset_requests_count_to_server(request)
        return Response(result, status=result["status"])
