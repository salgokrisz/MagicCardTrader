# Generated by Django 3.1.1 on 2020-09-21 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0029_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
    ]
