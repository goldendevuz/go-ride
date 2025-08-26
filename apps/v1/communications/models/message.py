from django.db import models
from apps.v1.shared.models import BaseModel

class Message(BaseModel):
    owner = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField(blank=True, null=True)
    has_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["created"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"From {self.owner} to {self.receiver}"
