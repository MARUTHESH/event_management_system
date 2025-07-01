from django.contrib import admin
from events.models import (Event, EventRegistration)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'start_time', 'end_time', 'max_capacity')
    list_filter = ('start_time', 'end_time', 'max_capacity')
    search_fields = ('name', 'location')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee_name', 'attendee_email')
    list_filter = ('event',)
    search_fields = ('attendee_name', 'attendee_email')