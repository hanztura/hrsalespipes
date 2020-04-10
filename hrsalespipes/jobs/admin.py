from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Status, JobStatus, Job, JobCandidate, Interview


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


class JobCandidateAdmin(SimpleHistoryAdmin):
    fields = [
        'id',
        'created',
        'modified',
        'pipeline',
        'job',
        'candidate',
        'registration_date',
        'status',
        'cv_source',
        'cv_date_shared',
        'remarks',
        'salary_offered_currency',
        'salary_offered',
        'tentative_date_of_joining',
        'associate',
        'consultant'
    ]
    readonly_fields = [
        'id',
        'created',
        'modified',
        'pipeline',
        'job',
        'candidate',
        'registration_date',
        'status',
        'cv_source',
        'cv_date_shared',
        'remarks',
        'salary_offered_currency',
        'salary_offered',
        'tentative_date_of_joining',
        'associate',
        'consultant'
    ]
    list_display = ['id', 'job', 'candidate', 'registration_date']


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


class InterviewResource(resources.ModelResource):
    class Meta:
        model = Interview
        fields = (
            'id',
            'created',
            'modified',
            'job_candidate',
            'mode',
            'date_time',
            'status',
            'done_by',
        )


class InterviewAdmin(
        ImportExportModelAdmin,
        SimpleHistoryAdmin):
    resource_class = InterviewResource
    readonly_fields = InterviewResource.Meta.fields
    list_display = (
        'id',
        'created',
        'modified',
    )


admin.site.register(Status, StatusAdmin)
admin.site.register(JobStatus, JobStatusAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobCandidate, JobCandidateAdmin)
admin.site.register(Interview, InterviewAdmin)

# only enable import export if allowed
# register_optional_admin_items(((Job, JobAdmin), ))
