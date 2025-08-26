from django.db import models
from apps.v1.shared.models import BaseModel

class PaymentType(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Payment Type"
        verbose_name_plural = "Payment Types"

    def __str__(self):
        return self.name