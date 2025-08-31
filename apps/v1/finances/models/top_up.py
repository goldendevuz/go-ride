from django.db import models
from apps.v1.shared.models import BaseModel

class TopUp(BaseModel):
    profile = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="top_ups")
    amount = models.IntegerField()
    payment = models.ForeignKey("finances.Payment", on_delete=models.CASCADE, related_name="top_ups")

    class Meta:
        ordering = ["profile"]
        verbose_name = "Top Up"
        verbose_name_plural = "Top Ups"

    def __str__(self):
        return f"{self.profile} - {self.amount}"
