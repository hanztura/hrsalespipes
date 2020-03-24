from django.contrib import admin

from .forms import StatusModelForm
from .models import Status


class StatusAdmin(admin.ModelAdmin):
    form = StatusModelForm
    fields = [
        'name',
        'probability',
        'job_status',
    ]
    list_display = ('name', 'probability', 'job_status')


admin.site.register(Status, StatusAdmin)
