from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from apps.v1.shared.enums import NotificationStates
from apps.v1.shared.models import BaseModel


class Notification(BaseModel, TranslatableModel):
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Profile"),
        help_text=_("The profile that receives this notification"),
    )
    state = models.CharField(
        verbose_name=_("State"),
        max_length=10,
        choices=NotificationStates.choices,
        default=NotificationStates.NEW,
        help_text=_("The current state of the notification"),
    )
    sent_at = models.DateTimeField(
        verbose_name=_("Sent At"),
        default=timezone.now,
        help_text=_("The datetime when the notification was sent"),
    )

    translations = TranslatedFields(
        title=models.CharField(
            verbose_name=_("Title"),
            max_length=255,
            help_text=_("The title of the notification"),
        ),
        description=models.TextField(
            verbose_name=_("Description"),
            help_text=_("The description or body of the notification"),
        ),
    )

    class Meta:
        ordering = ["sent_at"]
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.safe_translation_getter("title", any_language=True)
