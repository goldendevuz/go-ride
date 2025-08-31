from django.db import models
from apps.v1.shared.models.base import BaseModel
from django.conf import settings

class Chat(BaseModel):
    user1 = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="chats_as_user1")
    user2 = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="chats_as_user2")

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Chat {self.id} ({self.user1} ↔ {self.user2})"