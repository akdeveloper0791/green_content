from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('create/',views.create,name='create'),
    path('assignPlayers/',views.assignPlayers,name="assignPlayers"),
    path('removePlayers/',views.removePlayers,name="removePlayers"),
    ]