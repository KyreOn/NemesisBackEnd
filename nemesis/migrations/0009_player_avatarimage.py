# Generated by Django 5.0.1 on 2024-01-22 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemesis', '0008_rename_desc_player_gamecount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='avatarImage',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
