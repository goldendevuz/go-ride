from django.db import models
from . import Doctor
from ...shared.models import BaseModel


class History(BaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='history_logs')
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History: {self.doctor} - {self.action[:30]}"