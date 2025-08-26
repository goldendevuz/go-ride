from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.v1.communications.models.notification_setting import NotificationSetting
from apps.v1.finances.models.wallet import Wallet
from .models import Profile, SecuritySetting, LinkedAccount

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_related_objects(sender, instance, created, **kwargs):
    """
    Signal receiver to create a new Profile, SecuritySetting, LinkedAccount, 
    NotificationSetting, and Wallet whenever a new User is created.
    """
    if created:
        # Create the profile first
        if not hasattr(instance, 'profile'):
            profile = Profile.objects.create(user=instance)
        else:
            profile = instance.profile

        # Create the SecuritySetting using the profile
        if not hasattr(profile, 'security_setting'):
            SecuritySetting.objects.create(profile=profile)

        # Create the LinkedAccount using the user instance
        if not hasattr(instance, 'linked_account'):
            LinkedAccount.objects.create(profile=profile)

        # Then create the notification setting using the profile
        if not hasattr(profile, 'notification_setting'):
            NotificationSetting.objects.create(profile=profile)
        
        # Finally, create the wallet using the profile
        if not hasattr(profile, 'wallet'):
            Wallet.objects.create(profile=profile)