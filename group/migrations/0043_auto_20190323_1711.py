# Generated by Django 2.0.9 on 2019-03-23 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0042_auto_20190323_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 17, 10, 54, 615142)),
        ),
    ]
