from django.db import models
from apps.v1.shared.models import BaseModel

class Driver(BaseModel):
    profile = models.OneToOneField("users.profile", on_delete=models.CASCADE, related_name="driver")
    car = models.OneToOneField("rides.Car", on_delete=models.CASCADE, related_name="driver")
    ride_orders_count = models.SmallIntegerField(default=0)
    experience_in_years = models.SmallIntegerField(blank=True, null=True)
    member_from_date = models.DateTimeField(blank=True, null=True)
    ratings_count = models.SmallIntegerField(default=0)
    total_rating = models.SmallIntegerField(default=0)
    average_rating = models.FloatField(default=0)

    class Meta:
        ordering = ["profile"]
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
        return f"{self.profile}"
