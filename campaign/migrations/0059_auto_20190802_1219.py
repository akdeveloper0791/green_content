# Generated by Django 2.1.5 on 2019-08-02 06:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0058_auto_20190802_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule_campaign',
            name='device_group',
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 19, 3, 693649)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 19, 3, 677654)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 19, 3, 694653)),
        ),
    ]