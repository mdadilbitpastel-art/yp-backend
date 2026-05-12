"""
Partners page CMS models.

Each Partners section lives in its own singleton table — added one at a
time as the page grows. Reuses `home.models.SingletonModel` as the
abstract base so all sections share the same single-row guarantee +
`load()` helper.
"""

from django.db import models

from home.models import SingletonModel
from home.validators import validate_image_extension, validate_image_size


class PartnersHeroSection(SingletonModel):
    """Partners — top hero / banner section. Label, title, description,
    plus the statistics chosen for this section from
    `data_management.Statistic`."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    selected_statistics = models.ManyToManyField(
        "data_management.Statistic",
        blank=True,
        related_name="partners_hero_sections",
    )

    class Meta:
        verbose_name = "Partners Hero Section"
        verbose_name_plural = "Partners Hero Section"

    def __str__(self) -> str:
        return self.title or "Partners Hero Section"

    def hero_stats(self) -> list[dict]:
        return [
            {
                "position": index,
                "value": stat.value,
                "label": stat.label,
            }
            for index, stat in enumerate(self.selected_statistics.all(), start=1)
        ]


class PartnersPartnerSection(SingletonModel):
    """Partners — partner section. Search placeholder, a dynamic list of
    categories (name only) managed via the related `PartnersCategory`
    model, plus the employers chosen for this section from
    `data_management.Employer`."""

    search_placeholder = models.CharField(max_length=120, blank=True)
    explore_button_text = models.CharField(max_length=80, blank=True)
    selected_employers = models.ManyToManyField(
        "data_management.Employer",
        blank=True,
        related_name="partners_partner_sections",
    )

    class Meta:
        verbose_name = "Partners Partner Section"
        verbose_name_plural = "Partners Partner Section"

    def __str__(self) -> str:
        return "Partners Partner Section"

    def categories(self) -> list[dict]:
        return [
            {"position": index, "name": category.name}
            for index, category in enumerate(self.category_entries.all(), start=1)
        ]

    def partner_employers(self) -> list[dict]:
        return [
            {
                "position": index,
                "name": employer.name,
                "logo": employer.logo if employer.logo else None,
                "description": employer.description,
                "url": employer.url,
            }
            for index, employer in enumerate(self.selected_employers.all(), start=1)
        ]


class PartnersCategory(models.Model):
    """A single category shown in the Partners partner section."""

    section = models.ForeignKey(
        PartnersPartnerSection,
        on_delete=models.CASCADE,
        related_name="category_entries",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Category {self.pk}"


class PartnersFamilySection(SingletonModel):
    """Partners — family section. Label, title, description, selectable
    employers, and a "Load more" CTA (button text + URL)."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    selected_employers = models.ManyToManyField(
        "data_management.Employer",
        blank=True,
        related_name="partners_family_sections",
    )
    load_more_button_text = models.CharField(max_length=80, blank=True)
    load_more_button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Partners Family Section"
        verbose_name_plural = "Partners Family Section"

    def __str__(self) -> str:
        return self.title or "Partners Family Section"

    def family_employers(self) -> list[dict]:
        return [
            {
                "position": index,
                "name": employer.name,
                "logo": employer.logo if employer.logo else None,
                "description": employer.description,
                "url": employer.url,
            }
            for index, employer in enumerate(self.selected_employers.all(), start=1)
        ]


class PartnersReviewSection(SingletonModel):
    """Partners — review section. Label, title, plus a dynamic list of
    review cards (name + designation + message) managed via the related
    `PartnersReviewCard` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Partners Review Section"
        verbose_name_plural = "Partners Review Section"

    def __str__(self) -> str:
        return self.title or "Partners Review Section"

    def review_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "name": card.name,
                "designation": card.designation,
                "message": card.message,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class PartnersReviewCard(models.Model):
    """A single review card — name + designation + message."""

    section = models.ForeignKey(
        PartnersReviewSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=160, blank=True)
    designation = models.CharField(max_length=160, blank=True)
    message = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Review Card {self.pk}"


class PartnersFounderSection(SingletonModel):
    """Partners — founder section. Label, title, description, two CTA
    buttons (text + URL), plus a side image."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.URLField(blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Partners Founder Section"
        verbose_name_plural = "Partners Founder Section"

    def __str__(self) -> str:
        return self.title or "Partners Founder Section"
