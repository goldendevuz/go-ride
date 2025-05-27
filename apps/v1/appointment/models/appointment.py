from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

from django.utils.timezone import make_aware

from .reason import Reason
from apps.v1.clinic.models import Service
from apps.v1.doctor.models import Doctor
from apps.v1.shared.models import BaseModel

User = get_user_model()

class Appointment(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        CANCELED = 'canceled', 'Canceled'
        COMPLETED = 'completed', 'Completed'
        RESCHEDULED = 'rescheduled', 'Rescheduled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    age = models.PositiveIntegerField()
    problem = models.TextField(blank=True)
    reason = models.ForeignKey(Reason, on_delete=models.SET_NULL, null=True, related_name='appointments')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    @property
    def appointment_time(self):
        if self.date and self.time:
            return datetime.combine(self.date, self.time)
        return None

    def clean(self):
        super().clean()
        if self.date and self.time:
            combined_datetime = datetime.combine(self.date, self.time)

            # Convert to timezone-aware datetime if it's naive
            if timezone.is_naive(combined_datetime):
                combined_datetime = make_aware(combined_datetime)

            if combined_datetime < timezone.now():
                raise ValidationError({'date': 'Appointment date and time cannot be in the past.'})
    def __str__(self):
        return f"{self.full_name} with Dr. {self.doctor.user.get_full_name()} on {self.date} at {self.time}"