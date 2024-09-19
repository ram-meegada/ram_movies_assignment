from django.db.models import Sum
from rest_framework import serializers
from movies_app.models.collectionModel import CollectionModel
from movies_app.models.moviesModel import MoviesModel
from movies_app.models.moviesCollectionModel import MoviesCollectionModel


class CreateCollectionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = CollectionModel
        fields = ['id', 'user', 'title', 'description']

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesModel
        fields = ['id', 'uuid', 'title', 'description', 'genres']

class CollectionWithMoviesReadSerializer(serializers.ModelSerializer):
    movies = serializers.SerializerMethodField()
    class Meta:
        model = CollectionModel
        fields = ['id', 'uuid', 'title', 'description', 'movies']
    def get_movies(self, obj):
        try:
            movie_collections = MoviesCollectionModel.objects.filter(
                collection=obj.id
                ).values_list("movie_id", flat=True)
            movies = MoviesModel.objects.filter(id__in=list(movie_collections))
            serializer_movies = MovieSerializer(movies, many=True)
            return serializer_movies.data
        except:
            return []

class CollectionWithoutMoviesReadSerialier(serializers.ModelSerializer):
    class Meta:
        model = CollectionModel
        fields = ['id', 'title', 'uuid', 'description']
