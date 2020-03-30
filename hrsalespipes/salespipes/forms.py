from django.contrib import messages
from django.db import transaction
from django.forms import ModelForm
from django.utils import timezone

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

        # if status is greater or equal to 1 then invoice details
        # should be provided
        if cleaned_data['status'].should_have_invoice:
            if not cleaned_data['invoice_date']:
                msg = 'Provide invoice date.'
                self.add_error('invoice_date', msg)

            if not cleaned_data['invoice_number']:
                msg = 'Provide invoice number.'
                self.add_error('invoice_number', msg)

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
                today = timezone.localdate()
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
            'job_candidate',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

        self.fields['job_candidate'].required = True

    def clean_job_candidate(self):
        """Don't allow job candidate of job that is closed.
        """
        job_candidate = self.cleaned_data['job_candidate']
        if job_candidate:
            # check if job status is closed, then add error
            job = job_candidate.job
            job_status = job.status
            if job_status:
                if not job_status.is_job_open:
                    msg = job_candidate.job.closed_job_msg
                    messages.info(self.request, msg)
                    self.add_error(
                        'job_candidate',
                        msg
                    )
        return job_candidate

    def is_valid(self):
        """Set default date, base amount, terms, rate, status,
        and potential income
        """
        is_valid = super().is_valid()

        if is_valid:
            self.instance.date = timezone.localdate()

            job_candidate = self.instance.job_candidate
            self.instance.base_amount = job_candidate.salary_offered

            job_candidate_status = job_candidate.status
            self.instance.status = getattr(
                job_candidate_status, 'related_pipeline_status', None)

            client = job_candidate.job.client
            self.instance.recruitment_term = client.agreement_term
            self.instance.recruitment_rate = client.agreement_fee

            computed_potential_income = self.instance.computed_potential_income
            self.instance.potential_income = computed_potential_income

        return is_valid


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
