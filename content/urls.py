from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('initUpload',views.initContentUpload,name='initContentUpload'),
    path('uploadContentResource/',views.uploadContentResource,name='uploadContentResource'),
    path('mycontent/',views.mycontent,name='mycontent'),
    path('mycontent/<int:pageNumber>',views.listMyContent,name='listMyContent'),
    path('preview/<int:contentId>',views.preview,name="previewContent"),
    path('delete',views.delete,name='deleteContent'),
    ]