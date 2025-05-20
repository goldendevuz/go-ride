from django.db import models

from apps.v1.shared.models import BaseModel


class Service(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.DurationField(help_text="Example: 00:30:00 for 30 minutes")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title