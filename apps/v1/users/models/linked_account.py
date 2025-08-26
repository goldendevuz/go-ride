from django.db import models
from apps.v1.shared.models import BaseModel

class LinkedAccount(BaseModel):
    profile = models.OneToOneField("users.profile", on_delete=models.CASCADE, related_name="linked_accounts")
    google = models.BooleanField(default=False)
    apple = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)

    class Meta:
        ordering = ["profile"]
        verbose_name = "Linked Accounts"
        verbose_name_plural = "Linked Accounts"

    def __str__(self):
        return f"Linked Accounts for {self.profile}"
