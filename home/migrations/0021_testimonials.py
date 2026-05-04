"""Create the Testimonials singleton section — background image + 3 users."""

import home.validators
from django.db import migrations, models


def _profile_field():
    return models.ImageField(
        blank=True,
        null=True,
        upload_to="home/testimonials/profiles/",
        validators=[
            home.validators.validate_image_size,
            home.validators.validate_image_extension,
        ],
    )


def _user_fields(i):
    return [
        (f"testimonial_{i}_name", models.CharField(blank=True, max_length=120)),
        (f"testimonial_{i}_profile_image", _profile_field()),
        (f"testimonial_{i}_message", models.TextField(blank=True)),
    ]


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0020_social_media"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestimonialsSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "background_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home/testimonials/backgrounds/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                *_user_fields(1),
                *_user_fields(2),
                *_user_fields(3),
            ],
            options={
                "verbose_name": "Testimonials Section",
                "verbose_name_plural": "Testimonials Section",
            },
        ),
    ]
