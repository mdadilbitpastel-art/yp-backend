import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_management", "0002_migrate_network_stats"),
    ]

    operations = [
        migrations.CreateModel(
            name="Employer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="data/employers/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension])),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Employer",
                "verbose_name_plural": "Employers",
                "ordering": ("order", "id"),
            },
        ),
    ]
