import datetime

from django.forms import ModelForm

from .models import Job, JobCandidate


class JobCreateModelForm(ModelForm):

    class Meta:
        model = Job
        fields = [
            'reference_number',
            'client',
            'position',
        ]


class JobUpdateModelForm(ModelForm):

    class Meta:
        model = Job
        fields = [
            'reference_number',
            'date',
            'client',
            'position',
            'consultant',
            'location',
            'potential_income',
        ]


class JobCandidateCreateModelForm(ModelForm):

    class Meta:
        model = JobCandidate
        fields = [
            'candidate',
        ]


class JobCandidateUpdateModelForm(ModelForm):

    class Meta:
        model = JobCandidate
        fields = [
            'candidate',
            'registration_date',
            'status',
            'cv_date_shared',
            'remarks',
            'salary_offered_currency',
            'salary_offered',
            'tentative_date_of_joining',
            'actual_income',
        ]
