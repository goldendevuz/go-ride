from django.db import models
from apps.v1.shared.models.base import BaseModel

class Message(BaseModel):
    chat = models.ForeignKey("communications.Chat", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("users.Profile", on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(blank=True)
    encrypted = models.BooleanField(default=False)
    images = models.ManyToManyField("communications.Image", blank=True, related_name="messages")

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"Msg {self.id} from {self.sender}"