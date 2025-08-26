from django.db import models
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import PromoInformationType

class PromoInformation(BaseModel):
    type = models.CharField(max_length=50, choices=PromoInformationType.choices, unique=True)
    description = models.CharField(max_length=255, unique=True)
    display_order = models.SmallIntegerField(default=1)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Promo Information"
        verbose_name_plural = "Promo Informations"

    def __str__(self):
        return self.description
