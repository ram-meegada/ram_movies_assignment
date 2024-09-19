from decouple import config
import uuid
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry
from rest_framework import status
from movies_app.utils import messages
from movies_app.models.moviesCollectionModel import MoviesCollectionModel
from movies_app.serializers.User.moviesSerializer import CreateCollectionSerializer, MovieSerializer

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

retry_strategy = Retry(
    total=5,               
    backoff_factor=1,      
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)

session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

class MoviesService:
    def movies_list(self, request):
        try:
            URL = "https://demo.credy.in/api/v1/maya/movies/"
            api = session.get(
                URL,
                auth=(CLIENT_ID, CLIENT_SECRET)
                )
            return {"data": api.json(), "messsage": messages.MOVIES_LIST, "status": status.HTTP_200_OK}
        except Exception as err:
            return {"error": str(err), "error_type": str(type(err)), "messsage": messages.WENT_WRONG, "status": status.HTTP_400_BAD_REQUEST}

    def create_collection(self, request):
        '''
            method:- POST
            
        '''
        movies_list = request.data.pop("movies")
        try:
            collection_serilizer = CreateCollectionSerializer(data=request.data, context={'request': request})
            if collection_serilizer.is_valid():
                collection_serilizer_obj = collection_serilizer.save()
            else:
                return {"serializer_errors": collection_serilizer.errors, "messsage": messages.WENT_WRONG, "status": status.HTTP_400_BAD_REQUEST}
            for movie in movies_list:
                movie_serializer = MovieSerializer(data=movie)
                if movie_serializer.is_valid():
                    movie_serializer_obj = movie_serializer.save()
                    # Create Collection
                    create_collection = MoviesCollectionModel.objects.create(
                        collection_id=collection_serilizer_obj.id,
                        movie=movie_serializer_obj.id
                        )

        except Exception as err:
            return {"error": str(err), "messsage": messages.WENT_WRONG, "status": status.HTTP_400_BAD_REQUEST}
