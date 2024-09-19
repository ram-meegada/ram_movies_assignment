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
