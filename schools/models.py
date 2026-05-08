"""
Schools page CMS models.

Each Schools section lives in its own singleton table — added one at a
time as the page grows. Reuses `home.models.SingletonModel` as the
abstract base so all sections share the same single-row guarantee +
`load()` helper.
"""

from django.db import models

from home.models import SingletonModel
from home.validators import validate_image_extension, validate_image_size


class SchoolsHeroSection(SingletonModel):
    """Schools — top hero / banner section. Label, title, description, two
    CTA buttons, and a side image."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    primary_button_text = models.CharField(max_length=80, blank=True)
    primary_button_url = models.URLField(blank=True)
    secondary_button_text = models.CharField(max_length=80, blank=True)
    secondary_button_url = models.URLField(blank=True)

    side_image = models.ImageField(
        upload_to="schools/hero/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Schools Hero Section"
        verbose_name_plural = "Schools Hero Section"

    def __str__(self) -> str:
        return self.title or "Schools Hero Section"


class SchoolsHelpSection(SingletonModel):
    """Schools — help section. Label, title, plus a dynamic list of help
    cards (title + description) managed via the related `SchoolsHelpCard`
    model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Schools Help Section"
        verbose_name_plural = "Schools Help Section"

    def __str__(self) -> str:
        return self.title or "Schools Help Section"

    def help_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "title": card.title,
                "description": card.description,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class SchoolsHelpCard(models.Model):
    """A single help card — title + description."""

    section = models.ForeignKey(
        SchoolsHelpSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Help Card {self.pk}"


class SchoolsEmployerSection(SingletonModel):
    """Schools — employer section. Label, title, description, single CTA
    button, plus a dynamic list of employer logos managed via the related
    `SchoolsEmployer` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Schools Employer Section"
        verbose_name_plural = "Schools Employer Section"

    def __str__(self) -> str:
        return self.title or "Schools Employer Section"

    def employers(self) -> list[dict]:
        return [
            {
                "position": index,
                "name": employer.name,
                "logo": employer.logo if employer.logo else None,
            }
            for index, employer in enumerate(self.entries.all(), start=1)
        ]


class SchoolsEmployer(models.Model):
    """A single employer entry — name + logo image."""

    section = models.ForeignKey(
        SchoolsEmployerSection,
        on_delete=models.CASCADE,
        related_name="entries",
    )
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=160, blank=True)
    logo = models.ImageField(
        upload_to="schools/employers/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.name or f"Employer {self.pk}"


class SchoolsBenchmarkSection(SingletonModel):
    """Schools — benchmark section. Label, title, description, plus a
    dynamic list of benchmark cards (title + description) managed via the
    related `SchoolsBenchmarkCard` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Schools Benchmark Section"
        verbose_name_plural = "Schools Benchmark Section"

    def __str__(self) -> str:
        return self.title or "Schools Benchmark Section"

    def benchmark_cards(self) -> list[dict]:
        return [
            {
                "position": index,
                "title": card.title,
                "description": card.description,
            }
            for index, card in enumerate(self.cards.all(), start=1)
        ]


class SchoolsBenchmarkCard(models.Model):
    """A single benchmark card — title + description."""

    section = models.ForeignKey(
        SchoolsBenchmarkSection,
        on_delete=models.CASCADE,
        related_name="cards",
    )
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.title or f"Benchmark Card {self.pk}"


class SchoolsSubscribeSection(SingletonModel):
    """Schools — subscribe section. Label, title, description, subscribe
    CTA button, side image, plus a dynamic list of form fields managed via
    the related `SchoolsSubscribeField` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    button_text = models.CharField(max_length=80, blank=True)
    button_url = models.URLField(blank=True)

    side_image = models.ImageField(
        upload_to="schools/subscribe/",
        validators=[validate_image_size, validate_image_extension],
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Schools Subscribe Section"
        verbose_name_plural = "Schools Subscribe Section"

    def __str__(self) -> str:
        return self.title or "Schools Subscribe Section"

    def subscribe_fields(self) -> list[dict]:
        return [
            {
                "position": index,
                "field_name": field.field_name,
                "placeholder": field.placeholder,
            }
            for index, field in enumerate(self.fields.all(), start=1)
        ]


class SchoolsSubscribeField(models.Model):
    """A single form field definition for the subscribe form — name +
    placeholder."""

    section = models.ForeignKey(
        SchoolsSubscribeSection,
        on_delete=models.CASCADE,
        related_name="fields",
    )
    order = models.PositiveIntegerField(default=0)
    field_name = models.CharField(max_length=120, blank=True)
    placeholder = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.field_name or f"Subscribe Field {self.pk}"


class SchoolsFaqSection(SingletonModel):
    """Schools — FAQ section. Label, title, description, plus a dynamic
    list of Q&A cards (question + answer) managed via the related
    `SchoolsFaqItem` model."""

    label = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Schools FAQ Section"
        verbose_name_plural = "Schools FAQ Section"

    def __str__(self) -> str:
        return self.title or "Schools FAQ Section"

    def faq_items(self) -> list[dict]:
        return [
            {
                "position": index,
                "question": item.question,
                "answer": item.answer,
            }
            for index, item in enumerate(self.items.all(), start=1)
        ]


class SchoolsFaqItem(models.Model):
    """A single FAQ entry — question + answer."""

    section = models.ForeignKey(
        SchoolsFaqSection,
        on_delete=models.CASCADE,
        related_name="items",
    )
    order = models.PositiveIntegerField(default=0)
    question = models.CharField(max_length=255, blank=True)
    answer = models.TextField(blank=True)

    class Meta:
        ordering = ("order", "id")

    def __str__(self) -> str:
        return self.question or f"FAQ Item {self.pk}"
