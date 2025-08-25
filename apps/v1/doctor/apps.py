from django.apps import AppConfig

class DoctorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.v1.doctor'
    def ready(self):
        import apps.v1.doctor.signals # noqa