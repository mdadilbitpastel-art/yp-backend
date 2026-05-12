"""
Events page CMS models.

Each Events section lives in its own singleton table — added one at a
time as the page grows. Reuses `home.models.SingletonModel` as the
abstract base so all sections share the same single-row guarantee +
`load()` helper.
"""

from django.db import models

from home.models import SingletonModel
from home.storage import video_storage
from home.validators import (
    validate_image_extension,
    validate_image_size,
    validate_video_extension,
    validate_video_size,
)


class EventsHeroSection(SingletonModel):
    """Events — top hero / banner section. Label, title, description,
    plus two CTA buttons (text + URL)."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.URLField(blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Events Hero Section"
        verbose_name_plural = "Events Hero Section"

    def __str__(self) -> str:
        return self.title or "Events Hero Section"


class EventsFeaturedSection(SingletonModel):
    """Events — featured section. Label, a free-form date/time label
    (e.g. "Fri 15 May - 10:00 - 16:00 BST"), title, description, a
    category label, and a single CTA button (text + URL)."""

    label = models.CharField(max_length=120, blank=True)
    datetime_label = models.CharField(max_length=160, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    category_label = models.CharField(max_length=120, blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Events Featured Section"
        verbose_name_plural = "Events Featured Section"

    def __str__(self) -> str:
        return self.title or "Events Featured Section"


class EventsUpcomingSection(SingletonModel):
    """Events — upcoming section. Label, title, a shared card button
    label, plus a manual list of category labels
    (`EventsUpcomingCategory`) and a manual list of event cards
    (`EventsUpcomingCard`)."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    card_button_text = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = "Events Upcoming Section"
        verbose_name_plural = "Events Upcoming Section"

    def __str__(self) -> str:
        return self.title or "Events Upcoming Section"

    def categories(self) -> list[dict]:
        return [
            {"position": index, "name": category.name}
            for index, category in enumerate(self.categories_entries.all(), start=1)
        ]

    def cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "image": card.image if card.image else None,
                "label": card.label,
                "title": card.title,
                "description": card.description,
                "years_label": card.years_label,
                "price_label": card.price_label,
                "button_url": card.button_url,
            }
            for index, card in enumerate(self.card_entries.all(), start=1)
        ]


class EventsUpcomingCategory(models.Model):
    """A single category label shown in the Events upcoming section."""

    section = models.ForeignKey(
        EventsUpcomingSection,
        on_delete=models.CASCADE,
        related_name="categories_entries",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Category {self.pk}"


class EventsUpcomingCard(models.Model):
    """A single event card shown in the Events upcoming section.

    The card footer is split into `years_label` (age range, e.g.
    "Years 12+") and `price_label` (cost, e.g. "Free")."""

    section = models.ForeignKey(
        EventsUpcomingSection,
        on_delete=models.CASCADE,
        related_name="card_entries",
    )
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="events/upcoming/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    years_label = models.CharField(max_length=80, blank=True)
    price_label = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Upcoming Card {self.pk}"


class EventsMissedSection(SingletonModel):
    """Events — missed section. Label, title, description, a shared card
    button label, plus a manual list of missed event cards (video, title,
    date label, button URL)."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    card_button_text = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = "Events Missed Section"
        verbose_name_plural = "Events Missed Section"

    def __str__(self) -> str:
        return self.title or "Events Missed Section"

    def cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "video": card.video if card.video else None,
                "title": card.title,
                "date_label": card.date_label,
                "button_url": card.button_url,
            }
            for index, card in enumerate(self.card_entries.all(), start=1)
        ]


class EventsMissedCard(models.Model):
    """A single missed event card — video + title + a free-form date
    label (e.g. "AUG 2025") + a per-card button URL.

    The button text is shared across all cards via
    `EventsMissedSection.card_button_text`."""

    section = models.ForeignKey(
        EventsMissedSection,
        on_delete=models.CASCADE,
        related_name="card_entries",
    )
    order = models.PositiveIntegerField(default=0)
    video = models.FileField(
        upload_to="events/missed/",
        storage=video_storage,
        validators=[validate_video_size, validate_video_extension],
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=255, blank=True)
    date_label = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Missed Card {self.pk}"


class EventsSubmitSection(SingletonModel):
    """Events — submit events section. Label, title, description, and a
    single CTA button (text + URL). Images live on `SectionImage`."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Events Submit Section"
        verbose_name_plural = "Events Submit Section"

    def __str__(self) -> str:
        return self.title or "Events Submit Section"
