# Generated by Django 2.0.9 on 2019-03-16 09:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0029_auto_20190316_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 14, 38, 14, 73304)),
        ),
    ]