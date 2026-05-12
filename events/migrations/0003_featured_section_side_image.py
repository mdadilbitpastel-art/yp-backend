import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_featured_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventsfeaturedsection",
            name="side_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="events/featured/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
    ]
