from django.db import models
from apps.v1.shared.models import BaseModel

class Mood(BaseModel):
    smile = models.BinaryField()

    class Meta:
        ordering = ["id"]
        verbose_name = "Mood"
        verbose_name_plural = "Moods"

    def __str__(self):
        return f"Mood {self.id}"
