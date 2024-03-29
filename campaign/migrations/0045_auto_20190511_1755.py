# Generated by Django 2.2 on 2019-05-11 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0044_merge_20190511_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule_campaign',
            name='schedule_type',
            field=models.SmallIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 17, 55, 55, 929621)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 17, 55, 55, 928624)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 11, 17, 55, 55, 930622)),
        ),
    ]
