from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from apps.v1.shared.models import BaseModel

User = get_user_model()

class Payment(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Failed'
        REFUNDED = 'refunded', 'Refunded'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50)
    receipt = models.FileField(upload_to='payments/receipts/', blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_payments')

    def clean(self):
        super().clean()
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be a positive number.'})

        if self.reviewed_at and not self.reviewed_by:
            raise ValidationError({'reviewed_by': 'Reviewer must be set if reviewed_at is set.'})
        if self.reviewed_by and not self.reviewed_at:
            raise ValidationError({'reviewed_at': 'Review date must be set if reviewed_by is set.'})

    def __str__(self):
        return f"{self.user} - {self.amount} ({self.status})"