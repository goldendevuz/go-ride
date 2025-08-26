from django.db import models
from apps.v1.shared.models import BaseModel

class SupportedPayment(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    icon = models.BinaryField(unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Supported Payment"
        verbose_name_plural = "Supported Payments"

    def __str__(self):
        return self.name or f"Payment {self.id}"
