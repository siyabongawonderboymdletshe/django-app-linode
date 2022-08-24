# Generated by Django 4.1 on 2022-08-19 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BackOfficeApp', '0009_remove_customer_phone_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=150, verbose_name='Account Number')),
                ('loan_amount', models.BigIntegerField(verbose_name='Loan Name')),
                ('rate', models.IntegerField(verbose_name='Rate')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackOfficeApp.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('year', models.IntegerField(verbose_name='Year')),
                ('category', models.CharField(max_length=150, verbose_name='Category')),
                ('serial_number', models.CharField(max_length=150, verbose_name='Serial Number')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackOfficeApp.customer')),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackOfficeApp.productitem')),
            ],
        ),
        migrations.CreateModel(
            name='Catalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackOfficeApp.productitem')),
            ],
        ),
        migrations.CreateModel(
            name='AccountItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=150, verbose_name='Account Number')),
                ('market_value', models.BigIntegerField(verbose_name='Market Value')),
                ('operative_date', models.DateField(verbose_name='Operative Date')),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('SOLD', 'SOLD'), ('REMOVED', 'REMOVED'), ('UNAVAILABLE', 'UNAVAILABLE')], default='AVAILABLE', max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackOfficeApp.account')),
                ('product_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BackOfficeApp.productitem')),
            ],
        ),
    ]