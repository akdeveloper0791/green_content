# Generated by Django 2.0.9 on 2019-03-19 05:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0042_multiple_campaign_upload_save_path'),
        ('player', '0014_auto_20190319_1052'),
        ('campaign', '0025_auto_20190316_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player_Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 3, 19, 10, 52, 5, 908723))),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.Multiple_campaign_upload')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 19, 10, 52, 5, 907724)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 19, 10, 52, 5, 906725)),
        ),
        migrations.AlterUniqueTogether(
            name='player_campaign',
            unique_together={('player', 'campaign')},
        ),
    ]