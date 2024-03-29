# Generated by Django 2.0.9 on 2019-03-23 08:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0018_auto_20190322_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 1, 37, 744472)),
        ),
        migrations.AlterField(
            model_name='campaign_reports',
            name='campaign',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, to='cmsapp.Multiple_campaign_upload'),
        ),
        migrations.AlterField(
            model_name='campaign_reports',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 1, 37, 744472)),
        ),
        migrations.AlterField(
            model_name='last_seen_metrics',
            name='accessed_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 1, 37, 744472)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 23, 14, 1, 37, 740488)),
        ),
    ]
