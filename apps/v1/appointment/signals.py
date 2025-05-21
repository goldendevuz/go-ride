from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Appointment, Review

@receiver(post_save, sender=Appointment)
def handle_appointment_status_change(sender, instance, created, **kwargs):
    if not created:
        if instance.status == Appointment.Status.COMPLETED:
            has_review = Review.objects.filter(appointment=instance).exists()
            if not has_review:
                # You can trigger a Notification here
                print(f"User {instance.user} can now write a review for appointment {instance.id}")
        elif instance.status == Appointment.Status.CANCELED:
            print(f"Appointment {instance.id} was canceled by {instance.user}")
        elif instance.status == Appointment.Status.RESCHEDULED:
            print(f"Appointment {instance.id} was rescheduled by {instance.user}")