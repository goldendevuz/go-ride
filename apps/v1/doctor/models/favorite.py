from django.contrib.auth import get_user_model
from django.db import models
from . import Doctor
from ...shared.models import BaseModel

User = get_user_model()

class Favorite(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_doctors')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'doctor')
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

    def __str__(self):
        return f"{self.user} ❤️ {self.doctor}"