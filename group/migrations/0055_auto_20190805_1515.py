# Generated by Django 2.2 on 2019-08-05 09:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0054_auto_20190802_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 5, 15, 15, 27, 409318)),
        ),
    ]
