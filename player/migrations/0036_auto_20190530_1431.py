# Generated by Django 2.2 on 2019-05-30 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0035_merge_20190517_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 14, 31, 50, 509354)),
        ),
        migrations.AlterField(
            model_name='campaign_reports',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 14, 31, 50, 509354)),
        ),
        migrations.AlterField(
            model_name='last_seen_metrics',
            name='accessed_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 14, 31, 50, 509354)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 14, 31, 50, 509354)),
        ),
    ]
