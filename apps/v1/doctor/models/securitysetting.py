from django.contrib.auth import get_user_model
from django.db import models
from ...shared.models import BaseModel

User = get_user_model()

class SecuritySetting(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_settings')
    remember_me = models.BooleanField(default=False)
    face_id = models.BooleanField(default=False)
    biometric_id = models.BooleanField(default=False)

    def __str__(self):
        return f"Security Settings for {self.user}"