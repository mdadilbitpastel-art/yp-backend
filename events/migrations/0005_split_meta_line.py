from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0004_upcoming_section"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventsupcomingcard",
            name="meta_line",
        ),
        migrations.AddField(
            model_name="eventsupcomingcard",
            name="years_label",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="eventsupcomingcard",
            name="price_label",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
