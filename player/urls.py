from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('register',views.register,name='register'),
    path('metrics',views.metrics,name='metrics'),
    
    ]