from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel


class CarType(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=20,
        unique=True,
        help_text=_("The type of car (e.g., Sedan, SUV)."),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Car Type")
        verbose_name_plural = _("Car Types")

    def __str__(self):
        return self.name