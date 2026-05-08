"""
Employers page CMS models.

Each Employers section lives in its own singleton table — added one at a
time as the page grows. Reuses `home.models.SingletonModel` as the
abstract base so all sections share the same single-row guarantee +
`load()` helper.
"""

from django.db import models

from home.models import SingletonModel
from home.validators import validate_image_extension, validate_image_size


class EmployersHeroSection(SingletonModel):
    """Employers — top hero / banner section. Label, title, description,
    two CTA buttons, and a side image."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.URLField(blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.URLField(blank=True)

    side_image = models.ImageField(
        upload_to="employers/hero/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Employers Hero Section"
        verbose_name_plural = "Employers Hero Section"

    def __str__(self) -> str:
        return self.title or "Employers Hero Section"


class EmployersMissionSection(SingletonModel):
    """Employers — mission section. Label, title, description, single CTA
    button, side image, plus a dynamic list of points managed via the
    related `EmployersMissionPoint` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    side_image = models.ImageField(
        upload_to="employers/mission/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Employers Mission Section"
        verbose_name_plural = "Employers Mission Section"

    def __str__(self) -> str:
        return self.title or "Employers Mission Section"

    def mission_points(self) -> list[dict]:
        return [
            {"position": index, "text": point.text}
            for index, point in enumerate(self.points.all(), start=1)
        ]


class EmployersMissionPoint(models.Model):
    """A single bullet point shown in the Employers mission section."""

    section = models.ForeignKey(
        EmployersMissionSection,
        on_delete=models.CASCADE,
        related_name="points",
    )
    order = models.PositiveIntegerField(default=0)
    text = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.text or f"Mission Point {self.pk}"


class EmployersOfferSection(SingletonModel):
    """Employers — offer section. Label, title, description, plus a
    dynamic list of offer cards (icon + title + description) managed via
    the related `EmployersOfferCard` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Employers Offer Section"
        verbose_name_plural = "Employers Offer Section"

    def __str__(self) -> str:
        return self.title or "Employers Offer Section"

    def offer_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "icon": card.icon if card.icon else None,
                "title": card.title,
                "description": card.description,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class EmployersOfferCard(models.Model):
    """A single offer card — icon + title + description."""

    section = models.ForeignKey(
        EmployersOfferSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    icon = models.ImageField(
        upload_to="employers/offers/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Offer Card {self.pk}"


class EmployersEventsSection(SingletonModel):
    """Employers — events section. Label, title, description, single CTA
    button, plus a dynamic list of event images managed via the related
    `EmployersEventImage` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Employers Events Section"
        verbose_name_plural = "Employers Events Section"

    def __str__(self) -> str:
        return self.title or "Employers Events Section"

    def event_images(self) -> list[dict]:
        return [
            {
                "position": index,
                "image": image.image if image.image else None,
            }
            for index, image in enumerate(self.images.all(), start=1)
        ]


class EmployersEventImage(models.Model):
    """A single event image — just an image upload."""

    section = models.ForeignKey(
        EmployersEventsSection,
        on_delete=models.CASCADE,
        related_name="images",
    )
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="employers/events/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return f"Event Image {self.pk}"
