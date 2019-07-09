from django.contrib import admin
from .models import IOT_Device,Contextual_Ads_Rule,CAR_Campaign,CAR_Device
from .models import Geder_Age_Metrics

# Register your models here.
admin.site.register(IOT_Device)
admin.site.register(Contextual_Ads_Rule)
admin.site.register(CAR_Campaign)
admin.site.register(CAR_Device)
admin.site.register(Geder_Age_Metrics)