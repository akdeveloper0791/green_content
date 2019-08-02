from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('create/',views.createDG,name='createDG'),
    path('assignPlayers/',views.assignPlayersDG,name="assignPlayersDG"),
    path('removePlayers/',views.removePlayersDG,name="removePlayersDG"),
    path('assignCampaigns/',views.assignCampaignsDG,name="assignCampaignsDG"),
    path('removeCampaigns/',views.removeCampaignsDG,name="removeCampaignsDG"),
    path('',views.deviceGroups,name='deviceGroups'),
    ]