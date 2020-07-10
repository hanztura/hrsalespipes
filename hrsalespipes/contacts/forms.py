from django.contrib import messages
from django.forms import ModelForm, BooleanField

from .models import Candidate, Client, Supplier, CVTemplate
from .utils import FormCleanContactNumber

default_contact_model = Candidate
default_contact_fields = [
    'name',
    'contact_number',
    'whatsapp_link',
    'email_address',
    'location',
    'website'
]


class ContactCreateModelForm(FormCleanContactNumber, ModelForm):
    has_confirmed = BooleanField(initial=False, required=False)
    need_to_confirm = False

    class Meta:
        model = default_contact_model
        fields = default_contact_fields

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs.keys():
            self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        # if name exists make user confirm
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        has_confirmed = cleaned_data['has_confirmed']
        self.need_to_confirm = False

        contacts = self.Meta.model.objects.filter(name__iexact=name)
        if contacts.exists():
            if not has_confirmed:
                msg = 'A contact with name "{}"\
                    already exists. Please confirm to continue'
                msg = msg.format(name)
                self.add_error('has_confirmed', msg)
                self.need_to_confirm = True
                if hasattr(self, 'request'):
                    messages.warning(self.request, msg)

        return cleaned_data


class ContactUpdateModelForm(FormCleanContactNumber, ModelForm):
    has_confirmed = BooleanField(initial=False, required=False)
    need_to_confirm = False

    class Meta:
        model = default_contact_model
        fields = default_contact_fields

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs.keys():
            self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def clean(self):
        # if name exists make user confirm
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        name_initial = self.initial['name']
        has_confirmed = cleaned_data['has_confirmed']
        self.need_to_confirm = False

        contacts = self.Meta.model.objects.filter(name__iexact=name)
        has_changed = name_initial.lower() != name.lower()
        if contacts.exists() and has_changed:
            if not has_confirmed:
                msg = 'A contact with name "{}"\
                    already exists. Please confirm to continue'
                msg = msg.format(name)
                self.add_error('has_confirmed', msg)
                self.need_to_confirm = True
                if hasattr(self, 'request'):
                    messages.warning(self.request, msg)

        return cleaned_data


class CandidateCreateModelForm(ContactCreateModelForm):

    class Meta:
        model = default_contact_model
        fields = default_contact_fields + [
            'current_previous_position', 'highest_educational_qualification',
            'notes']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

    def is_valid(self):
        """Set default candidate owner and cv template"""
        is_valid = super().is_valid()

        if is_valid:
            employee = getattr(self.user, 'as_employee', None)
            self.instance.candidate_owner = employee

            default_cv = CVTemplate.objects.filter(is_default=True).first()
            self.instance.cv_template = default_cv

        return is_valid


class CandidateUpdateModelForm(ContactUpdateModelForm):

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
            'other_online_ids',
            'location',

            'current_previous_position',
            'current_previous_company',
            'current_previous_salary',
            # 'current_previous_benefits',
            'motivation_for_leaving',
            'expected_salary',
            # 'expected_benefits',

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

    def clean_cv_template(self):
        default = CVTemplate.objects.filter(is_default=True).first()
        cv_template = self.cleaned_data['cv_template']
        if not cv_template:
            cv_template = default
        return cv_template


class ClientUpdateModelForm(ContactUpdateModelForm):
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
            'initial_approach_date',
            'meeting_arranged',
            'agreement_term',
            'agreement_fee',
            'refund_scheme',
            'validity',
            'notes',
            'point_of_contacts',
            'business_development_person',
            'signed_on',
        ]

    agreement_fields = (
        'agreement_term',
        'agreement_fee',
        'refund_scheme',
        'validity',
        'signed_on',
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super().__init__(*args, **kwargs)

        self.fields['industry'].required = True

        # disable agreement fields if not allowed
        is_allowed_to_edit_aggrement_fields = user.has_perm(
            'contacts.edit_client_agreement_fields')
        if not is_allowed_to_edit_aggrement_fields:
            for field in self.agreement_fields:
                self.fields[field].disabled = True


class ClientCreateModelForm(ContactCreateModelForm):

    class Meta:
        model = Client
        fields = [
            'name',
            'contact_number',
            'whatsapp_link',
            'email_address',
            'location',
            'industry',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['industry'].required = True


class SupplierModelForm(ContactCreateModelForm):

    class Meta:
        model = Supplier
        fields = default_contact_fields + [
            'alternate_contact_number',
            'skype_id',
            'ms_teams_id',
            'subscription_validity',
            'point_of_contacts',
            'notes',
        ]


class SupplierUpdateModelForm(ContactUpdateModelForm):
    class Meta:
        model = SupplierModelForm.Meta.model
        fields = SupplierModelForm.Meta.fields
