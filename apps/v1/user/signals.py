from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, UserConfirmation

User = get_user_model()

@receiver(post_save, sender=User)
def create_related_user_data(sender, instance, created, **kwargs):
    if created:
        # Profile yaratish
        Profile.objects.get_or_create(user=instance)
        # Confirmation yaratish
        # UserConfirmation.objects.get_or_create(user=instance)