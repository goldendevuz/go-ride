from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.v1.shared.models import BaseModel

class Rate(BaseModel):
    profile = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="rates")
    value = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    class Meta:
        ordering = ["profile"]
        verbose_name = "Rate"
        verbose_name_plural = "Rates"

    def __str__(self):
        return f"{self.profile} - {self.value}"
