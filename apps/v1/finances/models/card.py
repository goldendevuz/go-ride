from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel
from apps.v1.shared.validators import validate_full_name, validate_not_past


class Card(BaseModel):
    wallet = models.ForeignKey(
        "finances.Wallet",
        on_delete=models.CASCADE,
        related_name="cards",
        verbose_name=_("Wallet"),
        help_text=_("The wallet this card belongs to"),
    )
    number = models.CharField(
        verbose_name=_("Card Number"),
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(r"^\d{16}$", _("Card number must be 16 digits")),
        ],
        help_text=_("The 16-digit card number"),
    )
    account_holder_name = models.CharField(
        verbose_name=_("Account Holder Name"),
        max_length=255,
        validators=[validate_full_name],
        help_text=_("The full name of the account holder"),
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expires At"),
        validators=[validate_not_past],
        help_text=_("The expiration date of the card (must not be in the past)"),
    )
    cvv = models.PositiveSmallIntegerField(
        verbose_name=_("CVV"),
        validators=[
            MinValueValidator(100),
            MaxValueValidator(999),
        ],
        help_text=_("The 3-digit CVV security code"),
    )

    class Meta:
        ordering = ["wallet"]
        verbose_name = _("Card")
        verbose_name_plural = _("Cards")

    def __str__(self):
        return f"{self.account_holder_name} - {self.number}"
