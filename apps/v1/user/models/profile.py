import uuid
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth import get_user_model

from apps.v1.shared.enums import GenderChoices, RoleChoices, ThemeChoices
from apps.v1.shared.validators import phone_regex, validate_age, validate_email_lower, validate_full_name
from apps.v1.shared.models import BaseModel
from apps.v1.system.models.language import Language

User = get_user_model()

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_location_enabled = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='profiles/avatars/', null=True, blank=True)
    theme = models.CharField(choices=ThemeChoices, default=ThemeChoices.SYSTEM)
    app_language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        related_name="profiles",
        null=True,
        blank=True,
        default=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),  # DB-level default
    )

    phone = models.CharField(
        max_length=13,
        validators=[MinLengthValidator(13), phone_regex],
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
        validators=[validate_email_lower],
        null=True,
        blank=True,
    )
    gender = models.CharField(choices=GenderChoices, max_length=10, null=True, blank=True)
    birth_date = models.DateField(
        null=True,
        blank=True,
        validators=[validate_age],
    )
    full_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        validators=[validate_full_name],
    )
    role = models.CharField(max_length=31, choices=RoleChoices, default=RoleChoices.CUSTOMER)

    def __str__(self):
        return str(self.user)