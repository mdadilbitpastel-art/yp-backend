"""Add the About / Mission section fields to the HeroSection singleton row."""

import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0006_feature_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="about_section_label",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_primary_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_primary_button_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_secondary_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_secondary_button_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="home/about/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name="about_section_is_active",
            field=models.BooleanField(default=True),
        ),
    ]
