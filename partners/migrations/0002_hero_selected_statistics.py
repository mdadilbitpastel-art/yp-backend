from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0001_initial"),
        ("data_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnersherosection",
            name="selected_statistics",
            field=models.ManyToManyField(
                blank=True,
                related_name="partners_hero_sections",
                to="data_management.statistic",
            ),
        ),
    ]
