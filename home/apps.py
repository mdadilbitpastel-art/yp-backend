from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
    verbose_name = "Home Management"

    def ready(self):
        from . import signals
        signals.register()
