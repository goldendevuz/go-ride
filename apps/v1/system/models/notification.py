from django.db import models
from django.utils import timezone

from apps.v1.shared.enums import NotificationStates
from apps.v1.shared.models import BaseModel

class Notification(BaseModel):
    profile = models.ForeignKey(
        "user.Profile",
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    state = models.CharField(
        max_length=10,
        choices=NotificationStates.choices,
        default=NotificationStates.NEW,
    )
    sent_at = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} - {self.state}"
