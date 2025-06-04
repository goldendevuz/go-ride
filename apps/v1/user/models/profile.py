from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from apps.v1.shared.models import BaseModel
from . import User

class Profile(BaseModel):
    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, null=True, blank=True)
    avatar = models.ImageField(upload_to='profiles/avatars/', null=True, blank=True)

    # organization = models.CharField(max_length=255, null=True, blank=True)
    # organization_address = models.CharField(max_length=255, null=True, blank=True)
    # organization_number = models.CharField(max_length=255, null=True, blank=True)
    # type_of_service = models.CharField(max_length=255, null=True, blank=True)
    # function = models.CharField(max_length=255, null=True, blank=True)
    # additional_services = models.TextField(null=True, blank=True)
    # tel_number = models.CharField(max_length=255, null=True, blank=True)
    # full_name = models.CharField(max_length=255, null=True, blank=True)
    # city = models.CharField(max_length=255, null=True, blank=True)
    # location = models.CharField(max_length=255, null=True, blank=True)
    # price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # working_hours = models.CharField(max_length=255, null=True, blank=True)
    # weekend = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def clean(self):
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValidationError({'birth_date': "Birth date cannot be in the future."})