import home.storage
import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0006_share_card_button_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventsMissedSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("card_button_text", models.CharField(blank=True, max_length=80)),
            ],
            options={
                "verbose_name": "Events Missed Section",
                "verbose_name_plural": "Events Missed Section",
            },
        ),
        migrations.CreateModel(
            name="EventsMissedCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        null=True,
                        storage=home.storage.video_storage,
                        upload_to="events/missed/",
                        validators=[
                            home.validators.validate_video_size,
                            home.validators.validate_video_extension,
                        ],
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255)),
                ("date_label", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="card_entries",
                        to="events.eventsmissedsection",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
