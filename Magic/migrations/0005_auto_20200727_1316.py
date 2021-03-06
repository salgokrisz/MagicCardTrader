# Generated by Django 2.2.7 on 2020-07-27 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Magic', '0004_auto_20200712_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_name', models.CharField(max_length=150)),
                ('set_name', models.CharField(max_length=150)),
                ('price', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='Magic.User')),
            ],
        ),
        migrations.DeleteModel(
            name='CardsForSale',
        ),
    ]
