# Generated by Django 2.1.1 on 2022-05-25 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_applicant_details_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant_details',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
    ]