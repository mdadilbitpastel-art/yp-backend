"""Copy existing `home.NetworkStat` rows into the new `Statistic` table.

Pre-refactor the Home Network section and About Us Mission section both
displayed the *same* set of rows (FK'd to the singleton NetworkSection).
After this migration every existing row becomes a `Statistic`, and both
sections pre-select all of them so the public pages keep rendering the
same statistics they did before.
"""

from django.db import migrations


def copy_network_stats(apps, schema_editor):
    NetworkStat = apps.get_model("home", "NetworkStat")
    NetworkSection = apps.get_model("home", "NetworkSection")
    AboutUsMissionSection = apps.get_model("about_us", "AboutUsMissionSection")
    Statistic = apps.get_model("data_management", "Statistic")

    legacy = list(NetworkStat.objects.order_by("order", "id"))
    if not legacy:
        return

    new_ids = []
    for stat in legacy:
        new_stat = Statistic.objects.create(
            value=stat.value or "",
            label=stat.label or "",
            order=stat.order,
        )
        new_ids.append(new_stat.pk)

    network_section = NetworkSection.objects.first()
    if network_section is not None:
        network_section.selected_statistics.set(new_ids)

    mission_section = AboutUsMissionSection.objects.first()
    if mission_section is not None:
        mission_section.selected_statistics.set(new_ids)


def noop_reverse(apps, schema_editor):
    """Reverse: nothing to undo — leaves new Statistic rows in place."""


class Migration(migrations.Migration):

    dependencies = [
        ("data_management", "0001_initial"),
        ("home", "0035_network_selected_statistics"),
        ("about_us", "0012_mission_selected_statistics"),
    ]

    operations = [
        migrations.RunPython(copy_network_stats, noop_reverse),
    ]
