"""Storage cleanup signals.

When a model's FileField/ImageField is cleared (X icon in dashboard) or
replaced with a new upload, the old file is left orphaned in remote
storage (Cloudinary). These pre_save handlers compare the persisted value
with the incoming value and delete the obsolete file from storage.
"""

import logging

from django.db.models import FileField
from django.db.models.signals import pre_save

logger = logging.getLogger(__name__)


def _delete_obsolete_files(sender, instance, **kwargs):
    if not instance.pk:
        return

    file_fields = [f for f in sender._meta.get_fields() if isinstance(f, FileField)]
    if not file_fields:
        return

    try:
        old = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in file_fields:
        old_file = getattr(old, field.name)
        new_file = getattr(instance, field.name)
        if not old_file:
            continue
        if old_file == new_file:
            continue
        try:
            old_file.delete(save=False)
        except Exception as exc:
            logger.warning(
                "Failed to delete old file %s on %s.%s: %s",
                old_file, sender.__name__, field.name, exc,
            )


def register():
    """Wire up the pre_save handler for every model in the `home` app
    that has at least one FileField/ImageField."""
    from django.apps import apps

    for model in apps.get_app_config("home").get_models():
        if any(isinstance(f, FileField) for f in model._meta.get_fields()):
            pre_save.connect(_delete_obsolete_files, sender=model)
