# Generated by Django 3.2.8 on 2021-10-29 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gameon', '0004_auto_20211029_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_review',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_rating',
            field=models.IntegerField(default=0),
        ),
    ]
