# Generated by Django 2.2.7 on 2020-09-10 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0024_card_is_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]