# Generated by Django 2.0.9 on 2019-03-22 05:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0034_auto_20190321_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 22, 11, 25, 59, 159969)),
        ),
    ]
