"""Drop the standalone `AboutUsMissionStat` table and have the About Us
Mission section share stats with `home.NetworkStat`.

Any rows already present in `AboutUsMissionStat` are copied into
`home.NetworkStat` (FK to the singleton `home.NetworkSection`) before the
old table is removed, so editor data is preserved.
"""

from django.db import migrations


def _migrate_mission_stats_to_network(apps, schema_editor):
    AboutUsMissionStat = apps.get_model("about_us", "AboutUsMissionStat")
    NetworkSection = apps.get_model("home", "NetworkSection")
    NetworkStat = apps.get_model("home", "NetworkStat")

    section, _ = NetworkSection.objects.get_or_create(pk=1)

    for stat in AboutUsMissionStat.objects.all().order_by("order", "id"):
        if NetworkStat.objects.filter(
            section=section, value=stat.value, label=stat.label
        ).exists():
            continue
        NetworkStat.objects.create(
            section=section,
            order=stat.order,
            value=stat.value,
            label=stat.label,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("about_us", "0002_mission_section"),
        ("home", "0032_testimonial_users_dynamic"),
    ]

    operations = [
        migrations.RunPython(
            _migrate_mission_stats_to_network,
            migrations.RunPython.noop,
        ),
        migrations.DeleteModel(name="AboutUsMissionStat"),
    ]
