from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0034_talent_pool_label"),
        ("data_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="networksection",
            name="selected_statistics",
            field=models.ManyToManyField(
                blank=True,
                related_name="network_sections",
                to="data_management.statistic",
            ),
        ),
    ]
