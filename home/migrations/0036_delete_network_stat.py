from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0035_network_selected_statistics"),
        ("data_management", "0002_migrate_network_stats"),
    ]

    operations = [
        migrations.DeleteModel(name="NetworkStat"),
    ]
