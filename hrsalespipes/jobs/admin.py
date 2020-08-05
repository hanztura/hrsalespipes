from django.contrib import admin, messages

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Status, JobStatus, Job, JobCandidate, Interview


def make_change_job_status(status):
    def change_job_status(modeladmin, request, queryset):
        queryset.update(status=status)
        messages.info(request, 'Updated {} Job status to {}'.format(
            queryset.count(),
            status.name))

    change_job_status.short_description = 'Change Job Status to {}'.format(
        status.name)
    change_job_status.__name__ = 'change_job_status_{}'.format(status.pk)
    change_job_status.allowed_permissions = ('change',)
    return change_job_status


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
            'number_of_positions',
            'status',
            'assigned_recruiters'
        )


class JobAdmin(
        ImportExportModelAdmin,
        SimpleHistoryAdmin):
    resource_class = JobResource
    # readonly_fields = JobResource.Meta.fields
    list_display = [
        'id',
        'reference_number',
        'date',
        'position',
        'client',
        'status',
    ]
    fields = (
        'reference_number',
        'date',
        'client',
        'position',
        'location',
        'potential_income',
        'number_of_positions',
        'status',
        'assigned_recruiters'
    )
    search_fields = [
        'reference_number',
        'position'
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)

        for status in JobStatus.objects.all():
            action = make_change_job_status(status)
            actions[action.__name__] = (action,
                                        action.__name__,
                                        action.short_description)

        return actions


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
