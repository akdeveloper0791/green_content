# Generated by Django 2.0.9 on 2019-03-21 10:25

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0042_multiple_campaign_upload_save_path'),
        ('player', '0016_auto_20190321_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign_Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(max_length=50)),
                ('times_played', models.SmallIntegerField(default=1)),
                ('duration', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 3, 21, 15, 55, 31, 992499))),
                ('campaign', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='cmsapp.Multiple_campaign_upload')),
            ],
        ),
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 21, 15, 55, 31, 986500)),
        ),
        migrations.AlterField(
            model_name='last_seen_metrics',
            name='accessed_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 21, 15, 55, 31, 988498)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 21, 15, 55, 31, 981533)),
        ),
        migrations.AddField(
            model_name='campaign_reports',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player'),
        ),
    ]
