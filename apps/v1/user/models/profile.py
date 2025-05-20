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

    def __str__(self):
        return str(self.user)