# Generated by Django 2.1.5 on 2019-08-16 05:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0041_auto_20190816_1116'),
        ('group', '0054_auto_20190802_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('gc_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.GcGroups')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
        ),
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 16, 11, 16, 42, 905724)),
        ),
    ]