# Generated by Django 4.1 on 2022-08-22 19:40

import BackOfficeApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0023_productitemimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productitemimage',
            name='image',
            field=models.ImageField(upload_to=BackOfficeApp.models.content_file_name),
        ),
    ]
