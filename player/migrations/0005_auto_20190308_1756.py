# Generated by Django 2.0.9 on 2019-03-08 12:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0004_auto_20190308_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='registered_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 8, 17, 56, 3, 881330)),
        ),
    ]
