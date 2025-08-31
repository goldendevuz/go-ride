from django.db import models
from apps.v1.shared.models import BaseModel


class NotificationSetting(BaseModel):
    profile = models.OneToOneField(
        "users.profile",
        on_delete=models.CASCADE,
        related_name="notification_setting",
    )

    general_updates = models.BooleanField(default=True)
    safety_and_security_alerts = models.BooleanField(default=True)
    account_notification = models.BooleanField(default=True)
    ride_status_updates = models.BooleanField(default=True)
    promo_alerts = models.BooleanField(default=True)
    rating_and_reviews = models.BooleanField(default=True)
    personalised_recommendations = models.BooleanField(default=True)
    app_updates = models.BooleanField(default=True)
    service_updates = models.BooleanField(default=True)
    community_forum_activity = models.BooleanField(default=True)
    survey_and_feedback_requests = models.BooleanField(default=True)
    important_announcements = models.BooleanField(default=True)
    app_tips_and_tutorials = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification settings for {self.profile}"
