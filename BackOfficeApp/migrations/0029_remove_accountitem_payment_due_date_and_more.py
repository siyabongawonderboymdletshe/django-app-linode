# Generated by Django 4.1 on 2022-08-24 13:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0028_rename_operative_date_accountitem_payment_due_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountitem',
            name='payment_due_date',
        ),
        migrations.AddField(
            model_name='account',
            name='payment_due_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Payment Due Date'),
            preserve_default=False,
        ),
    ]