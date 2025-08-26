from django.db import models
from apps.v1.shared.models import BaseModel

class Car(BaseModel):
    model = models.CharField(max_length=255, unique=True)
    color = models.ForeignKey("rides.Color", on_delete=models.CASCADE, related_name="cars")
    plate_number = models.CharField(max_length=255, unique=True)
    car_type = models.ForeignKey("rides.CarType", on_delete=models.CASCADE, related_name="cars")

    class Meta:
        ordering = ["model"]
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return f"{self.model} - {self.plate_number}"
