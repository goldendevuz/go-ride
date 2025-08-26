import time
import asyncio
from django.core.management.base import BaseCommand
from apps.v1.users.models import User  # O'zingdagi User modelga moslashtir

REPEAT_COUNT = 100_000
STEP = 10_000

def sync_fetch_user():
    for i in range(REPEAT_COUNT):
        _ = User.objects.first()
        if (i + 1) % STEP == 0:
            print(f"Sync progress: {i + 1} done")

async def async_fetch_user():
    for i in range(REPEAT_COUNT):
        _ = await User.async_objects.afirst()
        if (i + 1) % STEP == 0:
            print(f"Async progress: {i + 1} done")

class Command(BaseCommand):
    help = "Compare performance of sync vs async ORM calls with larger query count"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING(f"🚀 Starting performance test with {REPEAT_COUNT} queries..."))

        # SYNC
        start = time.time()
        sync_fetch_user()
        sync_duration = time.time() - start
        self.stdout.write(self.style.SUCCESS(f"✅ Sync execution time: {sync_duration:.2f} seconds"))

        # ASYNC
        start = time.time()
        asyncio.run(async_fetch_user())
        async_duration = time.time() - start
        self.stdout.write(self.style.SUCCESS(f"✅ Async execution time: {async_duration:.2f} seconds"))

        # Comparison
        diff = sync_duration - async_duration
        faster = "Async" if diff > 0 else "Sync"
        self.stdout.write(self.style.NOTICE(f"🏁 {faster} is faster by {abs(diff):.2f} seconds"))
