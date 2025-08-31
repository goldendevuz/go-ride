from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.v1.shared.models import BaseModel


class Mood(BaseModel):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=50,
        unique=True,
        help_text=_("The name of the mood (e.g., 'Happy', 'Sad').")
    )
    smile = models.ImageField(
        verbose_name=_("Icon"),
        upload_to="moods/icons/",
        help_text=_("An icon representing the mood.")
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("Mood")
        verbose_name_plural = _("Moods")

    def __str__(self):
        return self.name