from django.contrib import admin

from import_export import resources
from import_export.admin import ExportMixin

from .models import User, Setting, VisaStatus, InterviewMode, Location


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'as_employee',
            'as_employee__name'
        )


class UserAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = UserResource


class VisaStatusResource(resources.ModelResource):
    class Meta:
        model = VisaStatus
        fields = (
            'id',
            'name'
        )


class VisaStatusAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = VisaStatusResource


# Register your models here
admin.site.register(User, UserAdmin)
admin.site.register(Setting)
admin.site.register(VisaStatus, VisaStatusAdmin)
admin.site.register(InterviewMode)
admin.site.register(Location)
