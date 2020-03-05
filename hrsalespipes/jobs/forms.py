import datetime

from django.forms import ModelForm

from .models import Job


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
