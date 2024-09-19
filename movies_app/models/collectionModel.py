from django.db import models
from django.contrib.auth.models import User
from movies_app.models.baseModel import BaseModel

class CollectionModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
