# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-11 06:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmsapp', '0016_auto_20181001_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='My_gc_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagged_name', models.CharField(max_length=20)),
                ('tagged_email', models.EmailField(max_length=254)),
                ('tagged_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
