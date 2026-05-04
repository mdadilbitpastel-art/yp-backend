"""Create the singleton HeaderSettings table."""

import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0016_apply_bottom_button"),
    ]

    operations = [
        migrations.CreateModel(
            name="HeaderSettings",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="header/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
            ],
            options={"verbose_name": "Header", "verbose_name_plural": "Header"},
        ),
    ]
