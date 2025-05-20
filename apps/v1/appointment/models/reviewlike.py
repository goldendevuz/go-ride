from django.contrib.auth import get_user_model
from django.db import models

from apps.v1.appointment.models.review import Review
from apps.v1.shared.models import BaseModel

User = get_user_model()

class ReviewLike(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_reviews')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"{self.user} liked review {self.review.id}"
