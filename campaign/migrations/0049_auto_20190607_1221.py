# Generated by Django 2.1.5 on 2019-06-07 06:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0048_auto_20190529_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_campaign',
            name='is_skip',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 7, 12, 21, 0, 540549)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 7, 12, 21, 0, 524901)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 7, 12, 21, 0, 540549)),
        ),
    ]
