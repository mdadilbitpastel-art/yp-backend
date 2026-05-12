from django.apps import AppConfig


class InsightConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "insight"
    verbose_name = "Insight Management"

    def ready(self):
        from . import signals
        signals.register()
