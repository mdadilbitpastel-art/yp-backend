"""Add the Stats / Network section fields to the HeroSection singleton row."""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0011_remove_herosection_subtitle"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="network_section_title",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_section_video_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_1_value",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_1_label",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_2_value",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_2_label",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_3_value",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_3_label",
            field=models.CharField(blank=True, max_length=160),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_4_value",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="herosection",
            name="network_stat_4_label",
            field=models.CharField(blank=True, max_length=160),
        ),
    ]
