# Generated by Django 2.0.9 on 2019-03-07 07:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0019_auto_20190305_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 7, 12, 57, 21, 478429)),
        ),
    ]
