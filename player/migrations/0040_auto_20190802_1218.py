# Generated by Django 2.1.5 on 2019-08-02 06:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0039_auto_20190802_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 18, 24, 55077)),
        ),
        migrations.AlterField(
            model_name='campaign_reports',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 18, 24, 56076)),
        ),
        migrations.AlterField(
            model_name='last_seen_metrics',
            name='accessed_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 18, 24, 56076)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 18, 24, 53078)),
        ),
    ]
