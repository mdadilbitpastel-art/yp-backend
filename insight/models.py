"""
Insight page CMS models.

Each Insight section lives in its own singleton table — added one at a
time as the page grows. Reuses `home.models.SingletonModel` as the
abstract base so all sections share the same single-row guarantee +
`load()` helper.
"""

from django.db import models

from home.models import SingletonModel
from home.validators import validate_image_extension, validate_image_size


class InsightHeroSection(SingletonModel):
    """Insight — top hero / banner section. Label, title, description,
    plus a search placeholder."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    search_placeholder = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = "Insight Hero Section"
        verbose_name_plural = "Insight Hero Section"

    def __str__(self) -> str:
        return self.title or "Insight Hero Section"


class InsightFounderSection(SingletonModel):
    """Insight — founder section. A dynamic list of category labels, two
    independent labels (label-1 / label-2), a free-form date label
    (e.g. "14 APR 2026"), title, description, a free-form meta-data line
    (e.g. "By metro - 4 min read"), a single CTA button (text + URL).
    Images live on `data_management.SectionImage`."""

    label_1 = models.CharField(max_length=120, blank=True)
    label_2 = models.CharField(max_length=120, blank=True)
    date_label = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    meta_data = models.CharField(max_length=160, blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Insight Founder Section"
        verbose_name_plural = "Insight Founder Section"

    def __str__(self) -> str:
        return self.title or "Insight Founder Section"

    def categories(self) -> list[dict]:
        return [
            {"position": index, "name": category.name}
            for index, category in enumerate(self.category_entries.all(), start=1)
        ]


class InsightFounderCategory(models.Model):
    """A single category label shown in the Insight founder section."""

    section = models.ForeignKey(
        InsightFounderSection,
        on_delete=models.CASCADE,
        related_name="category_entries",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Category {self.pk}"


class InsightArticleSection(SingletonModel):
    """Insight — article section. Title plus a shared card button label;
    cards live on the related `InsightArticleCard` model."""

    title = models.CharField(max_length=255, blank=True)
    card_button_text = models.CharField(max_length=80, blank=True)

    class Meta:
        verbose_name = "Insight Article Section"
        verbose_name_plural = "Insight Article Section"

    def __str__(self) -> str:
        return self.title or "Insight Article Section"

    def cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "label": card.label,
                "image": card.image if card.image else None,
                "date_label": card.date_label,
                "title": card.title,
                "description": card.description,
                "tag": card.tag,
                "button_url": card.button_url,
            }
            for index, card in enumerate(self.card_entries.all(), start=1)
        ]


class InsightLaneSection(SingletonModel):
    """Insight — "Pick your lane" section. Label + title; lanes live on
    the related `InsightLane` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Insight Lane Section"
        verbose_name_plural = "Insight Lane Section"

    def __str__(self) -> str:
        return self.title or "Insight Lane Section"

    def lanes(self) -> list[dict]:
        return [
            {
                "position": index,
                "name": lane.name,
                "article_count": lane.article_count,
                "url": lane.url,
            }
            for index, lane in enumerate(self.lane_entries.all(), start=1)
        ]


class InsightLane(models.Model):
    """A single lane shown in the Insight "Pick your lane" section —
    name + article count + URL."""

    section = models.ForeignKey(
        InsightLaneSection,
        on_delete=models.CASCADE,
        related_name="lane_entries",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=160, blank=True)
    article_count = models.PositiveIntegerField(default=0)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Lane {self.pk}"


class InsightSubscribeSection(SingletonModel):
    """Insight — subscribe section. Label, title, description, an email
    input placeholder, a subscribe CTA button (text + URL), and a small
    bottom note. Images live on `data_management.SectionImage`."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    email_placeholder = models.CharField(max_length=120, blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)
    bottom_note = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Insight Subscribe Section"
        verbose_name_plural = "Insight Subscribe Section"

    def __str__(self) -> str:
        return self.title or "Insight Subscribe Section"


class InsightArticleCard(models.Model):
    """A single article card shown in the Insight article section.

    The card button text is shared across all cards via
    `InsightArticleSection.card_button_text`."""

    section = models.ForeignKey(
        InsightArticleSection,
        on_delete=models.CASCADE,
        related_name="card_entries",
    )
    order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=120, blank=True)
    image = models.ImageField(
        upload_to="insight/articles/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )
    date_label = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    tag = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Article Card {self.pk}"
