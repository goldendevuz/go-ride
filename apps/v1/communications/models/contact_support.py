from django.db import models
from apps.v1.shared.models import BaseModel

class ContactSupport(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    icon = models.BinaryField(unique=True)
    display_order = models.SmallIntegerField(unique=True, default=1)
    url = models.TextField(unique=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Contact Support"
        verbose_name_plural = "Contact Supports"

    def __str__(self):
        return self.name or f"Contact {self.id}"
