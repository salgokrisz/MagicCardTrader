# Generated by Django 2.2.7 on 2020-07-12 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0003_auto_20200712_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardsforsale',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
