# Generated by Django 2.1.7 on 2020-08-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0015_auto_20200810_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_photo',
            field=models.FileField(default='profile_images/Magic_card_back.jpg', upload_to='profile_images'),
        ),
    ]
