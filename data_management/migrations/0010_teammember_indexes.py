from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0009_teammember'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='teammember',
            index=models.Index(fields=['order', 'id'], name='tm_order_id_idx'),
        ),
        migrations.AddIndex(
            model_name='teammember',
            index=models.Index(fields=['name'], name='tm_name_idx'),
        ),
        migrations.AddIndex(
            model_name='teammember',
            index=models.Index(fields=['designation'], name='tm_designation_idx'),
        ),
    ]
