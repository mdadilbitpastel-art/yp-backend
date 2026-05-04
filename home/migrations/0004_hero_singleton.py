"""Make HeroSection a singleton: title becomes optional, images nullable."""

import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_herosection"),
    ]

    operations = [
        migrations.AlterField(
            model_name="herosection",
            name="title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="herosection",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="herosection",
            name="background_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="home/hero/backgrounds/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="herosection",
            name="hero_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="home/hero/foreground/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
        migrations.AlterModelOptions(
            name="herosection",
            options={
                "verbose_name": "Hero Section",
                "verbose_name_plural": "Hero Section",
            },
        ),
    ]
