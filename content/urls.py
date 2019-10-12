from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('initUpload',views.initContentUpload,name='initContentUpload'),
    path('uploadContentResource/',views.uploadContentResource,name='uploadContentResource'),
    path('mycontent/',views.mycontent,name='mycontent'),
    path('mycontent/<int:pageNumber>',views.listMyContent,name='listMyContent'),
    path('mycontent_api/',views.listMyContentAPI,name='mycontentAPI'),
    path('preview/<int:contentId>',views.preview,name="previewContent"),
    path('delete',views.delete,name='deleteContent'),
    path('list_pending_approval/<int:approveType>',views.listPendingApprovals,name='listPendingApprovalsContent'),
    path('approve',views.approve,name='approveContent'),
    path('search',views.search,name='searchContent'),
    ]