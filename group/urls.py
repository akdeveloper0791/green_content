from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('groups',views.gcGroups,name='gcGroups'),
    path('',views.gcGroups,name='gcGroups'),
    path('createGroupApi/',views.createGroupApi,name='createGroupApi'),
    path('groupInfoApi/',views.groupInfo,name='groupInfoApi'),
    path('assignCampaigns/',views.assignCampaigns,name='assignCampaignsApi'),
    path('removeCampaigns/',views.removeCampaigns,name='removeCampaigns'),
    path('assignMembers/',views.assignMembers,name='assignMembers'),
    path('removeMembers/',views.removeMembers,name='removeMembers'),
    path('getAssignedGroups/',views.getAssignedGroups,name='getAssignedGroups'),
    path('updateMemberGroupStatus/',views.updateMemberGroupStatus,name='updateMemberGroupStatus'),
    path('getMemberGroupCampaigns/',views.getMemberGroupCampaigns,name='getMemberGroupCampaigns'),
    path('approveGroupCampaign/',views.approveGroupCampaign,name='approveGroupCampaign'),
    path('approve/<int:gId>', views.approveFromMemer, name='approveFromMemer'),
    path('assignPlayers/',views.assignPlayersGCGroup,name='assignPlayersGCGroup'),
    path('removePlayers/',views.removePlayersGCGroup,name='removePlayersGCGroup'),

   ]