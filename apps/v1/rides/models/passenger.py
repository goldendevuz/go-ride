from django.db import models
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import GenderChoices

class Passenger(BaseModel):
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    age = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    added_by = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="added_passengers")

    class Meta:
        ordering = ["name"]
        verbose_name = "Passenger"
        verbose_name_plural = "Passengers"

    def __str__(self):
        return self.full_name or self.name
