# Generated by Django 2.1.5 on 2019-08-02 06:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190530_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forgotpwdsession',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 2, 12, 17, 28, 691803)),
        ),
    ]
