from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Statistic",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=80)),
                ("label", models.CharField(max_length=160)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Statistic",
                "verbose_name_plural": "Statistics",
                "ordering": ("order", "id"),
            },
        ),
    ]
