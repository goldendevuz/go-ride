from django.db import models
from apps.v1.shared.models import BaseModel
from apps.v1.shared.enums import FAQCategories

class FAQ(BaseModel):
    category = models.CharField(
        max_length=50,
        choices=FAQCategories.choices,
        unique=True,
        default=FAQCategories.GENERAL
    )
    question = models.CharField(max_length=255, unique=True)
    answer = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["category"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
