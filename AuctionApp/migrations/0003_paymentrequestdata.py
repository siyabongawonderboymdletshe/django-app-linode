# Generated by Django 4.1 on 2022-08-07 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuctionApp', '0002_alter_itembuyer_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequestData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.CharField(max_length=32)),
                ('data', models.TextField(blank=True)),
                ('date_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
