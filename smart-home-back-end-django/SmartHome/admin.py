from django.contrib import admin

# Register your models here.

from SmartHome.models import Client, BoardType, Sensor, Dashboard

admin.site.register(Client)
admin.site.register(BoardType)
admin.site.register(Sensor)
admin.site.register(Dashboard)
