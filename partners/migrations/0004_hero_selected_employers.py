from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0003_partner_section"),
        ("data_management", "0005_employer_description_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnersherosection",
            name="selected_employers",
            field=models.ManyToManyField(
                blank=True,
                related_name="partners_hero_sections",
                to="data_management.employer",
            ),
        ),
    ]
