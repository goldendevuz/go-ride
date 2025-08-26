from django.db import models
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import ReasonTypes

class Reason(BaseModel):
    profile = models.ForeignKey("users.profile", on_delete=models.CASCADE, related_name="reasons")
    reason_type = models.CharField(
        max_length=50,
        choices=ReasonTypes.choices,
        default=ReasonTypes.CHANGE_IN_PLANS
    )
    message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["profile"]
        verbose_name = "Reason"
        verbose_name_plural = "Reasons"

    def __str__(self):
        return f"{self.profile} - {self.reason_type}"
