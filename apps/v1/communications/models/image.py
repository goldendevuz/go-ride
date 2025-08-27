from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from apps.v1.shared.models import BaseModel


class Image(BaseModel, TranslatableModel):
    file = models.BinaryField(
        verbose_name=_("File"),
        unique=True,
        help_text=_("The binary content of the image file"),
    )

    translations = TranslatedFields(
        alt_text=models.CharField(
            verbose_name=_("Alt Text"),
            max_length=255,
            blank=True,
            null=True,
            help_text=_("Alternative text for the image"),
        ),
    )

    class Meta:
        ordering = ["id"]
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.safe_translation_getter("alt_text", any_language=True) or f"Image {self.id}"
