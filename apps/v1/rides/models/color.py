from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel


class Color(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        unique=True,
        help_text=_("The name of the color."),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Color")
        verbose_name_plural = _("Colors")

    def __str__(self):
        return self.name