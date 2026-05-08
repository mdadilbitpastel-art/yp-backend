from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployersMissionSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Employers Mission Section",
                "verbose_name_plural": "Employers Mission Section",
            },
        ),
        migrations.CreateModel(
            name="EmployersMissionPoint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("text", models.CharField(blank=True, max_length=255)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="points", to="employers.employersmissionsection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
