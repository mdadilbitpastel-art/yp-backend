import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employers", "0004_offer_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployersEventsSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
            ],
            options={
                "verbose_name": "Employers Events Section",
                "verbose_name_plural": "Employers Events Section",
            },
        ),
        migrations.CreateModel(
            name="EmployersEventImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("image", models.ImageField(blank=True, null=True, upload_to="employers/events/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension])),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="images", to="employers.employerseventssection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
