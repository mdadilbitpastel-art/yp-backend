"""Drop the legacy HomePage singleton and introduce HeroSection."""

import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_homepage_delete_feature_delete_herosection_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="HomePage",
        ),
        migrations.CreateModel(
            name="HeroSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("subtitle", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField()),
                ("highlight_text", models.CharField(blank=True, help_text='Inline highlight, e.g. "600,000 students".', max_length=160)),
                ("primary_button_text", models.CharField(blank=True, max_length=80)),
                ("primary_button_url", models.URLField(blank=True)),
                ("secondary_button_text", models.CharField(blank=True, max_length=80)),
                ("secondary_button_url", models.URLField(blank=True)),
                ("app_store_url", models.URLField(blank=True)),
                ("play_store_url", models.URLField(blank=True)),
                (
                    "background_image",
                    models.ImageField(
                        upload_to="home/hero/backgrounds/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                (
                    "hero_image",
                    models.ImageField(
                        upload_to="home/hero/foreground/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Hero Section",
                "verbose_name_plural": "Hero Sections",
                "ordering": ["-created_at"],
            },
        ),
    ]
