# Generated by Django 2.0.9 on 2019-02-18 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0041_multiple_campaign_upload_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='multiple_campaign_upload',
            name='save_path',
            field=models.TextField(default=''),
        ),
    ]
