from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0007_family_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnersReviewSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
            ],
            options={
                "verbose_name": "Partners Review Section",
                "verbose_name_plural": "Partners Review Section",
            },
        ),
        migrations.CreateModel(
            name="PartnersReviewCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("name", models.CharField(blank=True, max_length=160)),
                ("designation", models.CharField(blank=True, max_length=160)),
                ("message", models.TextField(blank=True)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="cards", to="partners.partnersreviewsection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
