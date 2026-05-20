"""Switch `TestimonialUser` from inline name/profile_image fields to a
required `team_member` FK that points at `data_management.TeamMember`.
Existing rows can't be auto-mapped to team members, so we drop them
before re-shaping the table."""

from django.db import migrations, models


def _drop_existing_rows(apps, schema_editor):
    TestimonialUser = apps.get_model("home", "TestimonialUser")
    TestimonialUser.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0041_appsection_bottom_note"),
        ("data_management", "0009_teammember"),
    ]

    operations = [
        migrations.RunPython(_drop_existing_rows, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="testimonialuser",
            name="name",
        ),
        migrations.RemoveField(
            model_name="testimonialuser",
            name="profile_image",
        ),
        migrations.AddField(
            model_name="testimonialuser",
            name="team_member",
            field=models.ForeignKey(
                null=True,
                on_delete=models.deletion.CASCADE,
                related_name="testimonial_entries",
                to="data_management.teammember",
            ),
        ),
        migrations.AlterField(
            model_name="testimonialuser",
            name="message",
            field=models.TextField(),
        ),
        migrations.AlterUniqueTogether(
            name="testimonialuser",
            unique_together={("section", "team_member")},
        ),
    ]
