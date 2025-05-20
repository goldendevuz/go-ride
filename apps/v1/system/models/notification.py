from django.db import models

from apps.v1.shared.models import BaseModel


class Notification(BaseModel):
    class State(models.TextChoices):
        NEW = 'new', 'New'
        READ = 'read', 'Read'

    title = models.CharField(max_length=255)
    description = models.TextField()
    send_at = models.DateTimeField()
    state = models.CharField(max_length=20, choices=State.choices, default=State.NEW)

    def __str__(self):
        return f"{self.title} ({self.state})"