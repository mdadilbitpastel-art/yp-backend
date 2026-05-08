from django.apps import AppConfig


class EmployersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "employers"
    verbose_name = "Employers Management"

    def ready(self):
        from . import signals
        signals.register()
