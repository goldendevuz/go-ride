import random
from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from apps.v1.shared.enums import AuthStatus, AuthType, EMAIL_EXPIRE, PHONE_EXPIRE
from apps.v1.shared.models import BaseModel
from apps.v1.shared.validators import validate_password, validate_username, validate_email_lower, phone_regex
from ..managers import UserManager


class User(AbstractUser, BaseModel):
    # Completely remove them
    first_name = None
    last_name = None
    
    # Restore the email field and make it unique but nullable
    email = models.EmailField(
        unique=True,
        validators=[validate_email_lower],
        null=True,
        blank=True,
    )
    
    # Add a nullable phone field, unique but nullable
    phone = models.CharField(
        max_length=13,
        unique=True,
        validators=[phone_regex],
        null=True,
        blank=True,
    )

    auth_status = models.CharField(
        max_length=31,
        choices=AuthStatus.choices,
        default=AuthStatus.NEW,
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[validate_username],
        null=True,
        blank=True,
    )

    password = models.CharField(
        max_length=128,
        validators=[validate_password],
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []  # No required fields during initial creation

    objects = UserManager()

    def __str__(self):
        return self.username or self.email or self.phone or f"user-{self.id}"

    def token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }
    
    def create_verify_code(self, verify_type):
        from .user_confirmation import UserConfirmation

        if verify_type not in [AuthType.VIA_PHONE.value, AuthType.VIA_EMAIL.value]:
            raise ValidationError("Invalid verification type.")

        if verify_type == AuthType.VIA_EMAIL.value and not self.email:
            raise ValidationError("Email is required for email verification.")

        if verify_type == AuthType.VIA_PHONE.value and not self.phone:
            raise ValidationError("Phone number is required for phone verification.")
            
        code = random.randint(1000, 9999)
        verify_value = getattr(self, verify_type)

        UserConfirmation.objects.create(
            user=self,
            verify_type=verify_type,
            verify_value=verify_value,
            code=code,
        )
        return code