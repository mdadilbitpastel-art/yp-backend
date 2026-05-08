import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0002_help_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolsEmployerSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
            ],
            options={
                "verbose_name": "Schools Employer Section",
                "verbose_name_plural": "Schools Employer Section",
            },
        ),
        migrations.CreateModel(
            name="SchoolsEmployer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="schools/employers/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension])),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="entries", to="schools.schoolsemployersection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
