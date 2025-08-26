from django.db import models
from apps.v1.shared.models import BaseModel

class Language(BaseModel):
    name = models.CharField(unique=True)
    code = models.CharField(
        max_length=50,
        unique=True,
        default="english_us",  # Default value for DB and future migrations
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
