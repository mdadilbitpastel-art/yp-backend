import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0007_missed_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventsSubmitSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
                (
                    "side_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="events/submit/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
            ],
            options={
                "verbose_name": "Events Submit Section",
                "verbose_name_plural": "Events Submit Section",
            },
        ),
    ]
