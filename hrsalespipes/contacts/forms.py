from django.forms import ModelForm

from .models import Candidate, Client
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


class CandidateUpdateModelForm(ContactCreateModelForm):

    class Meta:
        model = Candidate
        fields = [
            'name',
            'contact_number',
            'alternate_contact_number',
            'email_address',
            'whatsapp_link',
            'skype_id',
            'ms_teams_id',
            'location',

            'current_previous_position',
            'current_previous_company',
            'current_previous_salary_and_benefits',
            'motivation_for_leaving',

            'nationality',
            'languages',
            'preferred_location',
            'civil_status',
            'dependents',
            'gender',
            'highest_educational_qualification',
            'date_of_birth',

            'visa_status',
            'expected_salary_and_benefits',
            'availability_for_interview',
            'notice_period',
            'candidate_owner',
            'notes',
        ]


class ClientUpdateModelForm(ContactCreateModelForm):

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
            'agreement_terms',
            'agreement_fee',
            'refund_scheme',
            'validity',
        ]


class ClientCreateModelForm(FormCleanContactNumber, ModelForm):

    class Meta:
        model = Client
        fields = [
            'name',
            'contact_number',
            'whatsapp_link',
            'email_address',
            'location',
        ]
