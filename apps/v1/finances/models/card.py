from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from apps.v1.shared.models import BaseModel
from apps.v1.shared.validators import validate_full_name, validate_not_past

class Card(BaseModel):
    wallet = models.ForeignKey("finances.Wallet", on_delete=models.CASCADE, related_name="cards")
    number = models.CharField(
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(r'^\d{16}$', "Card number must be 16 digits")
        ]
    )
    account_holder_name = models.CharField(
        max_length=255,
        validators=[validate_full_name]
    )
    expires_at = models.DateTimeField(validators=[validate_not_past])
    cvv = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(999)
        ]
    )

    class Meta:
        ordering = ["wallet"]
        verbose_name = "Card"
        verbose_name_plural = "Cards"

    def __str__(self):
        return f"{self.account_holder_name} - {self.number}"
