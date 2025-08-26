from django.db import models
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import SeatsCountChoices, AppointmentStatuses

class Appointment(BaseModel):
    profile = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="appointments")
    from_address = models.ForeignKey("users.Address", on_delete=models.CASCADE, related_name="appointments_from")
    to_address = models.ForeignKey("users.Address", on_delete=models.CASCADE, related_name="appointments_to")
    pickup_address = models.ForeignKey("users.Address", on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments_pickup")
    seats_count = models.CharField(max_length=20, choices=SeatsCountChoices.choices, default=SeatsCountChoices.ONE_SEAT)
    payment = models.ForeignKey("finances.Payment", on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")
    promotion = models.ForeignKey("finances.Promotion", on_delete=models.CASCADE, related_name="appointments")
    total_price = models.IntegerField()
    status = models.CharField(max_length=20, choices=AppointmentStatuses.choices, default=AppointmentStatuses.PENDING)
    duration = models.SmallIntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    average_speed = models.SmallIntegerField(blank=True, null=True)
    mood_during_trip = models.ForeignKey("users.Mood", on_delete=models.CASCADE, related_name="appointments")
    date = models.DateField()
    time = models.TimeField()
    picked_up_at = models.DateTimeField(blank=True, null=True)
    ride = models.ForeignKey("rides.Ride", on_delete=models.SET_NULL, null=True, blank=True, related_name="appointments")

    class Meta:
        ordering = ["date", "time"]
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"Appointment {self.id} - {self.profile}"
