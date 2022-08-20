from django.contrib import admin

# Register your models here.

from SmartHome.models import Client, BoardType, ConfiguredModule, Dashboard, GPIOPinConfig, AvailableModule

admin.site.register(BoardType)
admin.site.register(Client)
admin.site.register(AvailableModule)
admin.site.register(ConfiguredModule)
admin.site.register(GPIOPinConfig)
admin.site.register(Dashboard)
