# Generated by Django 2.0.9 on 2019-03-16 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0010_auto_20190316_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='location_desc',
            field=models.CharField(default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 13, 20, 1, 680882)),
        ),
        migrations.AlterField(
            model_name='auto_sync_metrics',
            name='accessed_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 13, 20, 1, 680882)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 13, 20, 1, 679882)),
        ),
    ]
