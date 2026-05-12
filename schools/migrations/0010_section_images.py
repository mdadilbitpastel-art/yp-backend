"""Copy direct image fields on schools singletons into `SectionImage`
rows and drop the old fields."""

from django.db import migrations


SECTIONS = [
    ("schools", "SchoolsHeroSection", ["side_image"]),
    ("schools", "SchoolsSubscribeSection", ["side_image"]),
]


def copy_images_to_section_image(apps, schema_editor):
    SectionImage = apps.get_model("data_management", "SectionImage")
    ContentType = apps.get_model("contenttypes", "ContentType")

    for app_label, model_name, field_names in SECTIONS:
        Model = apps.get_model(app_label, model_name)
        ct, _ = ContentType.objects.get_or_create(
            app_label=app_label, model=model_name.lower()
        )
        for instance in Model.objects.all():
            order = SectionImage.objects.filter(
                content_type=ct, object_id=instance.pk
            ).count()
            for field_name in field_names:
                img = getattr(instance, field_name, None)
                if img and getattr(img, "name", ""):
                    SectionImage.objects.create(
                        content_type=ct,
                        object_id=instance.pk,
                        order=order,
                        image=img.name,
                    )
                    order += 1


def noop_reverse(apps, schema_editor):
    """Reverse: leave the new SectionImage rows in place."""


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0009_delete_schools_employer"),
        ("data_management", "0006_section_image"),
    ]

    operations = [
        migrations.RunPython(copy_images_to_section_image, noop_reverse),
        migrations.RemoveField(model_name="schoolsherosection", name="side_image"),
        migrations.RemoveField(model_name="schoolssubscribesection", name="side_image"),
    ]
