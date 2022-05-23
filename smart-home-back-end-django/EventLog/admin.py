from django.contrib import admin
from EventLog.models import Event


class EventAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('id', 'type', 'additional_data')
    search_fields = ('additional_data', 'type')


admin.site.register(Event, EventAdmin)
