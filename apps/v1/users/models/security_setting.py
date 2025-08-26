from django.db import models
from apps.v1.shared.models import BaseModel

class SecuritySetting(BaseModel):
    profile = models.OneToOneField("users.profile", on_delete=models.CASCADE, related_name="security_setting")
    biometric_id = models.BooleanField(default=False)
    face_id = models.BooleanField(default=False)
    sms_authenticator = models.BooleanField(default=False)
    google_authenticator = models.BooleanField(default=False)

    class Meta:
        ordering = ["profile"]
        verbose_name = "Security Setting"
        verbose_name_plural = "Security Settings"

    def __str__(self):
        return f"Security Setting for {self.profile}"
