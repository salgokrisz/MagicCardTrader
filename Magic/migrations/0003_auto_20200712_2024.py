# Generated by Django 2.2.7 on 2020-07-12 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0002_auto_20200701_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardsforsale',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='user',
            name='available_cards',
            field=models.IntegerField(),
        ),
    ]
