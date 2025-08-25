from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now

from apps.v1.system.models import NotificationSetting, Payment
from django.contrib.auth import get_user_model
from apps.v1.system.models import Notification
from apps.v1.system.tasks import send_notification

User = get_user_model()

@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationSetting.objects.create(user=instance)
        print(f"Notification settings created for {instance}")

@receiver(pre_save, sender=Payment)
def validate_payment_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            prev = Payment.objects.get(pk=instance.pk)
        except Payment.DoesNotExist:
            prev = None
        if prev and prev.status != instance.status:
            print(f"Payment {instance.id} status changed from {prev.status} to {instance.status}")
            if instance.status in [Payment.Status.PAID, Payment.Status.REFUNDED]:
                if not instance.reviewed_by:
                    instance.reviewed_by = instance.user
                if not instance.reviewed_at:
                    instance.reviewed_at = now()

@receiver(post_save, sender=Notification)
def schedule_notification_task(sender, instance, created, **kwargs):
    if created:
        eta = instance.send_at
        if eta > now():
            # Taskni rejalashtirilgan vaqtda ishlatish
            send_notification.apply_async((instance.id,), eta=eta)
        else:
            # Vaqt o'tib ketgan bo'lsa, hozir ishlasin
            send_notification.delay(instance.id)