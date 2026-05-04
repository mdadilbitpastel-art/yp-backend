"""Create the FooterSettings singleton and the related FooterLink model."""

import django.db.models.deletion
import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0018_header_tab_labels"),
    ]

    operations = [
        migrations.CreateModel(
            name="FooterSettings",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="footer/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=160)),
                ("address", models.TextField(blank=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("copyright_text", models.CharField(blank=True, max_length=255)),
            ],
            options={"verbose_name": "Footer", "verbose_name_plural": "Footer"},
        ),
        migrations.CreateModel(
            name="FooterLink",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("label", models.CharField(max_length=120)),
                ("url", models.URLField(blank=True)),
                (
                    "footer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="links",
                        to="home.footersettings",
                    ),
                ),
            ],
            options={"ordering": ("order", "id")},
        ),
    ]
