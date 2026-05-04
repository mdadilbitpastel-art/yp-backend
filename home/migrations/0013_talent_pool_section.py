"""Add the Talent Pool section fields to the HeroSection singleton row."""

import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0012_network_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_subtitle",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_primary_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_primary_button_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_secondary_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_secondary_button_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="talent_pool_section_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="home/talent_pool/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
    ]
