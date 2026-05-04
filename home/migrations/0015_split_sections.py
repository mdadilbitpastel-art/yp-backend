"""Split the single HeroSection singleton into one table per homepage section.

Hero stays in `home_herosection` (with non-Hero columns dropped). Each other
section moves into its own singleton table; existing data is copied via the
`copy_data` RunPython step before the legacy columns are removed.
"""

import home.validators
from django.db import migrations, models


FEATURE_FIELDS = (
    "features_title",
    "features_description",
    "features_button_text",
    *[f"feature_{i}_title" for i in range(1, 6)],
    *[f"feature_{i}_icon" for i in range(1, 6)],
    *[f"feature_{i}_button_url" for i in range(1, 6)],
)

ABOUT_FIELDS = (
    "about_section_label",
    "about_section_title",
    "about_section_description",
    "about_section_primary_button_text",
    "about_section_primary_button_url",
    "about_section_secondary_button_text",
    "about_section_secondary_button_url",
    "about_section_image",
)

NETWORK_FIELDS = (
    "network_section_title",
    "network_section_video_url",
    *[f"network_stat_{i}_value" for i in range(1, 5)],
    *[f"network_stat_{i}_label" for i in range(1, 5)],
)

TALENT_POOL_FIELDS = (
    "talent_pool_section_title",
    "talent_pool_section_subtitle",
    "talent_pool_section_description",
    "talent_pool_section_primary_button_text",
    "talent_pool_section_primary_button_url",
    "talent_pool_section_secondary_button_text",
    "talent_pool_section_secondary_button_url",
    "talent_pool_section_image",
)

APPLY_FIELDS = (
    "apply_section_title",
    "apply_section_subtitle",
    *[
        f"apply_company_{i}_{suffix}"
        for i in range(1, 4)
        for suffix in (
            "label",
            "title",
            "description",
            "button_text",
            "button_url",
            "large_image",
            "small_image",
        )
    ],
)


def _copy(apps, src, dst_model_name, fields):
    Dst = apps.get_model("home", dst_model_name)
    payload = {f: getattr(src, f) for f in fields}
    payload["pk"] = 1
    Dst.objects.update_or_create(pk=1, defaults=payload)


def copy_data(apps, schema_editor):
    HeroSection = apps.get_model("home", "HeroSection")
    src = HeroSection.objects.filter(pk=1).first()
    if src is None:
        return
    _copy(apps, src, "FeatureSection", FEATURE_FIELDS)
    _copy(apps, src, "AboutSection", ABOUT_FIELDS)
    _copy(apps, src, "NetworkSection", NETWORK_FIELDS)
    _copy(apps, src, "TalentPoolSection", TALENT_POOL_FIELDS)
    _copy(apps, src, "ApplySection", APPLY_FIELDS)


def noop_reverse(apps, schema_editor):
    # Reverse migration is intentionally a no-op — the destination tables
    # are dropped by the schema reversal of CreateModel below.
    return


def _image_field(upload_to):
    return models.ImageField(
        blank=True,
        null=True,
        upload_to=upload_to,
        validators=[
            home.validators.validate_image_size,
            home.validators.validate_image_extension,
        ],
    )


def _company_fields(i):
    return [
        (f"apply_company_{i}_label", models.CharField(blank=True, max_length=120)),
        (f"apply_company_{i}_title", models.CharField(blank=True, max_length=255)),
        (f"apply_company_{i}_description", models.TextField(blank=True)),
        (f"apply_company_{i}_button_text", models.CharField(blank=True, max_length=80)),
        (f"apply_company_{i}_button_url", models.URLField(blank=True)),
        (f"apply_company_{i}_large_image", _image_field("home/apply/")),
        (f"apply_company_{i}_small_image", _image_field("home/apply/")),
    ]


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0014_apply_section"),
    ]

    operations = [
        # ----- new section tables ------------------------------------
        migrations.CreateModel(
            name="FeatureSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("features_title", models.CharField(blank=True, max_length=255)),
                ("features_description", models.TextField(blank=True)),
                (
                    "features_button_text",
                    models.CharField(
                        blank=True,
                        help_text="Shared button label used on every feature card.",
                        max_length=80,
                    ),
                ),
                *[(f"feature_{i}_title", models.CharField(blank=True, max_length=255)) for i in range(1, 6)],
                *[(f"feature_{i}_icon", _image_field("home/features/")) for i in range(1, 6)],
                *[(f"feature_{i}_button_url", models.URLField(blank=True)) for i in range(1, 6)],
            ],
            options={"verbose_name": "Feature Section", "verbose_name_plural": "Feature Section"},
        ),
        migrations.CreateModel(
            name="AboutSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("about_section_label", models.CharField(blank=True, max_length=120)),
                ("about_section_title", models.CharField(blank=True, max_length=255)),
                ("about_section_description", models.TextField(blank=True)),
                ("about_section_primary_button_text", models.CharField(blank=True, max_length=80)),
                ("about_section_primary_button_url", models.URLField(blank=True)),
                ("about_section_secondary_button_text", models.CharField(blank=True, max_length=80)),
                ("about_section_secondary_button_url", models.URLField(blank=True)),
                ("about_section_image", _image_field("home/about/")),
            ],
            options={"verbose_name": "About Section", "verbose_name_plural": "About Section"},
        ),
        migrations.CreateModel(
            name="NetworkSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("network_section_title", models.CharField(blank=True, max_length=255)),
                ("network_section_video_url", models.URLField(blank=True)),
                *[(f"network_stat_{i}_value", models.CharField(blank=True, max_length=80)) for i in range(1, 5)],
                *[(f"network_stat_{i}_label", models.CharField(blank=True, max_length=160)) for i in range(1, 5)],
            ],
            options={"verbose_name": "Network Section", "verbose_name_plural": "Network Section"},
        ),
        migrations.CreateModel(
            name="TalentPoolSection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("talent_pool_section_title", models.CharField(blank=True, max_length=255)),
                ("talent_pool_section_subtitle", models.CharField(blank=True, max_length=255)),
                ("talent_pool_section_description", models.TextField(blank=True)),
                ("talent_pool_section_primary_button_text", models.CharField(blank=True, max_length=80)),
                ("talent_pool_section_primary_button_url", models.URLField(blank=True)),
                ("talent_pool_section_secondary_button_text", models.CharField(blank=True, max_length=80)),
                ("talent_pool_section_secondary_button_url", models.URLField(blank=True)),
                ("talent_pool_section_image", _image_field("home/talent_pool/")),
            ],
            options={"verbose_name": "Talent Pool Section", "verbose_name_plural": "Talent Pool Section"},
        ),
        migrations.CreateModel(
            name="ApplySection",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("apply_section_title", models.CharField(blank=True, max_length=255)),
                ("apply_section_subtitle", models.CharField(blank=True, max_length=255)),
                *_company_fields(1),
                *_company_fields(2),
                *_company_fields(3),
            ],
            options={"verbose_name": "Apply Section", "verbose_name_plural": "Apply Section"},
        ),

        # ----- copy data from HeroSection into the new tables ---------
        migrations.RunPython(copy_data, noop_reverse),

        # ----- drop the moved columns from HeroSection ----------------
        *[migrations.RemoveField(model_name="herosection", name=f) for f in FEATURE_FIELDS],
        *[migrations.RemoveField(model_name="herosection", name=f) for f in ABOUT_FIELDS],
        *[migrations.RemoveField(model_name="herosection", name=f) for f in NETWORK_FIELDS],
        *[migrations.RemoveField(model_name="herosection", name=f) for f in TALENT_POOL_FIELDS],
        *[migrations.RemoveField(model_name="herosection", name=f) for f in APPLY_FIELDS],
    ]
