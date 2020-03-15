import datetime

from django.db import transaction
from django.forms import ModelForm

from .models import Job, JobCandidate, Interview
from salespipes.forms import (
    Pipeline, PipelineModelForm, PipelineUpdateStatus)


class JobCreateModelForm(ModelForm):

    class Meta:
        model = Job
        fields = [
            'board',
            'reference_number',
            'client',
            'position',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['board'].required = True


class JobUpdateModelForm(ModelForm):

    class Meta:
        model = Job
        fields = [
            'board',
            'reference_number',
            'date',
            'client',
            'position',
            'location',
            'potential_income',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['board'].required = True


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
            'associate',
        ]

    @transaction.atomic
    def save(self, commit=True):
        instance = super().save(commit)

        if instance.status.should_create_pipeline and commit:
            try:
                related_pipeline_status = \
                    instance.status.related_pipeline_status
                is_upgrade = instance.status.probability > \
                    related_pipeline_status.probability
            except Exception as e:
                related_pipeline_status = None
                is_upgrade = False

            pipeline_record = Pipeline.objects.filter(job_id=instance.job_id)
            if not pipeline_record.exists():
                data = {
                    'job': instance.job_id,
                    'status': related_pipeline_status.pk,
                    'base_amount': instance.salary_offered,
                    'date': datetime.date.today(),
                }
                pipeline = PipelineModelForm(data)
                if pipeline.is_valid():
                    pipeline = pipeline.save()

            # only update status if not created and if probability is upgrade
            if pipeline_record.exists() and is_upgrade:
                pipeline_record = pipeline_record.first()
                pipeline = PipelineUpdateStatus(
                    {'status': related_pipeline_status.pk},
                    instance=pipeline_record)

                if pipeline.is_valid():
                    pipeline.save()

        return instance


class InterviewModelForm(ModelForm):

    class Meta:
        model = Interview
        fields = [
            'mode',
            'date',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].initial = datetime.date.today()
