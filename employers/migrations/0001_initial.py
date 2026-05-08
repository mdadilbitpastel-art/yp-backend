import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="EmployersHeroSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("primary_button_text", models.CharField(blank=True, max_length=80)),
                ("primary_button_url", models.URLField(blank=True)),
                ("secondary_button_text", models.CharField(blank=True, max_length=80)),
                ("secondary_button_url", models.URLField(blank=True)),
                ("side_image", models.ImageField(blank=True, null=True, upload_to="employers/hero/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension])),
            ],
            options={
                "verbose_name": "Employers Hero Section",
                "verbose_name_plural": "Employers Hero Section",
            },
        ),
    ]
