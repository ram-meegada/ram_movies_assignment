from rest_framework.views import APIView
from rest_framework.response import Response

from movies_app.services.User.moviesService import MoviesService

movies_obj = MoviesService()

class MoviesListingView(APIView):
    def get(self, request):
        result = movies_obj.movies_list(request)
        return Response(result, status=result["status"])

class ReadWriteCollectionView(APIView):
    def post(self, request):
        result = movies_obj.create_collection(request)
        return Response(result, status=result["status"])

    def get(self, request):
        result = movies_obj.all_collections(request)
        return Response(result, status=result["status"])

class FetchUpdateDeleteCollectionView(APIView):
    def get(self, request, collection_uuid):
        result = movies_obj.fetch_collection(request, collection_uuid)
        return Response(result, status=result["status"])

    def delete(self, request, collection_uuid):
        result = movies_obj.delete_collection(request, collection_uuid)
        return Response(result, status=result["status"])

    def put(self, request, collection_uuid):
        result = movies_obj.update_collection(request, collection_uuid)
        return Response(result, status=result["status"])
