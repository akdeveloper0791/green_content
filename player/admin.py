from django.contrib import admin
from .models import Player, Age_Geder_Metrics, Last_Seen_Metrics, Campaign_Reports

class PlayerAdmin(admin.ModelAdmin):
	list_display = ('mac', 'name');
	search_fields = ('mac','name',);

# Register your models here.
admin.site.register(Player,PlayerAdmin)
admin.site.register(Age_Geder_Metrics)
admin.site.register(Last_Seen_Metrics)
admin.site.register(Campaign_Reports)

