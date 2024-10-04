from django.apps import AppConfig

class Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dsud"

    def ready(self):
        import dsud.signals

