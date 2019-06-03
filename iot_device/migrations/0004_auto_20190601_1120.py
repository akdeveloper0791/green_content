# Generated by Django 2.1.5 on 2019-06-01 05:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('iot_device', '0003_iot_device_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='iot_device',
            name='registered_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='iot_device',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
