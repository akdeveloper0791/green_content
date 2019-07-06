from django.urls import path
from . import views

urlpatterns = [
    #url(r'^first/',csrf_exempt(views.first),name='first'),
    path('rules',views.contextualAdsRules,name='contextualAdsRules'),
    path('register',views.register,name='iotDeviceRegister'),
    path('createRule',views.createRule,name="createContextualAdsRule"),
    path('deleteRule',views.deleteRule,name="deleteContextualAdsRule"),
    path('assignCampaignsToRule',views.assignCampaignsToCARule,name="assignCampaignsToCARule"),
    path('removeCampaignsFromRule',views.removeCampaignsFromCARule,name="removeCampaignsFromCARule"),
    path('assignDevicesToRule',views.assignDevicesToRule,name="assignDevicesToRule"),
    path('removeDevicesFromRule',views.removeDevicesFromRule,name="removeDevicesFromRule"),
    path('getCARules',views.getCARules,name="getIOTDeviceCARules"),
    path('getCARuleInfo',views.getCARuleInfo,name="getIOTDeviceCARuleInfo"),
    path('metrics',views.metrics,name='iotDeviceMetrics'),
    path('viewer_metrics',views.viewerMetrics,name="iotViewerMetrics"),
    path('get_v_metrics',views.getViewerMetrics,name="getIOTViewerMetrics"),
    path('exportViewerMetrics/',views.exportViewerMetrics, name="exportIOTViewerMetrics"),
    path('broadCastMicPhoneRule/',views.broadCastMicPhoneRule, name="broadCastMicPhoneRule"),
    path('micPhoneClassifiers/',views.micPhoneClassifiers, name="micPhoneClassifiers"),
    path('vm_bar_reports',views.getViewerBarMetrics,name="getViewerBarMetrics"),
    path('vm_gender_pie_reports',views.vmGenderPieReports,name="vmGenderPieReports"),
    ]