from decouple import config
import uuid
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry
from rest_framework import status
from movies_app.utils import messages
from movies_app.models import MoviesCollectionModel, CollectionModel, MoviesModel
from movies_app.serializers.User import moviesSerializer
from django.db import transaction
from movies_app.utils.favouriteGenres import get_favourite_genres

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)
session = requests.Session()
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

class MoviesService:
    '''
        This class handles all the apis related to collection and movies
    '''
    def movies_list(self, request):
        '''
            Method:- GET
            Response:- List of all the the movies from third party api.
        '''
        try:
            URL = "https://demo.credy.in/api/v1/maya/movies/"
            api = session.get(
                URL,
                auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
                verify=False
                )
            return {
                "data": api.json(),
                "messsage": messages.MOVIES_LIST,
                "status": status.HTTP_200_OK
                }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }


    def create_collection(self, request):
        '''
            Method:- POST
            Payload:- title(<string>), description(<string>), (<list of movie objects>)
        '''
        try:
            with transaction.atomic():
                movies_list = request.data.pop("movies")
                collection_serilizer = moviesSerializer.CreateCollectionSerializer(
                    data=request.data,
                    context={'request': request}
                    )
                if collection_serilizer.is_valid():
                    UUID = uuid.uuid4()
                    collection_serilizer_obj = collection_serilizer.save(uuid=UUID)
                else:
                    return {
                        "serializer_errors": collection_serilizer.errors,
                        "message": messages.WENT_WRONG,
                        "status": status.HTTP_400_BAD_REQUEST
                        }
                for movie in movies_list:
                    movie_obj, created = MoviesModel.objects.get_or_create(
                        uuid=movie["uuid"],
                        defaults={
                            "title": movie["title"],
                            "description": movie["description"],
                            "genres": movie["genres"]
                        })
                    # Create Collection
                    create_collection = MoviesCollectionModel.objects.create(
                        collection_id=collection_serilizer_obj.id,
                        movie_id=movie_obj.id
                        )
                return {
                    "data": {
                        "collection_uuid": UUID
                        },
                    "message": messages.COLLECTION_CREATED,
                    "status": status.HTTP_201_CREATED
                    }
        except Exception as err:
            return {"error": str(err),
                    "error_type": str(type(err)),
                    "messsage": messages.WENT_WRONG,
                    "status": status.HTTP_400_BAD_REQUEST
                    }


    def fetch_collection(self, request, collection_uuid):
        '''
            Method:- GET
            Response:- Collection details
        '''
        try:
            collection = CollectionModel.objects.get(uuid=collection_uuid, user_id=request.user.id)
            collection_serializer = moviesSerializer.CollectionWithMoviesReadSerializer(collection)
            return {
                "data": collection_serializer.data,
                "messsage": messages.FETCH_COLLECTION,
                "status": status.HTTP_200_OK
                }
        except CollectionModel.DoesNotExist:
            return {
                "data": None,
                "messsage": messages.COLLECTION_NOT_FOUND,
                "status": status.HTTP_400_BAD_REQUEST
                }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }


    def delete_collection(self, request, collection_uuid):
        '''
            Method:- DELETE
            Purpose:- Delete collection based on collection_uuid
        '''
        try:
            collection = CollectionModel.objects.get(uuid=collection_uuid, user_id=request.user.id)
            collection.delete()
            return {
                "data": None,
                "messsage": messages.DELETE_COLLECTION,
                "status": status.HTTP_200_OK
                }
        except CollectionModel.DoesNotExist:
            return {
                "data": None,
                "messsage": messages.COLLECTION_NOT_FOUND,
                "status": status.HTTP_400_BAD_REQUEST
                }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }


    def update_collection(self, request, collection_uuid):
        '''
            Method:- PUT
            Purpose:- This api updates the details of collection
        '''
        try:
            with transaction.atomic():
                collection_obj = CollectionModel.objects.get(uuid=collection_uuid, user_id=request.user.id)
                movies_list = request.data.pop("movies")
                collection_serilizer = moviesSerializer.CreateCollectionSerializer(
                    collection_obj,
                    data=request.data,
                    context={'request': request}
                    )
                if collection_serilizer.is_valid():
                    collection_serilizer.save()
                else:
                    return {
                        "serializer_errors": collection_serilizer.errors,
                        "message": messages.WENT_WRONG,
                        "status": status.HTTP_400_BAD_REQUEST
                        }
                # delete movies
                movie_ids = [i["id"] for i in movies_list if "id" in i]
                collections_to_delete = MoviesCollectionModel.objects.filter(
                    collection=collection_obj.id
                ).exclude(collection=collection_obj.id, movie__in=movie_ids)
                if collections_to_delete: collections_to_delete.delete()

                # add movies
                for i in movies_list:
                    if "id" not in i:
                        record_uuid = i.pop("uuid")
                        movie_obj, created = MoviesModel.objects.get_or_create(
                            uuid=record_uuid,
                            defaults=i
                            )
                        create_collection = MoviesCollectionModel.objects.create(
                            collection_id=collection_obj.id,
                            movie_id=movie_obj.id
                            )
                return {
                    "data": None,
                    "messsage": messages.COLLECTION_UPDATED,
                    "status": status.HTTP_200_OK
                    }
        except CollectionModel.DoesNotExist:
            return {
                "data": None,
                "messsage": messages.COLLECTION_NOT_FOUND,
                "status": status.HTTP_400_BAD_REQUEST
                }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }


    def all_collections(self, request):
        '''
            Method:- GET
            Response:- List of all collections
        '''
        try:
            collections = CollectionModel.objects.filter(user=request.user)
            serializer = moviesSerializer.CollectionWithoutMoviesReadSerialier(collections, many=True)
            favourite_genres = get_favourite_genres(collections.values_list("id", flat=True))
            return {
                "is_success": True,
                "data": {
                    "collections": serializer.data,
                    "favourite_genres": favourite_genres
                    },
                "messsage": messages.ALL_COLLECTIONS,
                "status": status.HTTP_200_OK
                }
        except Exception as err:
            return {
                "error": str(err),
                "error_type": str(type(err)),
                "messsage": messages.WENT_WRONG,
                "status": status.HTTP_400_BAD_REQUEST
                }
