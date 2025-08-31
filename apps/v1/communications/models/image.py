from django.db import models
from apps.v1.shared.models import BaseModel

class Image(BaseModel):
    file = models.ImageField(upload_to="images/")

    def __str__(self):
        return self.file.name
