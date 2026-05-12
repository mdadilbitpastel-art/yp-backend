from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0005_move_selected_employers"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnerspartnersection",
            name="explore_button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
    ]
