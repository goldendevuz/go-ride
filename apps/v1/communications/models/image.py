from django.db import models
from apps.v1.shared.models import BaseModel

class Image(BaseModel):
    file = models.BinaryField(unique=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return f"Image {self.id}"
