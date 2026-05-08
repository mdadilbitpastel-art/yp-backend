from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0006_subscribe_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolsFaqSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Schools FAQ Section",
                "verbose_name_plural": "Schools FAQ Section",
            },
        ),
        migrations.CreateModel(
            name="SchoolsFaqItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("question", models.CharField(blank=True, max_length=255)),
                ("answer", models.TextField(blank=True)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="items", to="schools.schoolsfaqsection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
