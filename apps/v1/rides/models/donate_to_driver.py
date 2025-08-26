from django.db import models
from apps.v1.shared.models import BaseModel

class DonateToDriver(BaseModel):
    profile = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="donations")
    driver = models.ForeignKey("rides.Driver", on_delete=models.CASCADE, related_name="donations")
    amount = models.IntegerField()
    payment = models.ForeignKey("finances.Payment", on_delete=models.CASCADE, related_name="donations")

    class Meta:
        ordering = ["profile"]
        verbose_name = "Donate to Driver"
        verbose_name_plural = "Donations to Drivers"

    def __str__(self):
        return f"{self.profile} -> {self.driver} : {self.amount}"
