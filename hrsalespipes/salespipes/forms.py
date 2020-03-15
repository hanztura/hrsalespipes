from django.forms import ModelForm

from .models import Pipeline
from commissions.helpers import create_commission
from system.models import Setting


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

    def clean_recruitment_term(self):
        default = 1
        cleaned_data = self.cleaned_data.get('recruitment_term', default)
        if cleaned_data:
            return round(cleaned_data, 2)

        return default

    def clean_recruitment_rate(self):
        default = 0
        cleaned_data = self.cleaned_data.get('recruitment_rate', default)
        if cleaned_data:
            return round(cleaned_data, 2)

        return default

    def clean_base_amount(self):
        default = 0
        cleaned_data = self.cleaned_data.get('base_amount', default)
        if cleaned_data:
            return round(cleaned_data, 2)

        return default

    def clean_potential_income(self):
        default = 0
        cleaned_data = self.cleaned_data.get('potential_income', default)
        if cleaned_data:
            return round(cleaned_data, 2)

        return default

    def clean(self):
        cleaned_data = super().clean()
        potential_income = cleaned_data.get('potential_income')

        setting = Setting.objects.all().first()
        vat = round(potential_income * setting.vat_rate, 2)
        invoice_amount = round(potential_income + vat, 2)

        cleaned_data['vat'] = vat
        cleaned_data['invoice_amount'] = invoice_amount

        return cleaned_data

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
