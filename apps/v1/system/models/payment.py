from django.db import models
from apps.v1.shared.enums import PaymentStatuses
from apps.v1.shared.models import BaseModel


class Payment(BaseModel):
    profile = models.ForeignKey(
        "user.Profile",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount = models.PositiveIntegerField()
    payment_type = models.ForeignKey(
        "system.PaymentType",
        on_delete=models.PROTECT,
        related_name="payments",
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        "user.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_payments",
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatuses.choices,
        default=PaymentStatuses.PENDING,
    )
    receipt = models.FileField(
        upload_to="payments/receipts/",
        null=True,
        blank=True,
        unique=True,
    )

    def __str__(self):
        return f"Payment {self.id} - {self.profile} - {self.status}"
