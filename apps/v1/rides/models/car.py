from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel

class Car(BaseModel):
    model = models.CharField(
        verbose_name=_("Model"),
        max_length=255,
        help_text=_("The brand and model of the car (e.g., 'Toyota Camry')."),
    )
    color = models.ForeignKey(
        "rides.Color",
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name=_("Color"),
        help_text=_("The color of the car."),
    )
    plate_number = models.CharField(
        verbose_name=_("Plate Number"),
        max_length=255,
        unique=True,
        help_text=_("The unique license plate number of the car."),
    )
    car_type = models.ForeignKey(
        "rides.CarType",
        on_delete=models.PROTECT,
        related_name="cars",
        verbose_name=_("Car Type"),
        help_text=_("The type of car (e.g., Sedan, SUV)."),
    )

    class Meta:
        ordering = ["model"]
        verbose_name = _("Car")
        verbose_name_plural = _("Cars")
        # Ensure a car model with a specific color is unique
        unique_together = ('model', 'color', 'plate_number')

    def __str__(self):
        return f"{self.model} - {self.plate_number}"