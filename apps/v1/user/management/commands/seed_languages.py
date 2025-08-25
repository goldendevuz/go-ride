from django.core.management.base import BaseCommand
from apps.v1.system.models import Language
import uuid


class Command(BaseCommand):
    help = "Seed default languages"

    LANGUAGES = [
        ("english_us", "English (US)"),
        ("russian", "Russian"),
        ("uzbek", "Uzbek"),
        ("arabic", "Arabic"),
        ("tojik", "Tajik"),
        ("yapon", "Japanese"),
    ]

    def handle(self, *args, **kwargs):
        for code, name in self.LANGUAGES:
            obj, created = Language.objects.get_or_create(
                code=code,
                defaults={"id": uuid.uuid4(), "name": name}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created language: {name} ({code})"))
            else:
                self.stdout.write(self.style.WARNING(f"Language already exists: {name} ({code})"))
