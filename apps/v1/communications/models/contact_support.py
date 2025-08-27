from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from apps.v1.shared.models import BaseModel


class ContactSupport(BaseModel, TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_("Name"),
            max_length=255,
            help_text=_("The display name of the support contact."),
        ),
    )

    icon = models.ImageField(
        verbose_name=_("Icon"),
        upload_to="contact_support_icons/",
        help_text=_("Icon image."),
    )
    display_order = models.PositiveSmallIntegerField(
        verbose_name=_("Display Order"),
        unique=True,
        default=1,
        help_text=_("The order in which this contact appears."),
    )
    url = models.TextField(
        verbose_name=_("URL"),
        unique=True,
        help_text=_("The link to the support contact."),
    )

    class Meta:
        ordering = ["display_order"]
        verbose_name = _("Contact Support")
        verbose_name_plural = _("Contact Supports")

    def __str__(self):
        return self.safe_translation_getter("name", any_language=True) or f"Contact {self.id}"