# Generated by Django 2.0.9 on 2019-03-16 09:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0023_auto_20190316_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 14, 38, 14, 69306)),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 16, 14, 38, 14, 69306)),
        ),
    ]
