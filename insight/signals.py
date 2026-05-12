"""Storage cleanup signals for the insight app.

Mirrors `partners.signals` / `events.signals` — when a model's FileField/
ImageField is cleared or replaced, the obsolete file is removed from
storage so Cloudinary doesn't accumulate orphans. Wired up automatically
for every insight model that has at least one FileField/ImageField.
"""

import logging

from django.db.models import FileField
from django.db.models.signals import pre_delete, pre_save

logger = logging.getLogger(__name__)


def _file_fields(sender):
    return [f for f in sender._meta.get_fields() if isinstance(f, FileField)]


def _delete_obsolete_files(sender, instance, **kwargs):
    if not instance.pk:
        return

    file_fields = _file_fields(sender)
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


def _delete_files_on_instance_delete(sender, instance, **kwargs):
    for field in _file_fields(sender):
        file_value = getattr(instance, field.name)
        if not file_value:
            continue
        try:
            file_value.delete(save=False)
        except Exception as exc:
            logger.warning(
                "Failed to delete file %s on %s.%s during delete: %s",
                file_value, sender.__name__, field.name, exc,
            )


def register():
    from django.apps import apps

    for model in apps.get_app_config("insight").get_models():
        if any(isinstance(f, FileField) for f in model._meta.get_fields()):
            pre_save.connect(_delete_obsolete_files, sender=model)
            pre_delete.connect(_delete_files_on_instance_delete, sender=model)
