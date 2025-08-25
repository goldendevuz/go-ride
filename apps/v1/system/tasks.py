from celery import shared_task
from django.utils import timezone
from apps.v1.system.models import Notification

@shared_task
def send_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return f"Notification {notification_id} does not exist."

    # Send logic: (for now, just print)
    print(f"📢 Sending Notification: {notification.title}")
    print(f"Description: {notification.description}")

    notification.state = Notification.State.READ
    notification.save(update_fields=["state"])
    return f"Notification {notification_id} sent at {timezone.now()}"
