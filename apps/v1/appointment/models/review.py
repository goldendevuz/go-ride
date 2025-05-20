from django.contrib.auth import get_user_model
from django.db import models

from apps.v1.appointment.models import Appointment
from apps.v1.shared.models import BaseModel

User = get_user_model()

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    recommend = models.BooleanField(default=True)

    def __str__(self):
        return f"Review by {self.user} - {self.rating}⭐"