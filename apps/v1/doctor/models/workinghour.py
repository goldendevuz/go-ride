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

    class Meta:
        unique_together = ('doctor', 'day_of_week')
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.doctor} | {self.get_day_of_week_display()} {self.start_time} - {self.end_time}"