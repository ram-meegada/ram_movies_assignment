from rest_framework.views import APIView
from rest_framework.response import Response

from movies_app.services.User.moviesService import MoviesService

movies_obj = MoviesService()

class MoviesListingView(APIView):
    def get(self, request):
        result = movies_obj.movies_list(request)
        return Response(result, status=result["status"])

class CreateCollectionView(APIView):
    def post(self, request):
        result = movies_obj.create_collection(request)
        return Response(result, status=result["status"])
