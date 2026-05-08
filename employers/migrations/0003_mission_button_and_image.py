import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employers", "0002_mission_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="employersmissionsection",
            name="button_text",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="employersmissionsection",
            name="button_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="employersmissionsection",
            name="side_image",
            field=models.ImageField(blank=True, null=True, upload_to="employers/mission/", validators=[home.validators.validate_image_size, home.validators.validate_image_extension]),
        ),
    ]
