"""Replace the 5 inline feature card field-groups on FeatureSection with a
related FeatureCard model. Existing card data is copied across before the
old columns are dropped."""

import django.db.models.deletion
import home.validators
from django.db import migrations, models


_OLD_CARD_COUNT = 5


def _copy_cards_forward(apps, schema_editor):
    FeatureSection = apps.get_model("home", "FeatureSection")
    FeatureCard = apps.get_model("home", "FeatureCard")
    for section in FeatureSection.objects.all():
        for i in range(1, _OLD_CARD_COUNT + 1):
            title = getattr(section, f"feature_{i}_title", "") or ""
            icon = getattr(section, f"feature_{i}_icon", None)
            icon_name = icon.name if icon else ""
            button_url = getattr(section, f"feature_{i}_button_url", "") or ""
            if not (title or icon_name or button_url):
                continue
            FeatureCard.objects.create(
                section=section,
                order=i,
                title=title,
                icon=icon_name,
                button_url=button_url,
            )


def _noop_reverse(apps, schema_editor):
    # The old per-card fields are removed in this migration; no reverse copy
    # path exists. Reverse simply drops the migrated rows.
    FeatureCard = apps.get_model("home", "FeatureCard")
    FeatureCard.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0026_header_tabs"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeatureCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=255)),
                (
                    "icon",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="home/features/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                ("button_url", models.URLField(blank=True)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cards",
                        to="home.featuresection",
                    ),
                ),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.RunPython(_copy_cards_forward, _noop_reverse),
        migrations.RemoveField(model_name="featuresection", name="feature_1_title"),
        migrations.RemoveField(model_name="featuresection", name="feature_1_icon"),
        migrations.RemoveField(model_name="featuresection", name="feature_1_button_url"),
        migrations.RemoveField(model_name="featuresection", name="feature_2_title"),
        migrations.RemoveField(model_name="featuresection", name="feature_2_icon"),
        migrations.RemoveField(model_name="featuresection", name="feature_2_button_url"),
        migrations.RemoveField(model_name="featuresection", name="feature_3_title"),
        migrations.RemoveField(model_name="featuresection", name="feature_3_icon"),
        migrations.RemoveField(model_name="featuresection", name="feature_3_button_url"),
        migrations.RemoveField(model_name="featuresection", name="feature_4_title"),
        migrations.RemoveField(model_name="featuresection", name="feature_4_icon"),
        migrations.RemoveField(model_name="featuresection", name="feature_4_button_url"),
        migrations.RemoveField(model_name="featuresection", name="feature_5_title"),
        migrations.RemoveField(model_name="featuresection", name="feature_5_icon"),
        migrations.RemoveField(model_name="featuresection", name="feature_5_button_url"),
    ]
