# Generated by Django 5.0.1 on 2024-01-21 18:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemesis', '0003_alter_player_last_online_alter_session_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_online',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 21, 18, 19, 58, 213578, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 1, 21, 18, 19, 58, 213578, tzinfo=datetime.timezone.utc)),
        ),
    ]
