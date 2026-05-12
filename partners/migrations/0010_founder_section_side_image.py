import home.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("partners", "0009_founder_section"),
    ]

    operations = [
        migrations.AddField(
            model_name="partnersfoundersection",
            name="side_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="partners/founder/",
                validators=[
                    home.validators.validate_image_size,
                    home.validators.validate_image_extension,
                ],
            ),
        ),
    ]
