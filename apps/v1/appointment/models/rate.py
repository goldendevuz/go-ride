from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.v1.appointment.models.review import Review
from apps.v1.shared.models import BaseModel

User = get_user_model()

class Rate(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='rates')
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user} rated {self.value}⭐"