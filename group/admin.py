from django.contrib import admin
from .models import GcGroups, GcGroupMembers, GroupCampaigns, GroupMemberAssignNotification
from .models import GroupCampaignAssignNotification
from .models import Player
# Register your models here.
admin.site.register(GcGroups)
admin.site.register(GcGroupMembers)
admin.site.register(GroupCampaigns)
admin.site.register(GroupMemberAssignNotification)
admin.site.register(GroupCampaignAssignNotification)
admin.site.register(Player)