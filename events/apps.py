from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"
    verbose_name = "Events Management"

    def ready(self):
        from . import signals
        signals.register()
