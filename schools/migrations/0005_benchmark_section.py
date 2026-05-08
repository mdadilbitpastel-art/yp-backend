from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0004_schoolsemployer_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolsBenchmarkSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Schools Benchmark Section",
                "verbose_name_plural": "Schools Benchmark Section",
            },
        ),
        migrations.CreateModel(
            name="SchoolsBenchmarkCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="cards", to="schools.schoolsbenchmarksection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
