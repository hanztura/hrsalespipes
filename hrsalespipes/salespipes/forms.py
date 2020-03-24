import datetime
from django.db import transaction
from django.forms import ModelForm

from .models import Pipeline, Status
from .utils import CreateCommissionFormMixin
from system.models import Setting


class PipelineModelForm(CreateCommissionFormMixin, ModelForm):

    class Meta:
        model = Pipeline
        fields = [
            'date',
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

    @transaction.atomic
    def save(self, commit=True):
        """Update Pipeline record.

        If pipeline status changes INTO probability >= 1 then
        set successful date.

        If Pipeline status changes, update Job Candidate status
        accordingly.
        """
        # update success date if status has changed
        status = self.fields['status']
        initial = self.initial.get('status', None)
        data = self.cleaned_data['status'].pk
        instance = self.instance

        if status.has_changed(initial, data):
            # set successful date
            if instance.status.probability >= 1:
                today = datetime.date.today()
                instance.successful_date = today
            else:
                instance.successful_date = None

            # update job candidate status accordingly
            job_candidate = instance.job_candidate
            job_candidate.status_id = self.instance.status.job_status_id
            job_candidate.save()

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


class StatusModelForm(ModelForm):

    class Meta:
        model = Status
        fields = [
            'name',
            'probability',
            'job_status',
            'is_closed',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['job_status'].required = True
