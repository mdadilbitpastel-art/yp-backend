"""Add the Feature section fields (title, description, 5 fixed cards) to HeroSection.

The whole homepage lives in a single singleton row, so feature data is added
as flat columns rather than a separate table.
"""

import home.validators
from django.db import migrations, models


def _icon_field():
    return models.ImageField(
        blank=True,
        null=True,
        upload_to="home/features/",
        validators=[
            home.validators.validate_image_size,
            home.validators.validate_image_extension,
        ],
    )


def _card_fields(position: int):
    return [
        (f"feature_{position}_title", models.CharField(blank=True, max_length=255)),
        (f"feature_{position}_icon", _icon_field()),
        (f"feature_{position}_button_url", models.URLField(blank=True)),
        (f"feature_{position}_button_text", models.CharField(blank=True, max_length=80)),
        (f"feature_{position}_is_active", models.BooleanField(default=True)),
    ]


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0005_remove_unused_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="features_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name="features_description",
            field=models.TextField(blank=True),
        ),
        *[
            migrations.AddField(
                model_name="herosection",
                name=name,
                field=field,
            )
            for position in range(1, 6)
            for name, field in _card_fields(position)
        ],
    ]
