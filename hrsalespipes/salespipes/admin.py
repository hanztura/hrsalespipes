from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .forms import StatusModelForm
from .models import Status, Pipeline, Target


class StatusAdmin(admin.ModelAdmin):
    form = StatusModelForm
    fields = [
        'name',
        'probability',
        'should_have_invoice',
        'job_status',
    ]
    list_display = ('name', 'probability', 'should_have_invoice', 'job_status')


class TargetAdmin(admin.ModelAdmin):
    fields = ['date', 'amount', 'notes']
    list_display = ['id', 'date', 'amount', 'notes']


class PipelineAdmin(SimpleHistoryAdmin):
    fields = (
        'id',
        'created',
        'modified',
        'date',
        'job',
        'job_candidate',
        'recruitment_term',
        'recruitment_rate',
        'base_amount',
        'potential_income',
        'status',
        'invoice_date',
        'invoice_number',
        'invoice_amount',
        'vat'
    )
    readonly_fields = (
        'id',
        'created',
        'modified',
        'date',
        'job',
        'job_candidate',
        'recruitment_term',
        'recruitment_rate',
        'base_amount',
        'potential_income',
        'status',
        'invoice_date',
        'invoice_number',
        'invoice_amount',
        'vat'
    )
    list_display = ('id', 'date', 'job_candidate')


admin.site.register(Status, StatusAdmin)
admin.site.register(Pipeline, PipelineAdmin)
admin.site.register(Target, TargetAdmin)
