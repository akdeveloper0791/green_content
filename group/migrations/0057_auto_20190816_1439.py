# Generated by Django 2.1.5 on 2019-08-16 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0043_auto_20190816_1439'),
        ('group', '0056_auto_20190816_1431'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='G_Player',
            new_name='Player',
        ),
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 16, 14, 38, 58, 916431)),
        ),
    ]
