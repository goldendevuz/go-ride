import random
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from apps.v1.shared.models import BaseModel
from .userconfirmation import UserConfirmation
from ..managers import UserManager

PATIENT, DOCTOR, ADMIN = ("patient", 'doctor', 'admin')
VIA_EMAIL, VIA_PHONE = ("via_email", "via_phone")
NEW, CODE_VERIFIED, DONE, PHOTO_DONE = ('new', 'code_verified', 'done', 'photo_done')

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Telefon raqam quyidagi formatda bo'lishi kerak: '+998XXXXXXXXX' (masalan, +998901234567)."
)

class User(AbstractUser, BaseModel):
    ROLE = (
        (PATIENT, PATIENT),
        (DOCTOR, DOCTOR),
        (ADMIN, ADMIN)
    )
    AUTH_TYPE_CHOICES = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )
    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )
    objects = UserManager()
    role = models.CharField(max_length=31, choices=ROLE, default=PATIENT)
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE_CHOICES)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True, validators=[phone_regex])
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'heic', 'heif'])])
    remember_me = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    def create_verify_code(self, verify_type, verify_value=None):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            verify_value=verify_value,
            code=code
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f'user-{uuid.uuid4().__str__().split("-")[-1]}'
            while User.objects.filter(username=temp_username).exists():
                temp_username = f"{temp_username}{random.randint(0,9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            self.email = self.email.lower()

    def check_pass(self):
        if not self.password:
            temp_password = f'password-{uuid.uuid4().__str__().split("-")[-1]}'
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()