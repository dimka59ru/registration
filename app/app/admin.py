from django.contrib import admin
from .models import Project, Devices


class ProjectAdmin(admin.ModelAdmin):
    # fields = ('status', 'end_date')
    list_display = (
    'status', 'add_date', 'end_date', 'realization', 'partner', 'end_customer', 'email', 'contacts', 'file', 'note')


class DevicesAdmin(admin.ModelAdmin):
    list_display = ('device_name',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Devices, DevicesAdmin)
