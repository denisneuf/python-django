# Generated by Django 4.0.4 on 2022-05-27 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_orders_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orders',
            options={'managed': False},
        ),
        migrations.AlterModelTable(
            name='uploads',
            table=None,
        ),
    ]
