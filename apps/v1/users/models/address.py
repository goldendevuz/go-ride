from django.db import models
from apps.v1.shared.models import BaseModel

class Address(BaseModel):
    longitude = models.FloatField(unique=True)
    latitude = models.FloatField(unique=True)
    text = models.CharField(max_length=255, unique=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    details = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["text"]
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return self.text
