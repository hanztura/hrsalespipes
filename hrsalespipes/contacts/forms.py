from django.forms import ModelForm
from django.contrib.postgres.forms import JSONField

from .models import Candidate, Client, Supplier
from .utils import FormCleanContactNumber


class ContactCreateModelForm(FormCleanContactNumber, ModelForm):

    class Meta:
        model = Candidate
        fields = [
            'name',
            'contact_number',
            'whatsapp_link',
            'email_address',
            'location',
        ]


class CandidateCreateModelForm(ContactCreateModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

    def is_valid(self):
        """Set default candidate owner"""
        is_valid = super().is_valid()

        if is_valid:
            employee = getattr(self.user, 'as_employee', None)
            print(employee)
            self.instance.candidate_owner = employee

        return is_valid


class CandidateUpdateModelForm(ContactCreateModelForm):

    class Meta:
        model = Candidate
        fields = [
            'name',
            'code',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'whatsapp_link',
            'skype_id',
            'ms_teams_id',
            'location',

            'current_previous_position',
            'current_previous_company',
            'current_previous_salary',
            'current_previous_benefits',
            'motivation_for_leaving',
            'expected_salary',
            'expected_benefits',

            'nationality',
            'languages',
            'preferred_location',
            'civil_status',
            'dependents',
            'gender',
            'highest_educational_qualification',
            'date_of_birth',

            'visa_status',
            'availability_for_interview',
            'notice_period',
            'candidate_owner',
            'cv_template',
            'notes',

            # medical
            'is_medical',
            'medical_experience_in_years',
            'specialization',
            'other_certifications',
            'bls_validity',
            'acls_validity',
            'haad_dha_license_type',
            'haad_dha_license_validity',
            'job_title_on_dha_haad',
            'dataflow_last_update',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['candidate_owner'].required = True


class ClientUpdateModelForm(FormCleanContactNumber, ModelForm):
    class Meta:
        model = Client
        fields = [
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'whatsapp_link',
            'skype_id',
            'ms_teams_id',

            'industry',
            'location',
            'initial_approach',
            'meeting_arranged',
            'agreement_term',
            'agreement_fee',
            'refund_scheme',
            'validity',
            'point_of_contacts'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['industry'].required = True


class ClientCreateModelForm(FormCleanContactNumber, ModelForm):

    class Meta:
        model = Client
        fields = [
            'name',
            'contact_number',
            'whatsapp_link',
            'email_address',
            'location',
            'industry'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['industry'].required = True


class SupplierModelForm(FormCleanContactNumber, ModelForm):

    class Meta:
        model = Supplier
        fields = [
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'whatsapp_link',
            'skype_id',
            'ms_teams_id',
            'location',
            'point_of_contacts',
            'notes',
        ]
