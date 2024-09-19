from django.db import models
from django.contrib.auth.models import User

from movies_app.models.collectionModel import CollectionModel
from movies_app.models.moviesModel import MoviesModel
from movies_app.models.baseModel import BaseModel


class MoviesCollectionModel(BaseModel):
    collection = models.ForeignKey(CollectionModel, on_delete=models.CASCADE, related_name="collections_rn")
    movie = models.ForeignKey(MoviesModel, on_delete=models.CASCADE, related_name="movies_rn")

    def __str__(self):
        return self.collection.title
