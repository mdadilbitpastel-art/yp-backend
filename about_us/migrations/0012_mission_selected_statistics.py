from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("about_us", "0011_social_media_section"),
        ("data_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutusmissionsection",
            name="selected_statistics",
            field=models.ManyToManyField(
                blank=True,
                related_name="mission_sections",
                to="data_management.statistic",
            ),
        ),
    ]
