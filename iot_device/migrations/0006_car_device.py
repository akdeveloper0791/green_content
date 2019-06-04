# Generated by Django 2.1.5 on 2019-06-01 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0035_auto_20190601_1224'),
        ('iot_device', '0005_auto_20190601_1219'),
    ]

    operations = [
        migrations.CreateModel(
            name='CAR_Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iot_device.Contextual_Ads_Rule')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
        ),
    ]