# Generated by Django 2.0.9 on 2019-03-21 10:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0033_auto_20190321_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 21, 15, 55, 32, 25478)),
        ),
    ]
