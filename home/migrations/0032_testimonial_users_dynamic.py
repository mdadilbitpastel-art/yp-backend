"""Convert TestimonialsSection from 3 fixed user fields to a dynamic
related TestimonialUser table. Existing per-user data is preserved.

Order of operations matters:
  1. Create the TestimonialUser table.
  2. Copy any populated testimonial_{1,2,3}_* values into TestimonialUser rows.
  3. Drop the 9 legacy columns from TestimonialsSection.
"""

import django.db.models.deletion
import home.validators
from django.db import migrations, models


def _copy_testimonials_to_users(apps, schema_editor):
    TestimonialsSection = apps.get_model("home", "TestimonialsSection")
    TestimonialUser = apps.get_model("home", "TestimonialUser")

    for section in TestimonialsSection.objects.all():
        for position in range(1, 4):
            name = getattr(section, f"testimonial_{position}_name", "") or ""
            message = getattr(section, f"testimonial_{position}_message", "") or ""
            profile_image = getattr(section, f"testimonial_{position}_profile_image", None)

            if not (name or message or profile_image):
                continue

            TestimonialUser.objects.create(
                section=section,
                order=position,
                name=name,
                message=message,
                profile_image=profile_image or "",
            )


def _noop_reverse(apps, schema_editor):
    """The columns being repopulated were already dropped in this migration's
    forward — nothing to write back to."""


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0031_apply_companies"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestimonialUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("name", models.CharField(blank=True, max_length=120)),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home/testimonials/profiles/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("message", models.TextField(blank=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="users",
                        to="home.testimonialssection",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
        migrations.RunPython(_copy_testimonials_to_users, _noop_reverse),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_1_message"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_1_name"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_1_profile_image"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_2_message"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_2_name"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_2_profile_image"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_3_message"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_3_name"),
        migrations.RemoveField(model_name="testimonialssection", name="testimonial_3_profile_image"),
    ]
