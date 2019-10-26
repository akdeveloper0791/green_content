# Generated by Django 2.1.5 on 2019-09-05 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmsapp', '0043_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content_Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=125)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmsapp.Content')),
            ],
        ),
    ]