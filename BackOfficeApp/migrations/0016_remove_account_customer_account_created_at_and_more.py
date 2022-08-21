# Generated by Django 4.1 on 2022-08-19 12:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0015_remove_account_account_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='customer',
        ),
        migrations.AddField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='sale_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Sale Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountitem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated Date'),
        ),
    ]
