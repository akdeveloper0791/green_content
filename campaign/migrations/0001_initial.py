# Generated by Django 2.0.9 on 2019-02-01 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cmsapp', '0040_auto_20190201_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField()),
                ('campaign_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.Multiple_campaign_upload', unique=True)),
            ],
        ),
    ]
