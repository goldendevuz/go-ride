from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel


class PaymentType(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=20,
        unique=True,
        help_text=_("The name of the payment type"),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Payment Type")
        verbose_name_plural = _("Payment Types")

    def __str__(self):
        return self.name
