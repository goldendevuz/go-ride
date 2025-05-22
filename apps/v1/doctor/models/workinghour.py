from django.core.exceptions import ValidationError
from django.db import models
from . import Doctor
from ...shared.models import BaseModel

class WorkingHour(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='working_hours')
    day_of_week = models.IntegerField(choices=[
        (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
        (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def clean(self):
        if self.start_time is not None and self.end_time is not None:
            if self.start_time >= self.end_time:
                raise ValidationError("Ish boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak.")

            overlapping_hours = WorkingHour.objects.filter(
                doctor=self.doctor,
                day_of_week=self.day_of_week
            ).exclude(pk=self.pk)

            for wh in overlapping_hours:
                if (self.start_time < wh.end_time) and (self.end_time > wh.start_time):
                    raise ValidationError(
                        f"Bu vaqt boshqa kiritilgan vaqt bilan mos kelmaydi: {wh.start_time} - {wh.end_time}"
                    )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.doctor} | {self.get_day_of_week_display()} {self.start_time} - {self.end_time}"