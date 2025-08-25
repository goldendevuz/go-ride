import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.v1.shared.enums import AuthStatus
from apps.v1.shared.models import BaseModel
from apps.v1.shared.validators import validate_password, validate_username
from ..managers import UserManager


class User(AbstractUser, BaseModel):
    # completely remove them
    email = None  
    first_name = None
    last_name = None

    auth_status = models.CharField(
        max_length=31,
        choices=AuthStatus,
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
    REQUIRED_FIELDS = []

    objects = UserManager()  # 🔑 attach the custom manager

    def __str__(self):
        return self.username or f"user-{self.id}"

    def token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }

    def create_verify_code(self, verify_type, verify_value=None):
        from .userconfirmation import UserConfirmation
        code = f"{random.randint(1000, 9999)}"
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            verify_value=verify_value,
            code=code,
        )
        return code
