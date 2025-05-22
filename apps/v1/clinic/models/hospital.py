from django.core.exceptions import ValidationError
from django.db import models
from apps.v1.shared.models import BaseModel

class Hospital(BaseModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='hospitals/logos/', blank=True, null=True)

    def __str__(self):
        return self.name

    def clean(self):
        # Agar telefon raqam kiritilgan bo'lsa, uni formatini oddiy tekshirish
        if self.phone:
            # Oddiy regex misoli, agar kerak bo'lsa phone_regex import qilib ishlatish mumkin
            import re
            pattern = re.compile(r'^\+?[\d\s\-]{7,30}$')
            if not pattern.match(self.phone):
                raise ValidationError({'phone': "Telefon raqam noto'g'ri formatda."})

        # email va website uchun EmailField va URLField o'z ichida validatsiya qiladi,
        # ammo email bo'sh bo'lishi mumkin (blank=True), shuning uchun alohida tekshiruv shart emas

        # website url http:// yoki https:// bilan boshlanishi kerak
        if self.website and not self.website.startswith(('http://', 'https://')):
            raise ValidationError({'website': "Sayt URL 'http://' yoki 'https://' bilan boshlanishi kerak."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)