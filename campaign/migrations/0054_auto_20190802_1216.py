# Generated by Django 2.1.5 on 2019-08-02 06:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device_group', '0008_auto_20190802_1216'),
        ('campaign', '0053_auto_20190802_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule_campaign',
            name='device_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='device_group.Device_Group'),
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 16, 33, 923014)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 16, 33, 907006)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 16, 33, 924018)),
        ),
        migrations.AlterField(
            model_name='schedule_campaign',
            name='player_campaign',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='campaign.Player_Campaign'),
        ),
    ]
