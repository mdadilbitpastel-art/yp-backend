"""Copy existing `schools.SchoolsEmployer` rows into `Employer` and
pre-select them on the Schools Employer section so the public page keeps
rendering the same logos it did before."""

from django.db import migrations


def copy_schools_employers(apps, schema_editor):
    SchoolsEmployer = apps.get_model("schools", "SchoolsEmployer")
    SchoolsEmployerSection = apps.get_model("schools", "SchoolsEmployerSection")
    Employer = apps.get_model("data_management", "Employer")

    legacy = list(SchoolsEmployer.objects.order_by("order", "id"))
    if not legacy:
        return

    new_ids = []
    for row in legacy:
        new_row = Employer.objects.create(
            name=row.name or "",
            logo=row.logo,  # FileField value copies the storage path reference.
            order=row.order,
        )
        new_ids.append(new_row.pk)

    section = SchoolsEmployerSection.objects.first()
    if section is not None:
        section.selected_employers.set(new_ids)


def noop_reverse(apps, schema_editor):
    """Reverse: leave the new Employer rows in place."""


class Migration(migrations.Migration):

    dependencies = [
        ("data_management", "0003_employer"),
        ("schools", "0008_employer_section_selected_employers"),
    ]

    operations = [
        migrations.RunPython(copy_schools_employers, noop_reverse),
    ]
