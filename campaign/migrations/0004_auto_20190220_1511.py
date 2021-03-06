# Generated by Django 2.0.9 on 2019-02-20 09:41

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0010_auto_20190220_1511'),
        ('campaign', '0003_auto_20190220_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='approved_group_campaigns',
            name='group_campaign',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='group.GroupCampaigns'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 20, 15, 11, 18, 40348)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 20, 15, 11, 18, 39348)),
        ),
    ]
