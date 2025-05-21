from django.apps import AppConfig

class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.v1.system'
    def ready(self):
        import apps.v1.system.signals # noqa