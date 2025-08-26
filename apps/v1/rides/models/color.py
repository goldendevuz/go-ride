from django.db import models
from apps.v1.shared.models import BaseModel

class Color(BaseModel):
    name = models.CharField(
        max_length=50,
        unique=True,
        default="white"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name
