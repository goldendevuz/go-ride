from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel


class Address(BaseModel):
    longitude = models.FloatField(
        verbose_name=_("Longitude"),
        help_text=_("The longitude of the address."),
    )
    latitude = models.FloatField(
        verbose_name=_("Latitude"),
        help_text=_("The latitude of the address."),
    )
    text = models.CharField(
        verbose_name=_("Full Address Text"),
        max_length=255,
        help_text=_("The full-text representation of the address."),
    )
    landmark = models.CharField(
        verbose_name=_("Landmark"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("A nearby landmark or point of interest."),
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("A user-defined name for the address (e.g., 'Home', 'Work')."),
    )
    details = models.CharField(
        verbose_name=_("Details"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Additional details about the address."),
    )

    class Meta:
        ordering = ["text"]
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        # Ensure a specific combination of location and text is unique
        unique_together = ('longitude', 'latitude', 'text')

    def __str__(self):
        return self.text