# Generated by Django 2.0.13 on 2019-03-13 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_auto_20190312_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='age_geder_metrics',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 13, 12, 11, 18, 825153)),
        ),
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 13, 12, 11, 18, 809528)),
        ),
    ]
