# Generated by Django 2.1.5 on 2019-09-10 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_content_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 10, 12, 28, 7, 68883)),
        ),
    ]