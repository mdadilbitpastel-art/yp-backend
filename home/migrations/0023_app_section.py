"""Create the App promotion singleton section."""

import home.validators
from django.db import migrations, models


def _image_field():
    return models.ImageField(
        blank=True,
        null=True,
        upload_to="home/app/",
        validators=[
            home.validators.validate_image_size,
            home.validators.validate_image_extension,
        ],
    )


def _button_fields(i):
    return [
        (f"button_{i}_text", models.CharField(blank=True, max_length=80)),
        (f"button_{i}_url", models.URLField(blank=True)),
    ]


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0022_testimonials_title"),
    ]

    operations = [
        migrations.CreateModel(
            name="AppSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                *_button_fields(1),
                *_button_fields(2),
                *_button_fields(3),
                ("side_image", _image_field()),
                ("barcode_image", _image_field()),
            ],
            options={"verbose_name": "App Section", "verbose_name_plural": "App Section"},
        ),
    ]
