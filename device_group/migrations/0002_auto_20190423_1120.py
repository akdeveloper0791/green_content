# Generated by Django 2.0.9 on 2019-04-23 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device_group', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_group_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 23, 11, 20, 5, 942306)),
        ),
    ]