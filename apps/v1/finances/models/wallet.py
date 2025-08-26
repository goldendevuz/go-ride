from django.db import models
from apps.v1.shared.models import BaseModel

class Wallet(BaseModel):
    profile = models.OneToOneField("users.profile", on_delete=models.CASCADE, related_name="wallet")
    balance = models.IntegerField(default=0)

    class Meta:
        ordering = ["profile"]
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.profile} - {self.balance}"
