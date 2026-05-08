from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0003_employer_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="schoolsemployer",
            name="name",
            field=models.CharField(blank=True, max_length=160),
        ),
    ]
