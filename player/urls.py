from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('register',views.register,name='register'),
    path('metrics',views.metrics,name='metrics'),
    path('refresh_fcm_api',views.refreshFCM,name='refreshFCM'),
    path('viewer_metrics',views.viewerMetrics,name="viewerMetrics"),
    path('get_v_metrics',views.getViewerMetrics,name="getViewerMetrics"),
    path('device_mgmt',views.deviceMgmt,name="deviceMgmt"),
    path('campaigns/', views.groupCampaingsInfo, name='groupCampaingsInfo'),
    path('assignCampaigns/', views.assignCampaigns, name='assignCampaigns'),
    path('removeCampaigns/',views.removeCampaigns, name='removeCampaigns'),
    path('getPlayerCampaigns/',views.getPlayerCampaigns, name='getPlayerCampaigns'),
    path('saveCampaignReports/',views.saveCampaignReports, name="saveCampaignReports"),
    path('getCampaignReports/',views.getCampaignReports, name="getCampaignReports"),
    path('campaign_reports',views.campaignReports,name="campaignReports"),
    path('player_group',views.playerGroup,name="playerGroup"),
    ]