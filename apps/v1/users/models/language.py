from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel


class Language(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        unique=True,
        help_text=_("The full name of the language (e.g., 'English')."),
    )
    code = models.CharField(
        verbose_name=_("Code"),
        max_length=50,
        unique=True,
        default="english_us",
        help_text=_("The unique code for the language (e.g., 'en-us')."),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    def __str__(self):
        return self.name