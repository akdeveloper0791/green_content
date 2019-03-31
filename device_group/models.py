from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Device_Group(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=False,null=False)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    class Meta(object):
        unique_together = [
        ['user', 'name']
        ] 

class Device_Group_Player(models.Model):
    device_group = models.ForeignKey('device_group.Device_Group',on_delete=models.CASCADE)
    player = models.ForeignKey('player.Player',on_delete=models.CASCADE)
    
    class Meta(object):
        unique_together= [
        ['device_group','player']
        ]

class Device_Group_Campaign(models.Model):
    device_group = models.ForeignKey('device_group.Device_Group',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now())

    class Meta(object):
        unique_together=[
        ['device_group','campaign']
        ]
