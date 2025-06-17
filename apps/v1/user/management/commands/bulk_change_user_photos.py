import requests
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from apps.v1.user.models import User
from apps.v1.user.tasks import process_user_photo

PHOTO_DONE = 'photo_done'

class Command(BaseCommand):
    help = 'Assign realistic AI-generated photos from thispersondoesnotexist.com'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count = 0

        for user in users:
            try:
                url = "https://thispersondoesnotexist.com"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code != 200:
                    self.stdout.write(self.style.WARNING(f"⚠️ Rasm xatosi: {response.status_code}"))
                    continue

                image_content = BytesIO(response.content)
                image_name = f"user_{user.id}.jpg"

                uploaded_file = SimpleUploadedFile(
                    name=image_name,
                    content=image_content.read(),
                    content_type='image/jpeg'
                )

                user.photo = uploaded_file
                user.auth_status = PHOTO_DONE
                user.save()

                process_user_photo.delay(user.id)
                count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ {user.id} - Xatolik: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ {count} ta foydalanuvchiga AI-photo biriktirildi."))
