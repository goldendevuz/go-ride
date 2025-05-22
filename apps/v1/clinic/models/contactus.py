from django.core.exceptions import ValidationError
from django.db import models

from apps.v1.shared.models import BaseModel

class ContactUs(BaseModel):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Icon CSS class or name")
    url = models.URLField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def clean(self):
        # url http:// yoki https:// bilan boshlanishini tekshirish (URLField ichida bo'lishi mumkin, qo'shimcha tekshiruv)
        if self.url and not self.url.startswith(('http://', 'https://')):
            raise ValidationError({'url': 'URL http:// yoki https:// bilan boshlanishi kerak.'})

    def save(self, *args, **kwargs):
        self.full_clean()  # clean() chaqiriladi
        super().save(*args, **kwargs)