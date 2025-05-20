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