from django.contrib import admin

from .models import Status


class StatusAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'probability',
        'job_status',
    ]
    list_display = ('name', 'probability')


admin.site.register(Status, StatusAdmin)
