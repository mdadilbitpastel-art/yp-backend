"""Drop the auto-populated `tab_labels` JSON field and add the related
`HeaderTab` model so editors can manage navigation tabs manually."""

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0025_alter_appsection_id_alter_socialmediacard_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="headersettings",
            name="tab_labels",
        ),
        migrations.CreateModel(
            name="HeaderTab",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("label", models.CharField(max_length=80)),
                ("url", models.CharField(blank=True, max_length=255)),
                (
                    "header",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tabs",
                        to="home.headersettings",
                    ),
                ),
            ],
            options={"ordering": ("order", "id")},
        ),
    ]
