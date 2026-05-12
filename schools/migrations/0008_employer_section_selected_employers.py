from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0007_faq_section"),
        ("data_management", "0003_employer"),
    ]

    operations = [
        migrations.AddField(
            model_name="schoolsemployersection",
            name="selected_employers",
            field=models.ManyToManyField(
                blank=True,
                related_name="schools_employer_sections",
                to="data_management.employer",
            ),
        ),
    ]
