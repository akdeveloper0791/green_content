# Generated by Django 2.2 on 2019-04-25 05:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190328_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpwdsession',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 25, 11, 25, 18, 400289)),
        ),
    ]
