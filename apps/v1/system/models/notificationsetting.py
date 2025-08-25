from django.contrib.auth import get_user_model
from django.db import models

from apps.v1.shared.models import BaseModel

User = get_user_model()

class NotificationSetting(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    general = models.BooleanField(default=True)
    sound = models.BooleanField(default=True)
    vibrate = models.BooleanField(default=True)
    special_offers = models.BooleanField(default=True)
    promo_and_discount = models.BooleanField(default=True)
    payments = models.BooleanField(default=True)
    cashback = models.BooleanField(default=True)
    app_updates = models.BooleanField(default=True)
    new_service = models.BooleanField(default=True)
    new_tips = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification Settings for {self.user}"