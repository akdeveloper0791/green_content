# Generated by Django 2.0.9 on 2019-03-28 09:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0039_auto_20190328_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 14, 51, 58, 295165)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 14, 51, 58, 294166)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 14, 51, 58, 296161)),
        ),
    ]
