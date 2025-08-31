from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import PromoInformationType


class PromoInformation(BaseModel):
    type = models.CharField(
        verbose_name=_("Type"),
        max_length=50,
        choices=PromoInformationType.choices,
        help_text=_("The type of promotional information."),
    )
    description = models.CharField(
        verbose_name=_("Description"),
        max_length=255,
        help_text=_("The description of the promotional information."),
    )
    display_order = models.SmallIntegerField(
        verbose_name=_("Display Order"),
        default=1,
        help_text=_("The order in which this promo information appears."),
    )

    class Meta:
        ordering = ["display_order"]
        verbose_name = _("Promo Information")
        verbose_name_plural = _("Promo Information Items")

    def __str__(self):
        return f"{self.type} - {self.description}"