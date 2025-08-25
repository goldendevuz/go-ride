from django.core.exceptions import ValidationError
from django.db import models

from apps.v1.shared.models import BaseModel

class Banner(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='banners/')
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def clean(self):
        # Agar url berilgan bo‘lsa, tekshirish (URLField o‘zida validatsiya bor, shuning uchun ko‘p kerak emas)
        if self.url and not self.url.startswith(('http://', 'https://')):
            raise ValidationError({'url': 'URL http:// yoki https:// bilan boshlanishi kerak.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # clean() ni chaqiradi
        super().save(*args, **kwargs)