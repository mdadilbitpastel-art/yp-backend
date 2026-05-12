from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0005_split_meta_line"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventsupcomingcard",
            name="button_text",
        ),
        migrations.AddField(
            model_name="eventsupcomingsection",
            name="card_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
