from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0006_partner_section_explore_button"),
        ("data_management", "0005_employer_description_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="PartnersFamilySection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("load_more_button_text", models.CharField(blank=True, max_length=80)),
                ("load_more_button_url", models.URLField(blank=True)),
                (
                    "selected_employers",
                    models.ManyToManyField(
                        blank=True,
                        related_name="partners_family_sections",
                        to="data_management.employer",
                    ),
                ),
            ],
            options={
                "verbose_name": "Partners Family Section",
                "verbose_name_plural": "Partners Family Section",
            },
        ),
    ]
