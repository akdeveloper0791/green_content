# Generated by Django 2.0.9 on 2019-03-23 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0034_auto_20190323_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 31, 13, 14703)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 31, 13, 14703)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 31, 13, 14703)),
        ),
    ]
