# Generated by Django 2.1.5 on 2019-08-05 12:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device_group', '0014_auto_20190805_1758'),
        ('campaign', '0062_auto_20190802_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule_campaign',
            name='device_group',
        ),
        migrations.AddField(
            model_name='schedule_campaign',
            name='device_group_campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='device_group.Device_Group_Campaign'),
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 5, 17, 58, 56, 507340)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 5, 17, 58, 56, 491333)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 5, 17, 58, 56, 507340)),
        ),
    ]