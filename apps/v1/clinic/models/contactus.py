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