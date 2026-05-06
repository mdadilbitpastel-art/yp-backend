"""Replace the network_section_video_url URL field with a video file upload."""

import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0028_network_stats"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="networksection",
            name="network_section_video_url",
        ),
        migrations.AddField(
            model_name="networksection",
            name="network_section_video",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="home/network/",
                validators=[
                    home.validators.validate_video_size,
                    home.validators.validate_video_extension,
                ],
            ),
        ),
    ]
