# Generated by Django 4.1 on 2022-08-24 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0026_productrequest_alter_account_number_of_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountitem',
            name='product_item',
        ),
        migrations.AddField(
            model_name='accountitem',
            name='product_item',
            field=models.ManyToManyField(to='BackOfficeApp.productitem'),
        ),
    ]