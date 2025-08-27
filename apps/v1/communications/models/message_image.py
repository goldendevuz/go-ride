from django.db import models
from apps.v1.shared.models import BaseModel

class MessageImage(BaseModel):
    message = models.ForeignKey(
        "communications.Message",
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ForeignKey(
        "communications.Image",
        on_delete=models.CASCADE,
        related_name="messages"
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Message Image"
        verbose_name_plural = "Message Images"
        # Optional: ensure the same image isn't linked to the same message twice
        unique_together = ("message", "image")

    def __str__(self):
        return f"Message {self.message.id} - Image {self.image.id}"
