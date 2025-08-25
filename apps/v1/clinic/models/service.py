from django.core.exceptions import ValidationError
from django.db import models
from apps.v1.shared.models import BaseModel

class Service(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.DurationField(help_text="Example: 00:30:00 for 30 minutes")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def clean(self):
        # duration 0 yoki undan kam bo'lmasligi kerak
        if self.duration is not None and self.duration.total_seconds() <= 0:
            raise ValidationError({'duration': "Davomiylik musbat bo'lishi kerak."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)