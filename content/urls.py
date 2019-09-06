from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('initUpload',views.initContentUpload,name='initContentUpload'),
    path('uploadContentResource/',views.uploadContentResource,name='uploadContentResource'),
    ]