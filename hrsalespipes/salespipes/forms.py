from django.forms import ModelForm

from .models import Pipeline


class PipelineModelForm(ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'date',
            'job',
            'invoice_date',
            'recruitment_term',
            'recruitment_rate',
            'base_amount',
            'potential_income',
            'status',
            'invoice_amount',
            'vat',
        ]


class PipelineCreateModelForm(ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'job',
        ]
