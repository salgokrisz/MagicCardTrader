# Generated by Django 2.1.7 on 2020-07-27 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0007_auto_20200727_1344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='amount',
        ),
    ]
