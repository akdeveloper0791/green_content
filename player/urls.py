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
    path('device_mgmt_players',views.deviceMgmtPlayers,name="deviceMgmtPlayers"),
    path('campaigns/', views.groupCampaingsInfo, name='groupCampaingsInfo'),
    path('assignCampaigns/', views.assignCampaigns, name='assignCampaigns'),
    path('removeCampaigns/',views.removeCampaigns, name='removeCampaigns'),
    path('skipCampaigns/',views.skipCampaigns, name='skipCampaigns'),
    path('getPlayerCampaigns/',views.getPlayerCampaigns, name='getPlayerCampaigns'),
    path('getSchedulePlayerCampaigns/',views.getSchedulePlayerCampaigns, name='getSchedulePlayerCampaigns'),
    path('getDSPCampaigns/',views.getDSPCampaigns, name='getDSPCampaigns'),
    path('saveCampaignReports/',views.saveCampaignReports, name="saveCampaignReports"),
    path('getCampaignReports/',views.getCampaignReports, name="getCampaignReports"),
    path('campaign_reports',views.campaignReports,name="campaignReports"),
   
    path('exportCampaignReports/',views.exportCampaignReports, name="exportCampaignReports"),
    path('exportViewerMetrics/',views.exportViewerMetrics, name="exportViewerMetrics"),
    path('prepareViewerMetricsExcel/',views.prepareViewerMetricsExcel,name="prepareViewerMetricsExcel"),
    path('emailCampaignReports',views.emailCampaignReports,name='emailCampaignReports'),
    path('player_group',views.playerGroup,name="playerGroup"),
    path('listPlayersToPublishCamp/',views.listPlayersToPublishCamp,name="listPlayersToPublishCamp"),
    path('assignCampaignsToPlayer/',views.assignCampaignsToPlayer,name="assignCampaignsToPlayer"),
    path('schedule_campaign/<int:player>/<int:campaign>',views.scheduleCampaign,name="scheduleCampaign"),
    path('getCARules/',views.getCARules, name='getPlayerCARules'),
    path('getPlayers/',views.getPlayers, name='getPlayers'),
    ]