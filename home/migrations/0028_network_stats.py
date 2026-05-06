"""Replace the 4 inline stat field-pairs on NetworkSection with a related
NetworkStat model. Existing values are copied across before the old columns
are dropped."""

import django.db.models.deletion
from django.db import migrations, models


_OLD_STAT_COUNT = 4


def _copy_stats_forward(apps, schema_editor):
    NetworkSection = apps.get_model("home", "NetworkSection")
    NetworkStat = apps.get_model("home", "NetworkStat")
    for section in NetworkSection.objects.all():
        for i in range(1, _OLD_STAT_COUNT + 1):
            value = getattr(section, f"network_stat_{i}_value", "") or ""
            label = getattr(section, f"network_stat_{i}_label", "") or ""
            if not (value or label):
                continue
            NetworkStat.objects.create(
                section=section,
                order=i,
                value=value,
                label=label,
            )


def _noop_reverse(apps, schema_editor):
    NetworkStat = apps.get_model("home", "NetworkStat")
    NetworkStat.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0027_feature_cards"),
    ]

    operations = [
        migrations.CreateModel(
            name="NetworkStat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("value", models.CharField(blank=True, max_length=80)),
                ("label", models.CharField(blank=True, max_length=160)),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stats",
                        to="home.networksection",
                    ),
                ),
            ],
            options={"ordering": ("order", "id")},
        ),
        migrations.RunPython(_copy_stats_forward, _noop_reverse),
        migrations.RemoveField(model_name="networksection", name="network_stat_1_value"),
        migrations.RemoveField(model_name="networksection", name="network_stat_1_label"),
        migrations.RemoveField(model_name="networksection", name="network_stat_2_value"),
        migrations.RemoveField(model_name="networksection", name="network_stat_2_label"),
        migrations.RemoveField(model_name="networksection", name="network_stat_3_value"),
        migrations.RemoveField(model_name="networksection", name="network_stat_3_label"),
        migrations.RemoveField(model_name="networksection", name="network_stat_4_value"),
        migrations.RemoveField(model_name="networksection", name="network_stat_4_label"),
    ]
