import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_management", "0006_section_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="SocialMediaIcon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="data/social_media/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Social Media Icon",
                "verbose_name_plural": "Social Media Icons",
                "ordering": ("order", "id"),
            },
        ),
    ]
