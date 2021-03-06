# Generated by Django 2.0.9 on 2019-02-20 14:18

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0013_auto_20190220_1948'),
        ('cmsapp', '0042_multiple_campaign_upload_save_path'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign', '0006_auto_20190220_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 20, 19, 48, 11, 2424)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 20, 19, 48, 11, 2424)),
        ),
        migrations.AlterUniqueTogether(
            name='approved_group_campaigns',
            unique_together={('user', 'campaign', 'group', 'group_campaign')},
        ),
    ]
