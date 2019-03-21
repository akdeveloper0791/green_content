# Generated by Django 2.0.9 on 2019-03-19 05:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmsapp', '0042_multiple_campaign_upload_save_path'),
        ('player', '0015_auto_20190319_1107'),
        ('campaign', '0026_auto_20190319_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='player_campaign',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 19, 11, 7, 4, 511367)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 19, 11, 7, 4, 510367)),
        ),
        migrations.AlterField(
            model_name='player_campaign',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 19, 11, 7, 4, 511367)),
        ),
        migrations.AlterUniqueTogether(
            name='player_campaign',
            unique_together={('user', 'player', 'campaign')},
        ),
    ]