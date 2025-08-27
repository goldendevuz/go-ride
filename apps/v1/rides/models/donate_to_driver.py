from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.v1.shared.models import BaseModel


class DonateToDriver(BaseModel):
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="donations",
        verbose_name=_("Profile"),
        help_text=_("The user profile making the donation."),
    )
    driver = models.ForeignKey(
        "rides.Driver",
        on_delete=models.CASCADE,
        related_name="donations",
        verbose_name=_("Driver"),
        help_text=_("The driver receiving the donation."),
    )
    amount = models.PositiveIntegerField(
        verbose_name=_("Amount"),
        validators=[MinValueValidator(1)],
        help_text=_("The amount of the donation in the smallest currency unit."),
    )
    payment = models.ForeignKey(
        "finances.Payment",
        on_delete=models.CASCADE,
        related_name="donations",
        verbose_name=_("Payment"),
        help_text=_("The payment record for this donation."),
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Donation to Driver")
        verbose_name_plural = _("Donations to Drivers")

    def __str__(self):
        return f"Donation of {self.amount} from {self.profile} to {self.driver}"