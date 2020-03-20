import datetime
from django.forms import ModelForm

from .models import Pipeline
from .utils import CreateCommissionFormMixin
from system.models import Setting


class PipelineModelForm(CreateCommissionFormMixin, ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'date',
            'job',
            'job_candidate',
            'recruitment_term',
            'recruitment_rate',
            'base_amount',
            'potential_income',
            'status',
            'invoice_date',
            'invoice_number',
            'invoice_amount',
            'vat',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['job_candidate'].required = True

    def clean_recruitment_term(self):
        default = 1
        cleaned_data = self.cleaned_data.get('recruitment_term', default)
        if cleaned_data:
            return round(cleaned_data, 5)

        return default

    def clean_recruitment_rate(self):
        default = 0
        cleaned_data = self.cleaned_data.get('recruitment_rate', default)
        if cleaned_data:
            return round(cleaned_data, 10)

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
        # update success date if status has changed
        status = self.fields['status']
        initial = self.initial.get('status', None)
        data = self.cleaned_data['status'].pk
        if status.has_changed(initial, data):
            if self.instance.status.probability >= 1:
                today = datetime.date.today()
                self.instance.successful_date = today
            else:
                self.instance.successful_date = None

        return super().save(commit)


class PipelineCreateModelForm(ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'job',
            'job_candidate',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['job_candidate'].required = True


class PipelineUpdateStatusModelForm(CreateCommissionFormMixin, ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'status'
        ]
