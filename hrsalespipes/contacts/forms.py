from django.forms import ModelForm

from .models import Candidate


class CandidateCreateModelForm(ModelForm):

    class Meta:
        model = Candidate
        fields = [
            'name',
            'contact_number',
            'whatsapp_link',
            'email_address',
            'location',
        ]


class CandidateUpdateModelForm(CandidateCreateModelForm):

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
