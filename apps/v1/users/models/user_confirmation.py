from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.v1.shared.enums import EMAIL_EXPIRE, PHONE_EXPIRE, AuthType
from apps.v1.shared.models import BaseModel
from apps.v1.shared.validators import validate_not_past

User = get_user_model()

class UserConfirmation(BaseModel):
    code = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(9999),
        ],
    )
    verify_type = models.CharField(max_length=31, choices=AuthType.choices, default=AuthType.VIA_PHONE)
    verify_value = models.CharField(max_length=150)
    user = models.ForeignKey(User, models.CASCADE, related_name="verify_codes")
    expires_at = models.DateTimeField(validators=[validate_not_past])
    is_confirmed = models.BooleanField(default=False)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.verify_type}"

    def save(self, *args, **kwargs):
        # Set expiration before validation
        if not self.expires_at:
            if self.verify_type == AuthType.VIA_EMAIL:
                self.expires_at = timezone.now() + timedelta(minutes=EMAIL_EXPIRE)
            else:
                self.expires_at = timezone.now() + timedelta(minutes=PHONE_EXPIRE)

        self.full_clean()
        super().save(*args, **kwargs)