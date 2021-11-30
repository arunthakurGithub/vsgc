# Generated by Django 3.2 on 2021-04-27 20:11

import acrpapp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acrpapp', '0008_alter_designapp_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designapp',
            name='Upload',
            field=models.FileField(max_length=256, null=True, upload_to='media/', validators=[acrpapp.validators.validate_file_size]),
        ),
    ]
