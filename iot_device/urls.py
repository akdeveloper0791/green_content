from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('rules',views.contextualAdsRules,name='contextualAdsRules'),
    path('register',views.register,name='iotDeviceRegister'),
    path('createRule',views.createRule,name="createContextualAdsRule")
    ]