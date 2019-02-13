from django.db import models
from django.conf import settings

# Create your models here.
class GcGroups(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=20,blank=False,null=False)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    
    class Meta(object):
        unique_together = [
        ['user', 'name']
        ]

class GcGroupMembers(models.Model):
    gc_group = models.ForeignKey('group.GcGroups',on_delete=models.CASCADE)
    member = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=1)

    class Meta(object):
        unique_together= [
        ['gc_group','member']
        ]

class GroupCampaigns(models.Model):
    gc_group = models.ForeignKey('group.GcGroups',on_delete=models.CASCADE)
    campaign = models.ForeignKey('cmsapp.Multiple_campaign_upload',on_delete=models.CASCADE)

    class Meta(object):
        unique_together=[
        ['gc_group','campaign']
        ]