from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventsFeaturedSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("datetime_label", models.CharField(blank=True, max_length=160)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("category_label", models.CharField(blank=True, max_length=120)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
            ],
            options={
                "verbose_name": "Events Featured Section",
                "verbose_name_plural": "Events Featured Section",
            },
        ),
    ]
