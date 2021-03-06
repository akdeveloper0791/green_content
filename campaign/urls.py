from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('upload_camp_web/', views.upload_camp_web, name='upload_camp_web'),
    path('init/',views.initCampaignUpload, name='initCampaignUpload'),
    path('list_camp_web/', views.listCampaignsWeb, name='listCampaignsWeb'),
    path('list_my_campaigns/', views.listMyCampaignsAPI, name='listMyCampaignsAPI'),
    path('delete_campaign/', views.deleteMyCampaign, name='deleteMyCampaign'),
    path('removeApprovedCampaign/', views.removeApprovedCampaign, name='removeApprovedCampaign'),
    path('previewCampaign/<int:c_id>', views.previewCampaign, name='previewCampaign'),
    path('create/', views.create, name='create'),
    path('approve/<int:one>/<int:two>', views.approveCampaignNotif, name='approveCampaignNotif'),
    path('uploadCampaignResource/',views.uploadCampaignResource,name='uploadCampaignResource'),
    path('saveScheduleCampaign/',views.saveScheduleCampaign,name='saveScheduleCampaign'),
    path('deleteScheduleCampaign/',views.deleteScheduleCampaign,name='deleteScheduleCampaign'),
    path('editCampaign/',views.editCampaign,name='editCampaign'),
    path('getEditCampaignInfo/',views.getEditCampaignInfo,name='getEditCampaignInfo'),
    
    
]