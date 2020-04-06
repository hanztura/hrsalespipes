from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Status, JobStatus, Job, JobCandidate
from system.helpers import register_optional_admin_items


class JobResource(resources.ModelResource):
    class Meta:
        model = Job
        fields = (
            'id',
            'reference_number',
            'date',
            'client',
            'position',
            'location',
            'potential_income',
            'status',
        )


class JobAdmin(
        ImportExportModelAdmin,
        SimpleHistoryAdmin):
    resource_class = JobResource
    readonly_fields = JobResource.Meta.fields


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
        'id',
        'order',
        'name',
        'is_job_open',
        'is_default')


admin.site.register(Status, StatusAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
admin.site.register(Job, JobAdmin)

# only enable import export if allowed
# register_optional_admin_items(((Job, JobAdmin), ))
