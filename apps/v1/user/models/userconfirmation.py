from datetime import timedelta
from django.core.exceptions import ValidationError
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
        return str(self.user)

    def clean(self):
        # expiration_time must be in future (or equal to now)
        if self.expiration_time and self.expiration_time < timezone.now():
            raise ValidationError({'expiration_time': "Expiration time cannot be in the past."})

        # code should be 4 digits (optional stricter validation)
        if not self.code.isdigit() or len(self.code) != 4:
            raise ValidationError({'code': "Code must be exactly 4 digits."})

        # verify_type must be valid choice (usually guaranteed by CharField choices)
        if self.verify_type not in dict(self.TYPE_CHOICES):
            raise ValidationError({'verify_type': "Invalid verify type."})

    def save(self, *args, **kwargs):
        # Set expiration time before saving
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = timezone.now() + timedelta(minutes=EMAIL_EXPIRE)
        else:
            self.expiration_time = timezone.now() + timedelta(minutes=PHONE_EXPIRE)

        self.full_clean()  # this will call clean() and validate fields

        super(UserConfirmation, self).save(*args, **kwargs)