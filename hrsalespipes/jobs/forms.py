from django.contrib import messages
from django.db import transaction
from django.forms import ModelForm, BooleanField
from django.utils import timezone

from .models import Job, JobCandidate, Interview, JobStatus
from salespipes.forms import (
    Pipeline, PipelineUpdateStatusModelForm,
    PipelineCreateModelForm)


class JobCreateModelForm(ModelForm):

    class Meta:
        model = Job
        fields = [
            'reference_number',
            'client',
            'position',
        ]

    def is_valid(self):
        """Set default date and status here."""
        is_valid = super().is_valid()

        if is_valid:
            instance = self.instance

            # set default job status
            default_status = JobStatus.objects.filter(is_default=True).first()
            instance.status = default_status

            instance.date = timezone.localdate()

        return is_valid


class JobUpdateModelForm(ModelForm):
    has_confirmed = BooleanField(initial=False, required=False)

    request = None

    class Meta:
        model = Job
        fields = [
            'reference_number',
            'date',
            'client',
            'position',
            'location',
            'potential_income',
            'status'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

        self.fields['status'].required = True

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data['status']
        has_confirmed = cleaned_data['has_confirmed']

        if status.job_is_closed and not has_confirmed:
            if self.request:
                msg = 'Please confirm to close this Job.'
                messages.info(self.request, msg)

            self.add_error('has_confirmed', msg)


class JobCandidateCreateModelForm(ModelForm):
    request = None

    class Meta:
        model = JobCandidate
        fields = [
            'candidate',
        ]

    def __init__(self, *args, **kwargs):
        self.job = kwargs.pop('job')
        self.employee = kwargs.pop('employee')
        self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

    def is_valid(self, *args, **kwargs):
        """set default job, default associate and registration date"""
        self.instance.job = self.job

        # set associate
        if self.employee:
            self.instance.associate = self.employee
        else:
            if self.request:
                messages.warning(
                    self.request,
                    'Contact admin for employee profile.')

            self.add_error(None, 'Your Employee profile is required')

        self.instance.registration_date = timezone.localdate()

        return super().is_valid(*args, **kwargs)


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
        self.request = kwargs.pop('request')

        super().__init__(*args, **kwargs)

        self.fields['consultant'].required = True
        self.fields['cv_source'].required = True
        self.fields['status'].required = True

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
                # related_pipeline_status_pk = related_pipeline_status.pk if related_pipeline_status else None
                data = {
                    'job_candidate': instance.pk,
                }
                new_pipeline_form = PipelineCreateModelForm(data, request=None)

                if new_pipeline_form.is_valid():
                    new_pipeline_form.save()
                else:
                    if self.request:
                        msg = 'Pipeline not created due to {}. Please manually \
                            create a pipeline record.'
                        msg = msg.format(str(new_pipeline_form.errors))
                        messages.info(self.request, msg)


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
            'date_time',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        self.employee = kwargs.pop('employee')
        self.job_candidate = kwargs.pop('job_candidate')

        super().__init__(*args, **kwargs)

    def is_valid(self):
        is_valid = super().is_valid()

        if is_valid:
            self.instance.done_by = self.employee
            self.instance.job_candidate = self.job_candidate

        return is_valid


class InterviewUpdateModelForm(InterviewCreateModelForm):

    class Meta:
        model = Interview
        fields = [
            'mode',
            'date_time',
            'status',
            'done_by'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['done_by'].required = True
