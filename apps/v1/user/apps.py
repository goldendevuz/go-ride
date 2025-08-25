from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.v1.user'
    label = 'user'  # 👈 Add this
    def ready(self):
        import apps.v1.user.signals # noqa