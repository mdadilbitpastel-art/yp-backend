"""Add the `selected_social_media` M2M to AboutUsSocialMediaSection and
pre-select every existing `SocialMediaIcon` so the About Us page keeps
showing the same icons it did before (previously About Us shared all
cards with Home → Social Media)."""

from django.db import migrations, models


def preselect_all_icons(apps, schema_editor):
    AboutUsSocialMediaSection = apps.get_model(
        "about_us", "AboutUsSocialMediaSection"
    )
    SocialMediaIcon = apps.get_model("data_management", "SocialMediaIcon")

    section = AboutUsSocialMediaSection.objects.first()
    if section is None:
        return
    icon_ids = list(SocialMediaIcon.objects.values_list("pk", flat=True))
    if icon_ids:
        section.selected_social_media.set(icon_ids)


def noop_reverse(apps, schema_editor):
    """Reverse: leave the M2M membership intact (the table itself is
    dropped by the reverse of AddField)."""


class Migration(migrations.Migration):

    dependencies = [
        ("about_us", "0013_section_images"),
        ("data_management", "0007_social_media_icon"),
        ("home", "0038_social_media_m2m"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutussocialmediasection",
            name="selected_social_media",
            field=models.ManyToManyField(
                blank=True,
                related_name="about_us_social_media_sections",
                to="data_management.socialmediaicon",
            ),
        ),
        migrations.RunPython(preselect_all_icons, noop_reverse),
    ]
