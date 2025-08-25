from django.db import models
from apps.v1.shared.models import BaseModel
import uuid

class Language(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
    )
    code = models.CharField(
    max_length=50,
    unique=True,
    null=False,
    default="english_us",  # Default value for DB and future migrations
)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
