from django.contrib import admin
from .models import Event, Report


# Register your models here.
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
