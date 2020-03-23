from django.contrib import admin

from .models import Employee, CVTemplate


class CVTemplateAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'template',
        'is_default'
    ]
    list_display = ('name', 'is_default')


admin.site.register(Employee)
admin.site.register(CVTemplate, CVTemplateAdmin)
