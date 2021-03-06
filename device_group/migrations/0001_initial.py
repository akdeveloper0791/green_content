# Generated by Django 2.0.9 on 2019-03-31 09:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0030_auto_20190331_1438'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmsapp', '0042_multiple_campaign_upload_save_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Device_Group_Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 3, 31, 14, 38, 47, 800211))),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.Multiple_campaign_upload')),
                ('device_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device_group.Device_Group')),
            ],
        ),
        migrations.CreateModel(
            name='Device_Group_Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device_group.Device_Group')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='device_group_player',
            unique_together={('device_group', 'player')},
        ),
        migrations.AlterUniqueTogether(
            name='device_group_campaign',
            unique_together={('device_group', 'campaign')},
        ),
        migrations.AlterUniqueTogether(
            name='device_group',
            unique_together={('user', 'name')},
        ),
    ]
