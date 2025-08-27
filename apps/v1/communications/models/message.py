from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from apps.v1.shared.models import BaseModel


class Message(BaseModel, TranslatableModel):
    owner = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="sent_messages",
        verbose_name=_("Owner"),
        help_text=_("The profile that sent this message"),
    )
    receiver = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="received_messages",
        verbose_name=_("Receiver"),
        help_text=_("The profile that received this message"),
    )
    has_read = models.BooleanField(
        verbose_name=_("Has Read"),
        default=False,
        help_text=_("Whether the message has been read by the receiver"),
    )

    translations = TranslatedFields(
        text=models.TextField(
            verbose_name=_("Text"),
            blank=True,
            null=True,
            help_text=_("The message text content"),
        ),
    )

    class Meta:
        ordering = ["created"]
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return f"From {self.owner} to {self.receiver}"
