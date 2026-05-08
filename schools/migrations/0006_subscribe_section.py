import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("schools", "0005_benchmark_section"),
    ]

    operations = [
        migrations.CreateModel(
            name="SchoolsSubscribeSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(blank=True, max_length=120)),
                ("title", models.CharField(blank=True, max_length=255)),
                ("description", models.TextField(blank=True)),
                ("button_text", models.CharField(blank=True, max_length=80)),
                ("button_url", models.URLField(blank=True)),
                ("side_image", models.ImageField(blank=True, null=True, upload_to="schools/subscribe/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension])),
            ],
            options={
                "verbose_name": "Schools Subscribe Section",
                "verbose_name_plural": "Schools Subscribe Section",
            },
        ),
        migrations.CreateModel(
            name="SchoolsSubscribeField",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0)),
                ("field_name", models.CharField(blank=True, max_length=120)),
                ("placeholder", models.CharField(blank=True, max_length=160)),
                ("section", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="fields", to="schools.schoolssubscribesection")),
            ],
            options={
                "ordering": ("order", "id"),
            },
        ),
    ]
