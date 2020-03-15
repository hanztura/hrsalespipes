from django.contrib import admin

from .models import Status, Board


class StatusAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'probability',
        'should_create_pipeline',
    ]
    list_display = ('name', 'probability', 'should_create_pipeline')


admin.site.register(Status, StatusAdmin)
admin.site.register(Board)
