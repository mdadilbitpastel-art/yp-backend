import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employers", "0003_mission_button_and_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployersOfferSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Employers Offer Section",
                "verbose_name_plural": "Employers Offer Section",
            },
        ),
        migrations.CreateModel(
            name="EmployersOfferCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("icon", models.ImageField(blank=True, null=True, upload_to="employers/offers/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension])),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="cards", to="employers.employersoffersection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
