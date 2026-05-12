from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0008_review_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnersFounderSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("primary_button_text", models.CharField(blank=True, max_length=80)),
                ("primary_button_url", models.URLField(blank=True)),
                ("secondary_button_text", models.CharField(blank=True, max_length=80)),
                ("secondary_button_url", models.URLField(blank=True)),
            ],
            options={
                "verbose_name": "Partners Founder Section",
                "verbose_name_plural": "Partners Founder Section",
            },
        ),
    ]
