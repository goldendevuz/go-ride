from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now

from apps.v1.system.models import NotificationSetting, Payment
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationSetting.objects.create(user=instance)
        print(f"Notification settings created for {instance}")

@receiver(pre_save, sender=Payment)
def validate_payment_status(sender, instance, **kwargs):
    if instance.pk:
        prev = Payment.objects.get(pk=instance.pk)
        if prev.status != instance.status:
            print(f"Payment {instance.id} status changed from {prev.status} to {instance.status}")

            # Auto-fill reviewed_by and reviewed_at if going to PAID or REFUNDED
            if instance.status in [Payment.Status.PAID, Payment.Status.REFUNDED]:
                if not instance.reviewed_by:
                    instance.reviewed_by = instance.user  # fallback
                if not instance.reviewed_at:
                    instance.reviewed_at = now()