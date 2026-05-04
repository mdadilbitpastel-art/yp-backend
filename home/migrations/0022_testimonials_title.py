"""Add a title field to TestimonialsSection."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0021_testimonials"),
    ]

    operations = [
        migrations.AddField(
            model_name="testimonialssection",
            name="title",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
