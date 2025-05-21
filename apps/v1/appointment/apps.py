from django.apps import AppConfig

class AppointmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.v1.appointment'
    def ready(self):
        import apps.v1.appointment.signals # noqa