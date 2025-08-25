from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from ...clinic.models import Specialty, Hospital
from ...shared.models import BaseModel

User = get_user_model()

class Doctor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, related_name='doctor')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, related_name='doctor')
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    review_count = models.PositiveIntegerField(default=0)
    about = models.TextField(blank=True)

    def __str__(self):
        # Agar user full name bo'lmasa, username ko'rsatiladi
        full_name = self.user.get_full_name()
        if not full_name.strip():
            full_name = self.user.username
        return f"Dr. {full_name}"