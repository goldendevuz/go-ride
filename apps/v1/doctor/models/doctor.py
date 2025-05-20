from django.contrib.auth import get_user_model
from django.db import models

from ...clinic.models import Specialty, Hospital
from ...shared.models import BaseModel

User = get_user_model()

class Doctor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, related_name='doctor')
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, related_name='doctor')
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    review_count = models.PositiveIntegerField(default=0)
    about = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"