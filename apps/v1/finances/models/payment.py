from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from apps.v1.shared.enums import PaymentStatuses
from apps.v1.shared.models import BaseModel


class Payment(BaseModel):
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name=_("Profile"),
        help_text=_("The profile that made the payment"),
    )
    amount = models.PositiveIntegerField(
        verbose_name=_("Amount"),
        validators=[MinValueValidator(1000)],
        help_text=_("The amount of the payment (minimum 1000)"),
    )
    payment_type = models.ForeignKey(
        "finances.PaymentType",
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name=_("Payment Type"),
        help_text=_("The type of payment used"),
    )
    paid_at = models.DateTimeField(
        verbose_name=_("Paid At"),
        null=True,
        blank=True,
        help_text=_("The datetime when the payment was completed"),
    )
    reviewed_by = models.ForeignKey(
        "users.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_payments",
        verbose_name=_("Reviewed By"),
        help_text=_("The profile that reviewed this payment"),
    )
    reviewed_at = models.DateTimeField(
        verbose_name=_("Reviewed At"),
        null=True,
        blank=True,
        help_text=_("The datetime when the payment was reviewed"),
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=PaymentStatuses.choices,
        default=PaymentStatuses.PENDING,
        help_text=_("The current status of the payment"),
    )
    receipt = models.FileField(
        verbose_name=_("Receipt"),
        upload_to="payments/receipts/",
        null=True,
        blank=True,
        help_text=_("An optional uploaded receipt for the payment"),
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return f"Payment {self.id} - {self.profile} - {self.status}"
