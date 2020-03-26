from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Employee, CVTemplate, Client, Supplier, Candidate


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee
        fields = (
            'id',
            'code',
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'user',
        )


class EmployeeAdmin(ImportExportModelAdmin):
    resource_class = EmployeeResource


class ClientResource(resources.ModelResource):
    class Meta:
        model = Client
        fields = (
            'id',
            'code',
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'industry',
            'initial_approach',
            'meeting_arranged',
            'agreement_terms',
            'agreement_fee',
            'refund_scheme',
            'validity',
        )


class ClientAdmin(ImportExportModelAdmin):
    resource_class = ClientResource


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        fields = (
            'id',
            'code',
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
        )


class SupplierAdmin(ImportExportModelAdmin):
    resource_class = SupplierResource


class CandidateResource(resources.ModelResource):
    class Meta:
        model = Candidate
        fields = (
            'id',
            'code',
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'skype_id',
            'ms_teams_id',
            'location',
            'current_previous_position',
            'current_previous_company',
            'current_previous_benefits',
            'current_previous_salary',
            'motivation_for_leaving',
            'expected_benefits',
            'expected_salary',
            'nationality',
            'languages',
            'preferred_location',
            'civil_status',
            'dependents',
            'gender',
            'highest_educational_qualification',
            'date_of_birth',
            'visa_status',
            'driving_license',
            'availability_for_interview',
            'notice_period',
            'candidate_owner',
            'cv_template',
        )


class CandidateAdmin(ImportExportModelAdmin):
    resource_class = CandidateResource


class CVTemplateAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'template',
        'is_default'
    ]
    list_display = ('name', 'is_default')


admin.site.register(CVTemplate, CVTemplateAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Candidate, CandidateAdmin)
