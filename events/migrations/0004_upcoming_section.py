import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0003_featured_section_side_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventsUpcomingSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "verbose_name": "Events Upcoming Section",
                "verbose_name_plural": "Events Upcoming Section",
            },
        ),
        migrations.CreateModel(
            name="EventsUpcomingCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("name", models.CharField(blank=True, max_length=160)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="categories_entries",
                        to="events.eventsupcomingsection",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.CreateModel(
            name="EventsUpcomingCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="events/upcoming/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("meta_line", models.CharField(blank=True, max_length=160)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="card_entries",
                        to="events.eventsupcomingsection",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
