from django.db import models
from apps.v1.shared.models import BaseModel

class Ride(BaseModel):
    driver = models.ForeignKey("rides.Driver", on_delete=models.CASCADE, related_name="rides")
    from_address = models.ForeignKey("users.Address", on_delete=models.CASCADE, related_name="rides_from")
    to_address = models.ForeignKey("users.Address", on_delete=models.CASCADE, related_name="rides_to")
    departure = models.DateTimeField(blank=True, null=True)
    price_per_seat = models.FloatField(default=0)
    total_seats_count = models.SmallIntegerField(default=3)

    class Meta:
        ordering = ["departure"]
        verbose_name = "Ride"
        verbose_name_plural = "Rides"

    def __str__(self):
        return f"{self.driver} - {self.from_address} to {self.to_address}"
