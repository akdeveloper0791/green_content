# Generated by Django 2.0.9 on 2019-03-28 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0043_auto_20190323_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupcampaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 14, 30, 22, 494870)),
        ),
    ]