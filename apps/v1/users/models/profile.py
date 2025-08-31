from django.db import models

from apps.v1.shared.enums import GenderChoices, RoleChoices, ThemeChoices
from apps.v1.shared.validators import phone_regex, validate_age, validate_full_name
from apps.v1.shared.models import BaseModel
# from core.envs import DEFAULT_LANGUAGE_ID # This line is no longer needed

class Profile(BaseModel):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name='profile')
    is_location_enabled = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='profiles/avatars/', null=True, blank=True)
    theme = models.CharField(choices=ThemeChoices.choices, default=ThemeChoices.SYSTEM)
    app_language = models.ForeignKey(
        "users.Language",
        on_delete=models.SET_NULL,
        related_name="profiles",
        null=True,
        blank=True,
    )
    gender = models.CharField(choices=GenderChoices.choices, max_length=10, null=True, blank=True)
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
    role = models.CharField(max_length=31, choices=RoleChoices.choices, default=RoleChoices.CUSTOMER)

    def __str__(self):
        return str(self.user)