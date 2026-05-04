"""Add the bottom button (text + url) to the Apply section."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0015_split_sections"),
    ]

    operations = [
        migrations.AddField(
            model_name="applysection",
            name="apply_section_bottom_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="applysection",
            name="apply_section_bottom_button_url",
            field=models.URLField(blank=True),
        ),
    ]
