from django.contrib import admin
from .models import Player, Age_Geder_Metrics, Last_Seen_Metrics

# Register your models here.
admin.site.register(Player)
admin.site.register(Age_Geder_Metrics)
admin.site.register(Last_Seen_Metrics)
