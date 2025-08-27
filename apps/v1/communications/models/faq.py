from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import FAQCategories


class FAQ(BaseModel, TranslatableModel):
    category = models.CharField(
        verbose_name=_("Category"),
        max_length=50,
        choices=FAQCategories.choices,
        default=FAQCategories.GENERAL,
        help_text=_("The category this FAQ belongs to."),
    )

    translations = TranslatedFields(
        question=models.CharField(
            verbose_name=_("Question"),
            max_length=255,
            help_text=_("The FAQ question text."),
        ),
        answer=models.TextField(
            verbose_name=_("Answer"),
            help_text=_("The FAQ answer text."),
        ),
    )

    class Meta:
        ordering = ["category"]
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")

    def __str__(self):
        return self.safe_translation_getter("question", any_language=True) or f"FAQ {self.id}"