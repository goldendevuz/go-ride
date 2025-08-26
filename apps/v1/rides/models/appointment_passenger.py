from django.db import models
from apps.v1.shared.models import BaseModel

class AppointmentPassenger(BaseModel):
    appointment = models.ForeignKey("rides.Appointment", on_delete=models.CASCADE, related_name="passengers")
    passenger = models.ForeignKey("rides.Passenger", on_delete=models.CASCADE, related_name="appointments")
    seat_number = models.SmallIntegerField(blank=True, null=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["appointment", "seat_number"]
        verbose_name = "Appointment Passenger"
        verbose_name_plural = "Appointment Passengers"

    def __str__(self):
        return f"{self.passenger} - Appointment {self.appointment.id}"
