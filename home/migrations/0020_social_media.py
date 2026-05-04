"""Create the Social Media singleton section and its related card model."""

import django.db.models.deletion
import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0019_footer"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialMediaSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("heading", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "verbose_name": "Social Media Section",
                "verbose_name_plural": "Social Media Section",
            },
        ),
        migrations.CreateModel(
            name="SocialMediaCard",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("name", models.CharField(max_length=120)),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home/social_media/",
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
                        related_name="cards",
                        to="home.socialmediasection",
                    ),
                ),
            ],
            options={"ordering": ("order", "id")},
        ),
    ]
