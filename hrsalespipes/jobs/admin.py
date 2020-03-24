from django.contrib import admin

from .models import Status, JobStatus


class StatusAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'probability',
        'should_create_pipeline',
    ]
    list_display = ('name', 'probability', 'should_create_pipeline')


class JobStatusAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'is_job_open',
        'is_default',
        'order',
    ]
    list_display = (
        'order',
        'name',
        'is_job_open',
        'is_default')


admin.site.register(Status, StatusAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
