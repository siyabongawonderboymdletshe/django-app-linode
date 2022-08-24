# Generated by Django 4.1 on 2022-08-18 22:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0006_alter_customer_id_number_alter_customer_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='id_number',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator('^\\d{0,9}$'), django.core.validators.MinLengthValidator(13)], verbose_name='id number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{0,9}$'), django.core.validators.MinLengthValidator(13)], verbose_name='phone number'),
        ),
    ]