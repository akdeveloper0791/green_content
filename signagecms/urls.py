"""twitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from cmsapp import views
from django.urls import path



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signagecms/', include('cmsapp.urls')),
    
    url(r'^mycontent/upload/', views.upload, name='upload'),
    url(r'^upload_api/', views.upload_api, name='upload_api'),
    path('campaigns/',include('campaign.urls')),
    path('groups/',include('group.urls')),
    path('gdbx/',include('gdbx.urls')),
    path('player/',include('player.urls')),
    path('license/',include('license.urls')),
    path('device_group/',include('device_group.urls')),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^',include('cmsapp.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)



