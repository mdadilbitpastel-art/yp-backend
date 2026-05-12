from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0004_hero_selected_employers"),
        ("data_management", "0005_employer_description_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnerspartnersection",
            name="selected_employers",
            field=models.ManyToManyField(
                blank=True,
                related_name="partners_partner_sections",
                to="data_management.employer",
            ),
        ),
        migrations.RemoveField(
            model_name="partnersherosection",
            name="selected_employers",
        ),
    ]
