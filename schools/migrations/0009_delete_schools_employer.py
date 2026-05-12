from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0008_employer_section_selected_employers"),
        ("data_management", "0004_migrate_schools_employers"),
    ]

    operations = [
        migrations.DeleteModel(name="SchoolsEmployer"),
    ]
