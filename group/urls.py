from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('',views.gcGroups,name='gcGroups'),
    path('createGroupApi/',views.createGroupApi,name='createGroupApi'),
    path('groupInfoApi/',views.groupInfo,name='groupInfoApi'),
    path('assignCampaigns/',views.assignCampaigns,name='assignCampaignsApi'),
    path('removeCampaigns/',views.removeCampaigns,name='removeCampaigns'),
    path('assignMembers/',views.assignMembers,name='assignMembers'),
    path('removeMembers/',views.removeMembers,name='removeMembers'),
   ]