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