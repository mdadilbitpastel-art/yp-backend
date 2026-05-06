"""
Home page CMS models.

Each homepage section lives in its own singleton table — Hero, Feature,
About, Network, TalentPool, Apply. The custom dashboard exposes one edit
page per section, each backed by its own model.
"""

from django.core.exceptions import ValidationError
from django.db import models

from .storage import video_storage
from .validators import (
    validate_image_extension,
    validate_image_size,
    validate_video_extension,
    validate_video_size,
)


TESTIMONIAL_USER_COUNT = 3
APP_BUTTON_COUNT = 3


class SingletonModel(models.Model):
    """Abstract base — enforces a single row (pk=1) for the concrete model."""

    SINGLETON_PK = 1

    class Meta:
        abstract = True

    def clean(self):
        if not self.pk and type(self).objects.exists():
            raise ValidationError(
                f"Only one {type(self).__name__} row is allowed."
            )

    def save(self, *args, **kwargs):
        self.pk = self.SINGLETON_PK
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Singleton must always exist — block deletion.
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=cls.SINGLETON_PK)
        return obj


class HeaderSettings(SingletonModel):
    """Site header — logo, single CTA button. Tabs are managed manually as
    related `HeaderTab` rows so editors control both the label and URL."""

    logo = models.ImageField(
        upload_to="header/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Header"
        verbose_name_plural = "Header"

    def __str__(self) -> str:
        return self.button_text or "Header"


class HeaderTab(models.Model):
    """A single navigation tab displayed in the site header."""

    header = models.ForeignKey(
        HeaderSettings,
        on_delete=models.CASCADE,
        related_name="tabs",
    )
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=80)
    url = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.label


class SocialMediaSection(SingletonModel):
    """Social Media homepage section — heading plus a dynamic list of cards."""

    heading = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Social Media Section"
        verbose_name_plural = "Social Media Section"

    def __str__(self) -> str:
        return self.heading or "Social Media Section"


class SocialMediaCard(models.Model):
    """A single social-media card — icon + name."""

    section = models.ForeignKey(
        SocialMediaSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=120)
    icon = models.ImageField(
        upload_to="home/social_media/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name


class TestimonialsSection(SingletonModel):
    """Testimonials homepage section — title, background image + 3 fixed users."""

    title = models.CharField(max_length=255, blank=True)
    background_image = models.ImageField(
        upload_to="home/testimonials/backgrounds/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    testimonial_1_name = models.CharField(max_length=120, blank=True)
    testimonial_1_profile_image = models.ImageField(
        upload_to="home/testimonials/profiles/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    testimonial_1_message = models.TextField(blank=True)

    testimonial_2_name = models.CharField(max_length=120, blank=True)
    testimonial_2_profile_image = models.ImageField(
        upload_to="home/testimonials/profiles/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    testimonial_2_message = models.TextField(blank=True)

    testimonial_3_name = models.CharField(max_length=120, blank=True)
    testimonial_3_profile_image = models.ImageField(
        upload_to="home/testimonials/profiles/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    testimonial_3_message = models.TextField(blank=True)

    class Meta:
        verbose_name = "Testimonials Section"
        verbose_name_plural = "Testimonials Section"

    def __str__(self) -> str:
        return self.title or "Testimonials Section"

    def testimonials(self) -> list[dict]:
        users = []
        for i in range(1, TESTIMONIAL_USER_COUNT + 1):
            profile = getattr(self, f"testimonial_{i}_profile_image")
            users.append(
                {
                    "position": i,
                    "name": getattr(self, f"testimonial_{i}_name"),
                    "profile_image": profile if profile else None,
                    "message": getattr(self, f"testimonial_{i}_message"),
                }
            )
        return users


class AppSection(SingletonModel):
    """App promotion section — title, description, 3 CTA buttons, side & barcode images."""

    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    button_1_text = models.CharField(max_length=80, blank=True)
    button_1_url = models.URLField(blank=True)
    button_2_text = models.CharField(max_length=80, blank=True)
    button_2_url = models.URLField(blank=True)
    button_3_text = models.CharField(max_length=80, blank=True)
    button_3_url = models.URLField(blank=True)

    side_image = models.ImageField(
        upload_to="home/app/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    barcode_image = models.ImageField(
        upload_to="home/app/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "App Section"
        verbose_name_plural = "App Section"

    def __str__(self) -> str:
        return self.title or "App Section"

    def buttons(self) -> list[dict]:
        return [
            {
                "position": i,
                "text": getattr(self, f"button_{i}_text"),
                "url": getattr(self, f"button_{i}_url"),
            }
            for i in range(1, APP_BUTTON_COUNT + 1)
        ]


class FooterSettings(SingletonModel):
    """Site-wide footer — logo, contact details, copyright. Text links live
    on a related `FooterLink` model so they can be added one at a time."""

    logo = models.ImageField(
        upload_to="footer/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    copyright_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def __str__(self) -> str:
        return self.title or "Footer"


class FooterLink(models.Model):
    """A single text link in the footer."""

    footer = models.ForeignKey(
        FooterSettings,
        on_delete=models.CASCADE,
        related_name="links",
    )
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=120)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.label


class HeroSection(SingletonModel):
    """Hero / banner section."""

    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    highlight_text = models.CharField(
        max_length=160,
        blank=True,
        help_text='Inline highlight, e.g. "600,000 students".',
    )

    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.URLField(blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.URLField(blank=True)

    background_image = models.ImageField(
        upload_to="home/hero/backgrounds/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    hero_image = models.ImageField(
        upload_to="home/hero/foreground/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self) -> str:
        return self.title or "Hero Section"


class FeatureSection(SingletonModel):
    """Feature highlights — heading + a manual list of cards managed via
    the related `FeatureCard` model."""

    features_title = models.CharField(max_length=255, blank=True)
    features_description = models.TextField(blank=True)
    features_button_text = models.CharField(
        max_length=80,
        blank=True,
        help_text="Shared button label used on every feature card.",
    )

    class Meta:
        verbose_name = "Feature Section"
        verbose_name_plural = "Feature Section"

    def __str__(self) -> str:
        return self.features_title or "Feature Section"

    def feature_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "title": card.title,
                "icon": card.icon if card.icon else None,
                "button_url": card.button_url,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class FeatureCard(models.Model):
    """A single feature highlight card — title, icon image, and CTA URL."""

    section = models.ForeignKey(
        FeatureSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255, blank=True)
    icon = models.ImageField(
        upload_to="home/features/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    button_url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Feature Card {self.pk}"


class AboutSection(SingletonModel):
    """About / Mission section."""

    about_section_label = models.CharField(max_length=120, blank=True)
    about_section_title = models.CharField(max_length=255, blank=True)
    about_section_description = models.TextField(blank=True)

    about_section_primary_button_text = models.CharField(max_length=80, blank=True)
    about_section_primary_button_url = models.URLField(blank=True)
    about_section_secondary_button_text = models.CharField(max_length=80, blank=True)
    about_section_secondary_button_url = models.URLField(blank=True)

    about_section_image = models.ImageField(
        upload_to="home/about/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self) -> str:
        return self.about_section_title or "About Section"


class NetworkSection(SingletonModel):
    """Stats / Network section — heading, optional video, plus a manual list
    of stats managed via the related `NetworkStat` model."""

    network_section_title = models.CharField(max_length=255, blank=True)
    network_section_video = models.FileField(
        upload_to="home/network/",
        storage=video_storage,
        validators=[validate_video_size, validate_video_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Network Section"
        verbose_name_plural = "Network Section"

    def __str__(self) -> str:
        return self.network_section_title or "Network Section"

    def network_stats(self) -> list[dict]:
        return [
            {
                "position": index,
                "value": stat.value,
                "label": stat.label,
            }
            for index, stat in enumerate(self.stats.all(), start=1)
        ]


class NetworkStat(models.Model):
    """A single stat shown in the Network section — value + label."""

    section = models.ForeignKey(
        NetworkSection,
        on_delete=models.CASCADE,
        related_name="stats",
    )
    order = models.PositiveIntegerField(default=0)
    value = models.CharField(max_length=80, blank=True)
    label = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return f"{self.value} {self.label}".strip() or f"Network Stat {self.pk}"


class TalentPoolSection(SingletonModel):
    """Talent Pool section."""

    talent_pool_section_title = models.CharField(max_length=255, blank=True)
    talent_pool_section_subtitle = models.CharField(max_length=255, blank=True)
    talent_pool_section_description = models.TextField(blank=True)

    talent_pool_section_primary_button_text = models.CharField(max_length=80, blank=True)
    talent_pool_section_primary_button_url = models.URLField(blank=True)
    talent_pool_section_secondary_button_text = models.CharField(max_length=80, blank=True)
    talent_pool_section_secondary_button_url = models.URLField(blank=True)

    talent_pool_section_image = models.ImageField(
        upload_to="home/talent_pool/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Talent Pool Section"
        verbose_name_plural = "Talent Pool Section"

    def __str__(self) -> str:
        return self.talent_pool_section_title or "Talent Pool Section"


class ApplySection(SingletonModel):
    """Apply section — heading + sub-heading + a manual list of company
    cards managed via the related `ApplyCompany` model + a bottom button."""

    apply_section_title = models.CharField(max_length=255, blank=True)
    apply_section_subtitle = models.CharField(max_length=255, blank=True)
    apply_section_bottom_button_text = models.CharField(max_length=80, blank=True)
    apply_section_bottom_button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Apply Section"
        verbose_name_plural = "Apply Section"

    def __str__(self) -> str:
        return self.apply_section_title or "Apply Section"

    def apply_companies(self) -> list[dict]:
        return [
            {
                "position": index,
                "label": company.label,
                "title": company.title,
                "description": company.description,
                "button_text": company.button_text,
                "button_url": company.button_url,
                "large_image": company.large_image if company.large_image else None,
                "small_image": company.small_image if company.small_image else None,
            }
            for index, company in enumerate(self.companies.all(), start=1)
        ]


class ApplyCompany(models.Model):
    """A single company card shown in the Apply section."""

    section = models.ForeignKey(
        ApplySection,
        on_delete=models.CASCADE,
        related_name="companies",
    )
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)
    large_image = models.ImageField(
        upload_to="home/apply/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    small_image = models.ImageField(
        upload_to="home/apply/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or self.label or f"Apply Company {self.pk}"
