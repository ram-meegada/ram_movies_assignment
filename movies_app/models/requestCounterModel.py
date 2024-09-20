from django.db import models
from movies_app.models.baseModel import BaseModel

class RequestCounterModel(BaseModel):
    request_count = models.IntegerField(default=0)
