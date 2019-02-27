from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('init/', views.getGDbxxx, name='getGDbxxx'),
]