# Generated by Django 2.0.9 on 2019-04-23 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0040_auto_20190328_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 23, 11, 20, 5, 934305)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 23, 11, 20, 5, 934305)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 23, 11, 20, 5, 935305)),
        ),
    ]
