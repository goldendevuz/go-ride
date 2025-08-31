from django.db import models
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import DiscountType

class Promotion(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    discount_percent = models.SmallIntegerField(blank=True, null=True)
    discount_amount = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(
        max_length=10,
        choices=DiscountType.choices,
        default=DiscountType.PERCENT
    )
    valid_to = models.DateTimeField(blank=True, null=True)
    image_url = models.CharField(max_length=255, unique=True)
    minimum_spend = models.IntegerField(blank=True, null=True)
    usage_limit = models.SmallIntegerField(blank=True, null=True)
    used_count = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ["name"]
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def __str__(self):
        return self.name
