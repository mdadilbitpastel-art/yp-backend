from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_management", "0004_migrate_schools_employers"),
    ]

    operations = [
        migrations.AddField(
            model_name="employer",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="employer",
            name="url",
            field=models.URLField(blank=True),
        ),
    ]
