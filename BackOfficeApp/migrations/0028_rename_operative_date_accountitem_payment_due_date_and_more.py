# Generated by Django 4.1 on 2022-08-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0027_remove_accountitem_product_item_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accountitem',
            old_name='operative_date',
            new_name='payment_due_date',
        ),
        migrations.RemoveField(
            model_name='accountitem',
            name='market_value',
        ),
        migrations.AddField(
            model_name='productitem',
            name='market_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=13, verbose_name='Market Value'),
            preserve_default=False,
        ),
    ]