"""Add the Apply section fields to the HeroSection singleton row."""

import home.validators
from django.db import migrations, models


def _company_field_ops(i: int):
    return [
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_label",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_button_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_large_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="home/apply/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
        migrations.AddField(
            model_name="herosection",
            name=f"apply_company_{i}_small_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="home/apply/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
    ]


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0013_talent_pool_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="apply_section_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name="apply_section_subtitle",
            field=models.CharField(blank=True, max_length=255),
        ),
        *_company_field_ops(1),
        *_company_field_ops(2),
        *_company_field_ops(3),
    ]
