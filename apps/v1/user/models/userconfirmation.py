from datetime import timedelta
from django.db import models
from django.utils import timezone

from apps.v1.shared.models import BaseModel

PATIENT, DOCTOR, ADMIN = ("patient", 'doctor', 'admin')
VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')

PHONE_EXPIRE = 5
EMAIL_EXPIRE = 1

class UserConfirmation(BaseModel):
    TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, choices=TYPE_CHOICES)
    verify_value = models.CharField(max_length=31, null=True, blank=True)
    user = models.ForeignKey('user.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:  # 30-mart 11-33 + 5minutes
            self.expiration_time = timezone.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)