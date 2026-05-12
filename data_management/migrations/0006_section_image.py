import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("data_management", "0005_employer_description_url"),
    ]

    operations = [
        migrations.CreateModel(
            name="SectionImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.PositiveIntegerField()),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "image",
                    models.ImageField(
                        upload_to="sections/images/",
                        validators=[
                            home.validators.validate_image_size,
                            home.validators.validate_image_extension,
                        ],
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "ordering": ("order", "id"),
                "indexes": [
                    models.Index(fields=["content_type", "object_id"], name="data_manage_content_idx"),
                ],
            },
        ),
    ]
