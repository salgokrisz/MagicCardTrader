# Generated by Django 2.2.7 on 2020-09-10 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0027_card_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='slug',
        ),
    ]
