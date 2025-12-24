from django.contrib import admin
from .models import Event, Alert


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "source_name", "event_type", "severity", "timestamp")
    list_filter = ("event_type", "severity")
    search_fields = ("source_name", "description")


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "status", "created_at")
    list_filter = ("status",)
