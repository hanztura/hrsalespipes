from django.db import transaction
from django.forms import ModelForm
from django.utils import timezone

from .models import Job, JobCandidate, Interview
from salespipes.forms import (
    Pipeline, PipelineModelForm, PipelineUpdateStatusModelForm)


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
            'cv_source',
            'cv_date_shared',
            'remarks',
            'salary_offered_currency',
            'salary_offered',
            'tentative_date_of_joining',
            'associate',
            'consultant',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['consultant'].required = True
        self.fields['cv_source'].required = True

        # check if pipeline exists, then disable status ff yes
        job_candidate = self.instance
        try:
            if job_candidate.pipeline:
                self.fields['status'].disabled = True
        except Exception as e:
            pass

    @transaction.atomic
    def save(self, commit=True):
        instance = super().save(commit)

        # create pipeline if needed
        if instance.status.should_create_pipeline and commit:
            if hasattr(instance.status, 'related_pipeline_status'):
                # get candidate status' related pipeline status
                related_pipeline_status = \
                    instance.status.related_pipeline_status
            else:
                related_pipeline_status = None
                is_upgrade = False

            pipeline_record = Pipeline.objects.filter(
                job_candidate_id=instance.pk)

            if not pipeline_record.exists():  # if no pipeline record, create
                related_pipeline_status_pk = related_pipeline_status.pk if related_pipeline_status else None
                data = {
                    'job_candidate': instance.pk,
                    'status': related_pipeline_status_pk,
                    'base_amount': instance.salary_offered,
                    'date': timezone.localdate(),
                }
                new_pipeline_form = PipelineModelForm(data)

                if new_pipeline_form.is_valid():
                    new_pipeline_form.save()

            # only update status if not created and if probability is upgrade
            # then update pipeline status
            if pipeline_record.exists():
                is_upgrade = False
                pipeline_record = pipeline_record.first()
                pipeline_record_status = pipeline_record.status

                if pipeline_record_status:
                    is_upgrade = instance.status.probability > \
                        pipeline_record_status.probability

                if is_upgrade:
                    pipeline = PipelineUpdateStatusModelForm(
                        {'status': related_pipeline_status.pk},
                        instance=pipeline_record)

                    if pipeline.is_valid():
                        pipeline.save()

        return instance


class InterviewCreateModelForm(ModelForm):

    class Meta:
        model = Interview
        fields = [
            'mode',
            'date',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['date'].initial = timezone.localdate()


class InterviewUpdateModelForm(InterviewCreateModelForm):

    class Meta:
        model = Interview
        fields = [
            'mode',
            'date',
            'status',
            'done_by'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['done_by'].required = True
