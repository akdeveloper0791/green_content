from django.contrib import admin
from .models import GcGroups, GcGroupMembers, GroupCampaigns

# Register your models here.
admin.site.register(GcGroups)
admin.site.register(GcGroupMembers)
admin.site.register(GroupCampaigns)