from django.db import models
from movies_app.models.baseModel import BaseModel

class MoviesModel(BaseModel):
    uuid = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    