from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from apps.v1.shared.models import BaseModel


class Wallet(BaseModel):
    profile = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name=_("Profile"),
        help_text=_("The user profile this wallet belongs to."),
    )
    balance = models.PositiveIntegerField(
        verbose_name=_("Balance"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("The current balance of the wallet in the smallest currency unit."),
    )

    class Meta:
        ordering = ["profile"]
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self):
        return f"{self.profile.user.username} Wallet ({self.balance})"