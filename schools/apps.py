from django.apps import AppConfig


class SchoolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "schools"
    verbose_name = "Schools Management"

    def ready(self):
        from . import signals
        signals.register()
