from django.core.management.base import BaseCommand

from apps.v1.clinic.models import Hospital

class Command(BaseCommand):
    help = 'Generate 1000 identical hospital entries for testing'

    def handle(self, *args, **kwargs):
        hospitals = []
        for i in range(1000):
            hospitals.append(
                Hospital(
                    name="Test Hospital",
                    address="123 Test Street, Test City",
                    phone="+998901234567",
                    email="test@example.com",
                    website="https://testhospital.uz",
                )
            )

        Hospital.objects.bulk_create(hospitals)
        self.stdout.write(self.style.SUCCESS("✅ 1000 ta hospital muvaffaqiyatli yaratildi."))
