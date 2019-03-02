# Generated by Django 2.0.9 on 2019-03-02 11:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0011_auto_20190302_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaigninfo',
            name='id',
        ),
        migrations.AlterField(
            model_name='approved_group_campaigns',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 2, 17, 16, 29, 388110)),
        ),
        migrations.AlterField(
            model_name='campaigninfo',
            name='campaign_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='cmsapp.Multiple_campaign_upload'),
        ),
        migrations.AlterField(
            model_name='deleted_campaigns',
            name='deleted_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 2, 17, 16, 29, 388110)),
        ),
    ]
