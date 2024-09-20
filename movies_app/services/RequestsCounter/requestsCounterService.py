from rest_framework import status
from movies_app.models import RequestCounterModel
from movies_app.utils import messages

class RequestCounterService:
    '''
        This class handles all the apis related to requests count
    '''

    def requests_to_server(self, request):
        '''
            Method:- GET
            Response:- This api return the number of requests came to server
        '''
        try:
            requests_to_server = RequestCounterModel.objects.first()
            return {
                "requests": requests_to_server.request_count,
                "status": status.HTTP_200_OK
            }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }


    def reset_requests_count_to_server(self, request):
        '''
            Method:- PUT
            Response:- This api resets the count of requests came to server to zero
        '''
        try:
            requests_to_server = RequestCounterModel.objects.first()
            requests_to_server.request_count = 0
            requests_to_server.save()
            return {
                "message": messages.REQUESTS_RESET,
                "status": status.HTTP_200_OK
            }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }
