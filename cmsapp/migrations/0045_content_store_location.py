# Generated by Django 2.1.5 on 2019-09-06 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0044_content_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='store_location',
            field=models.SmallIntegerField(default=2),
        ),
    ]
