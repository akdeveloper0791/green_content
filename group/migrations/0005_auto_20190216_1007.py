# Generated by Django 2.0.9 on 2019-02-16 04:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_groupcampaigns_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 16, 10, 7, 29, 449630)),
        ),
    ]
