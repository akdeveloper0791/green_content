# Generated by Django 2.1.5 on 2019-08-02 06:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20190802_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpwdsession',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 18, 0, 993378)),
        ),
    ]
