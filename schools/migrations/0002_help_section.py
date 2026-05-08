from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolsHelpSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "verbose_name": "Schools Help Section",
                "verbose_name_plural": "Schools Help Section",
            },
        ),
        migrations.CreateModel(
            name="SchoolsHelpCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="cards", to="schools.schoolshelpsection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
