"""
About Us page CMS models.

Each About Us section lives in its own singleton table — added one at a
time as the page grows. Reuses `home.models.SingletonModel` as the abstract
base so all sections share the same single-row guarantee + `load()` helper.
"""

from django.db import models

from home.models import SingletonModel
from home.validators import validate_image_extension, validate_image_size


class AboutUsHeroSection(SingletonModel):
    """About Us — top hero / banner section."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "About Us Hero Section"
        verbose_name_plural = "About Us Hero Section"

    def __str__(self) -> str:
        return self.title or "About Us Hero Section"


class AboutUsMissionSection(SingletonModel):
    """About Us — mission section. Label, title, description, side image,
    plus the statistics chosen for this section from
    `data_management.Statistic`. The selection is independent of the home
    Network section's selection."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    selected_statistics = models.ManyToManyField(
        "data_management.Statistic",
        blank=True,
        related_name="mission_sections",
    )

    class Meta:
        verbose_name = "About Us Mission Section"
        verbose_name_plural = "About Us Mission Section"

    def __str__(self) -> str:
        return self.title or "About Us Mission Section"

    def mission_stats(self) -> list[dict]:
        return [
            {
                "position": index,
                "value": stat.value,
                "label": stat.label,
            }
            for index, stat in enumerate(self.selected_statistics.all(), start=1)
        ]


class AboutUsValuesSection(SingletonModel):
    """About Us — values section. Label, title, subtitle, plus a dynamic
    list of value cards managed via the related `AboutUsValueCard` model
    (icon, label, note)."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "About Us Values Section"
        verbose_name_plural = "About Us Values Section"

    def __str__(self) -> str:
        return self.title or "About Us Values Section"

    def value_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "icon": card.icon if card.icon else None,
                "label": card.label,
                "note": card.note,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class AboutUsValueCard(models.Model):
    """A single value card — icon, label, note."""

    section = models.ForeignKey(
        AboutUsValuesSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    icon = models.ImageField(
        upload_to="about_us/values/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    label = models.CharField(max_length=160, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.label or f"Value Card {self.pk}"


class AboutUsSocialMediaSection(SingletonModel):
    """About Us — social media section. Holds the About Us page's own
    heading/label/sub-title (independent of the home page), plus the
    social-media icons chosen for this section from
    `data_management.SocialMediaIcon`."""

    label = models.CharField(max_length=120, blank=True)
    heading = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    selected_social_media = models.ManyToManyField(
        "data_management.SocialMediaIcon",
        blank=True,
        related_name="about_us_social_media_sections",
    )

    class Meta:
        verbose_name = "About Us Social Media Section"
        verbose_name_plural = "About Us Social Media Section"

    def __str__(self) -> str:
        return self.heading or "About Us Social Media Section"

    def social_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "name": entry.name,
                "icon": entry.icon if entry.icon else None,
            }
            for index, entry in enumerate(self.selected_social_media.all(), start=1)
        ]


class AboutUsCommunitySection(SingletonModel):
    """About Us — community section. Label, title, subtitle, plus a dynamic
    list of community cards (image + name + description + button) managed
    via the related `AboutUsCommunityCard` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "About Us Community Section"
        verbose_name_plural = "About Us Community Section"

    def __str__(self) -> str:
        return self.title or "About Us Community Section"

    def community_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "image": card.image if card.image else None,
                "name": card.name,
                "description": card.description,
                "button_text": card.button_text,
                "button_url": card.button_url,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class AboutUsCommunityCard(models.Model):
    """A single community card — image, name, description, CTA button."""

    section = models.ForeignKey(
        AboutUsCommunitySection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="about_us/community/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Community Card {self.pk}"


class AboutUsTeamSection(SingletonModel):
    """About Us — team section. Label, title, subtitle, plus a dynamic
    list of member cards managed via the related `AboutUsTeamMember` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "About Us Team Section"
        verbose_name_plural = "About Us Team Section"

    def __str__(self) -> str:
        return self.title or "About Us Team Section"

    def team_members(self) -> list[dict]:
        return [
            {
                "position": index,
                "profile_image": member.profile_image if member.profile_image else None,
                "name": member.name,
                "designation": member.designation,
                "email_icon": member.email_icon if member.email_icon else None,
                "email_url": member.email_url,
                "view_profile_text": member.view_profile_text,
                "view_profile_url": member.view_profile_url,
            }
            for index, member in enumerate(self.members.all(), start=1)
        ]


class AboutUsTeamMember(models.Model):
    """A single team member card."""

    section = models.ForeignKey(
        AboutUsTeamSection,
        on_delete=models.CASCADE,
        related_name="members",
    )
    order = models.PositiveIntegerField(default=0)
    profile_image = models.ImageField(
        upload_to="about_us/team/profiles/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=160, blank=True)
    designation = models.CharField(max_length=160, blank=True)
    email_icon = models.ImageField(
        upload_to="about_us/team/icons/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    email_url = models.CharField(
        max_length=255,
        blank=True,
        help_text='Use a mailto: link, e.g. "mailto:name@example.com".',
    )
    view_profile_text = models.CharField(max_length=80, blank=True)
    view_profile_url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Team Member {self.pk}"


class AboutUsPledgeSection(SingletonModel):
    """About Us — pledge section. Label, title, description, side image."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name = "About Us Pledge Section"
        verbose_name_plural = "About Us Pledge Section"

    def __str__(self) -> str:
        return self.title or "About Us Pledge Section"


class AboutUsJourneySection(SingletonModel):
    """About Us — journey section. Label, title, subtitle, plus a dynamic
    list of journey cards (image + title + description) managed via the
    related `AboutUsJourneyCard` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "About Us Journey Section"
        verbose_name_plural = "About Us Journey Section"

    def __str__(self) -> str:
        return self.title or "About Us Journey Section"

    def journey_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "image": card.image if card.image else None,
                "title": card.title,
                "description": card.description,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class AboutUsJourneyCard(models.Model):
    """A single journey card — image, title, description."""

    section = models.ForeignKey(
        AboutUsJourneySection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="about_us/journey/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Journey Card {self.pk}"


class AboutUsFounderSection(SingletonModel):
    """About Us — founder section. Label, founder name, designation,
    description, founder message, single CTA button, and a side image."""

    label = models.CharField(max_length=120, blank=True)
    founder_name = models.CharField(max_length=160, blank=True)
    designation = models.CharField(max_length=160, blank=True)
    description = models.TextField(blank=True)
    founder_message = models.TextField(blank=True)

    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "About Us Founder Section"
        verbose_name_plural = "About Us Founder Section"

    def __str__(self) -> str:
        return self.founder_name or "About Us Founder Section"
