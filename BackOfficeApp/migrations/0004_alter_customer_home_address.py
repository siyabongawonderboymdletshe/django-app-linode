# Generated by Django 4.1 on 2022-08-18 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0003_customer_home_address_alter_customer_id_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='home_address',
            field=models.TextField(default='', max_length=255, verbose_name='home address'),
        ),
    ]