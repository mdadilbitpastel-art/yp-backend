"""Migrate `home.SocialMediaCard` rows into `data_management.SocialMediaIcon`
and link the home Social Media singleton to all of them. Drops the old
SocialMediaCard model afterwards. About Us picks up the same icons via
its own migration."""

from django.db import migrations, models


def copy_cards_to_icons(apps, schema_editor):
    SocialMediaCard = apps.get_model("home", "SocialMediaCard")
    SocialMediaSection = apps.get_model("home", "SocialMediaSection")
    SocialMediaIcon = apps.get_model("data_management", "SocialMediaIcon")

    legacy = list(SocialMediaCard.objects.order_by("order", "id"))
    if not legacy:
        return

    new_ids = []
    for card in legacy:
        new_icon = SocialMediaIcon.objects.create(
            name=card.name or "",
            icon=card.icon if card.icon else None,
            order=card.order,
        )
        new_ids.append(new_icon.pk)

    section = SocialMediaSection.objects.first()
    if section is not None:
        section.selected_social_media.set(new_ids)


def noop_reverse(apps, schema_editor):
    """Reverse: leave the new SocialMediaIcon rows in place."""


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0037_section_images"),
        ("data_management", "0007_social_media_icon"),
    ]

    operations = [
        migrations.AddField(
            model_name="socialmediasection",
            name="selected_social_media",
            field=models.ManyToManyField(
                blank=True,
                related_name="home_social_media_sections",
                to="data_management.socialmediaicon",
            ),
        ),
        migrations.RunPython(copy_cards_to_icons, noop_reverse),
        migrations.DeleteModel(name="SocialMediaCard"),
    ]
