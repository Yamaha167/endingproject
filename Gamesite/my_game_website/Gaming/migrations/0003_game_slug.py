# Generated by Django 5.0.4 on 2024-04-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gaming', '0002_game_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]
