from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.v1.shared.models import BaseModel

class Notification(BaseModel):
    class State(models.TextChoices):
        NEW = 'new', 'New'
        READ = 'read', 'Read'

    title = models.CharField(max_length=255)
    description = models.TextField()
    send_at = models.DateTimeField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.NEW)

    def clean(self):
        super().clean()
        if self.send_at is not None and self.send_at < timezone.now():
            raise ValidationError({'send_at': 'Notification date and time cannot be in the past.'})

    def __str__(self):
        return f"{self.title} ({self.state})"