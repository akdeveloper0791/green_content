# Generated by Django 2.0.9 on 2019-02-16 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0040_auto_20190201_1030'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiple_campaign_upload',
            name='source',
            field=models.SmallIntegerField(default=0),
        ),
    ]