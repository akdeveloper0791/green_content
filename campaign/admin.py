from django.contrib import admin
from .models import CampaignInfo,Deleted_Campaigns,Approved_Group_Campaigns

# Register your models here.
admin.site.register(CampaignInfo)
admin.site.register(Deleted_Campaigns)
admin.site.register(Approved_Group_Campaigns)
