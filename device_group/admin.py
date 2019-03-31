from django.contrib import admin
from .models import Device_Group,Device_Group_Player,Device_Group_Campaign

# Register your models here.
admin.site.register(Device_Group)
admin.site.register(Device_Group_Player)
admin.site.register(Device_Group_Campaign)
