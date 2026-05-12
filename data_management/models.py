"""
Shared dynamic data — `Statistic`, `Employer`, and `SectionImage`.

Consumer sections (`home.NetworkSection`, `about_us.AboutUsMissionSection`,
`partners.PartnersHeroSection`, `schools.SchoolsEmployerSection`, …) each
pick which `Statistic` / `Employer` rows they want via their own M2M, so
the same row can appear on one page, multiple pages, or none.

`SectionImage` is a generic-FK image row that any singleton section can
own a list of — used by every section's dashboard "Images" card so admins
can upload image-1, image-2, … instead of fighting with single fixed
`background_image` / `hero_image` / `side_image` slots.
"""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from home.validators import validate_image_extension, validate_image_size


class Statistic(models.Model):
    """A reusable stat — value + label, ordered globally."""

    value = models.CharField(max_length=80)
    label = models.CharField(max_length=160)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Statistic"
        verbose_name_plural = "Statistics"

    def __str__(self) -> str:
        return f"{self.value} {self.label}".strip() or f"Statistic {self.pk}"


class Employer(models.Model):
    """A reusable employer entry — name, logo, description, URL,
    ordered globally."""

    name = models.CharField(max_length=160)
    logo = models.ImageField(
        upload_to="data/employers/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Employer"
        verbose_name_plural = "Employers"

    def __str__(self) -> str:
        return self.name or f"Employer {self.pk}"


class SocialMediaIcon(models.Model):
    """A reusable social-media entry — name + icon, ordered globally.

    Consumer sections (`home.SocialMediaSection`,
    `about_us.AboutUsSocialMediaSection`) each pick which icons to show
    via their own M2M `selected_social_media`."""

    name = models.CharField(max_length=120)
    icon = models.ImageField(
        upload_to="data/social_media/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Social Media Icon"
        verbose_name_plural = "Social Media Icons"

    def __str__(self) -> str:
        return self.name or f"Social Media Icon {self.pk}"


class TeamMember(models.Model):
    """A reusable team member entry — name, profile image, designation,
    email URL, view-profile link. Ordered globally.

    Consumer sections (`about_us.AboutUsTeamSection`) pick which members
    to show via their own M2M `selected_team_members`."""

    name = models.CharField(max_length=160)
    profile_image = models.ImageField(
        upload_to="data/team/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    designation = models.CharField(max_length=160, blank=True)
    email_url = models.CharField(
        max_length=255,
        blank=True,
        help_text='Use a mailto: link, e.g. "mailto:name@example.com".',
    )
    view_profile_text = models.CharField(max_length=80, blank=True)
    view_profile_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "id")
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self) -> str:
        return self.name or f"Team Member {self.pk}"


class SectionImage(models.Model):
    """An image attached to any singleton section via a generic FK.

    Used by every section's "Images" card on the dashboard, so admins
    upload `image-1`, `image-2`, … rather than fighting with hard-coded
    `side_image` / `background_image` / `hero_image` slots."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    section = GenericForeignKey("content_type", "object_id")

    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="sections/images/",
        validators=[validate_image_size, validate_image_extension],
    )

    class Meta:
        ordering = ("order", "id")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

    def __str__(self) -> str:
        return f"SectionImage #{self.pk}"


def section_images(section) -> list[dict]:
    """Helper used by serializers — return the section's images as a
    list of `{"position", "image"}` dicts ordered by `order`."""
    ct = ContentType.objects.get_for_model(type(section))
    return [
        {"position": index, "image": row.image}
        for index, row in enumerate(
            SectionImage.objects.filter(content_type=ct, object_id=section.pk),
            start=1,
        )
    ]
