from django.forms import ModelForm

from .models import Pipeline
from commissions.helpers import create_commission


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

    def save(self, commit=True):
        instance = super().save(commit)

        probability = instance.status.probability
        if commit and probability >= 1:
            create_commission(instance)

        return instance


class PipelineCreateModelForm(ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'job',
        ]


class PipelineUpdateStatus(ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'status'
        ]

    def save(self, commit=True):
        instance = super().save(commit)

        probability = instance.status.probability
        if commit and probability >= 1:
            create_commission(instance)

        return instance
