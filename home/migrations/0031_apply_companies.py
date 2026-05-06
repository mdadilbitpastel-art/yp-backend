"""Replace the 3 inline company field-groups on ApplySection with a related
ApplyCompany model. Existing data (including image paths) is copied across
before the old columns are dropped."""

import django.db.models.deletion
import home.validators
from django.db import migrations, models


_OLD_COMPANY_COUNT = 3
_TEXT_FIELDS = ("label", "title", "description", "button_text", "button_url")
_IMAGE_FIELDS = ("large_image", "small_image")


def _copy_companies_forward(apps, schema_editor):
    ApplySection = apps.get_model("home", "ApplySection")
    ApplyCompany = apps.get_model("home", "ApplyCompany")
    for section in ApplySection.objects.all():
        for i in range(1, _OLD_COMPANY_COUNT + 1):
            text_values = {
                name: (getattr(section, f"apply_company_{i}_{name}", "") or "")
                for name in _TEXT_FIELDS
            }
            image_values = {}
            for name in _IMAGE_FIELDS:
                field_file = getattr(section, f"apply_company_{i}_{name}", None)
                image_values[name] = field_file.name if field_file else ""

            if not (any(text_values.values()) or any(image_values.values())):
                continue

            ApplyCompany.objects.create(
                section=section,
                order=i,
                **text_values,
                **image_values,
            )


def _noop_reverse(apps, schema_editor):
    ApplyCompany = apps.get_model("home", "ApplyCompany")
    ApplyCompany.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0030_network_video_storage"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplyCompany",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
                (
                    "large_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home/apply/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                (
                    "small_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home/apply/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="companies",
                        to="home.applysection",
                    ),
                ),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.RunPython(_copy_companies_forward, _noop_reverse),
        *[
            migrations.RemoveField(
                model_name="applysection",
                name=f"apply_company_{i}_{name}",
            )
            for i in range(1, _OLD_COMPANY_COUNT + 1)
            for name in (*_TEXT_FIELDS, *_IMAGE_FIELDS)
        ],
    ]
