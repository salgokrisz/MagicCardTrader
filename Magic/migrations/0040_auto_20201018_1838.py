# Generated by Django 3.1.1 on 2020-10-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0039_auto_20201018_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='image_url',
            field=models.TextField(),
        ),
    ]
