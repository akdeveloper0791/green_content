from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('upload_camp_web/', views.upload_camp_web, name='upload_camp_web'),
    path('init/',views.initCampaignUpload, name='initCampaignUpload'),
    path('list_camp_web/', views.listCampaignsWeb, name='listCampaignsWeb'),
    path('list_my_campaigns/', views.listMyCampaignsAPI, name='listMyCampaignsAPI'),
]