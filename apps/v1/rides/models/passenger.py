from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import GenderChoices


class Passenger(BaseModel):
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=10,
        choices=GenderChoices.choices,
        help_text=_("The gender of the passenger."),
    )
    age = models.PositiveSmallIntegerField(
        verbose_name=_("Age"),
        blank=True,
        null=True,
        help_text=_("The age of the passenger."),
    )
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=255,
        help_text=_("The first name of the passenger."),
    )
    full_name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The full name of the passenger."),
    )
    added_by = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="added_passengers",
        verbose_name=_("Added By"),
        help_text=_("The user profile that added this passenger."),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")

    def __str__(self):
        return self.full_name or self.name