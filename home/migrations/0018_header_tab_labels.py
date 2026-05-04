"""Add per-module tab label overrides to HeaderSettings."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0017_header_settings"),
    ]

    operations = [
        migrations.AddField(
            model_name="headersettings",
            name="tab_labels",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Per-module overrides for header tab labels — keyed by module key.",
            ),
        ),
    ]
