# Generated by Django 2.0.9 on 2019-03-23 09:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0024_auto_20190323_1438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign_reports',
            name='campaign',
        ),
        migrations.AddField(
            model_name='campaign_reports',
            name='campaign_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 39, 21, 93218)),
        ),
        migrations.AlterField(
            model_name='campaign_reports',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 39, 21, 93218)),
        ),
        migrations.AlterField(
            model_name='last_seen_metrics',
            name='accessed_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 39, 21, 93218)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 39, 21, 93218)),
        ),
    ]