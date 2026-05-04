"""Drop unused HeroSection columns: app_store_url, play_store_url, is_active, created_at."""

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_hero_singleton"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="herosection",
            name="app_store_url",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="play_store_url",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="created_at",
        ),
    ]
