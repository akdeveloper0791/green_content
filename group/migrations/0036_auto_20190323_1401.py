# Generated by Django 2.0.9 on 2019-03-23 08:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0035_auto_20190322_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 1, 37, 748468)),
        ),
    ]