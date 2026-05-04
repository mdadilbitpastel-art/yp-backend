"""Promote feature_N_button_text to a single shared features_button_text field.

Preserves any value already entered on per-card columns by copying the first
non-empty one into the new shared column before the old ones are dropped.
"""

from django.db import migrations, models


def copy_existing_button_text(apps, schema_editor):
    HeroSection = apps.get_model("home", "HeroSection")
    for row in HeroSection.objects.all():
        if row.features_button_text:
            continue
        for i in range(1, 6):
            value = getattr(row, f"feature_{i}_button_text", "") or ""
            if value:
                row.features_button_text = value
                row.save(update_fields=["features_button_text"])
                break


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0009_remove_active_toggles"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="features_button_text",
            field=models.CharField(
                blank=True,
                help_text="Shared button label used on every feature card.",
                max_length=80,
            ),
        ),
        migrations.RunPython(
            copy_existing_button_text,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="feature_1_button_text",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="feature_2_button_text",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="feature_3_button_text",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="feature_4_button_text",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="feature_5_button_text",
        ),
    ]
