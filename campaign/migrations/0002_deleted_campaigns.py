# Generated by Django 2.0.9 on 2019-02-18 09:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deleted_Campaigns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(max_length=50)),
                ('mac', models.CharField(max_length=50)),
                ('deleted_at', models.DateTimeField(default=datetime.datetime(2019, 2, 18, 14, 58, 53, 663988))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
