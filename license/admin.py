from django.contrib import admin
from .models import License_Device

# Register your models here.
class License_DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'status', 'expiry_date', 'registered_date');
    search_fields = ('mac',)
    #search_fields = ("mac");
    #list_per_page = 25;

admin.site.register(License_Device,License_DeviceAdmin);
