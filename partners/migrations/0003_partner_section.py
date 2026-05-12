from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0002_hero_selected_statistics"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnersPartnerSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("search_placeholder", models.CharField(blank=True, max_length=120)),
            ],
            options={
                "verbose_name": "Partners Partner Section",
                "verbose_name_plural": "Partners Partner Section",
            },
        ),
        migrations.CreateModel(
            name="PartnersCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("name", models.CharField(blank=True, max_length=160)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="category_entries", to="partners.partnerspartnersection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
