from django.urls import path
from . import views

urlpatterns = [ 
path('register',views.licenseRegister,name='licenseRegister'),
]