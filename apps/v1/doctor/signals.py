from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Doctor, History, WorkingHour, SecuritySetting

@receiver(post_save, sender=Doctor)
def create_doctor_related_data(sender, instance, created, **kwargs):
    if created:
        # History yaratish
        History.objects.create(
            doctor=instance,
            action="Doctor profile created."
        )

        # Default WorkingHour (Dushanba–Juma, 9:00–17:00)
        default_working_hours = [
            (0, "09:00", "17:00"),
            (1, "09:00", "17:00"),
            (2, "09:00", "17:00"),
            (3, "09:00", "17:00"),
            (4, "09:00", "17:00"),
        ]
        for day, start, end in default_working_hours:
            WorkingHour.objects.create(
                doctor=instance,
                day_of_week=day,
                start_time=start,
                end_time=end,
            )

        # SecuritySetting yaratish
        SecuritySetting.objects.get_or_create(user=instance.user)
    else:
        # Update bo‘lsa Historyga yozamiz
        History.objects.create(
            doctor=instance,
            action="Doctor profile updated."
        )