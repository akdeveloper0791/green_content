# Generated by Django 2.0.9 on 2019-03-02 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0017_auto_20190302_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 2, 17, 16, 29, 392124)),
        ),
    ]
