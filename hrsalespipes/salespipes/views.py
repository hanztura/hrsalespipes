import json

from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import PipelineCreateModelForm, PipelineModelForm
from .models import Pipeline, Status
from .utils import IsAllowedToViewOrEditMixin
from jobs.models import Job
from jobs.utils import JobIsClosedMixin, JobIsClosedContextMixin
from system.models import Setting
from system.helpers import ActionMessageViewMixin
from system.utils import (
    PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin,
    FromToViewFilterMixin, DisplayDateFormatMixin)


class PipelineCreateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Pipeline
    form_class = PipelineCreateModelForm
    template_name = 'salespipes/pipeline_create_form.html'
    permission_required = 'salespipes.add_pipeline'
    success_msg = 'Pipeline created.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_job_object(self):
        pipeline = self._kwargs['pk']
        self._pipeline = Pipeline.objects.select_related(
            'job_candidate__job').filter(pk=pipeline).first()
        if self._pipeline:
            return self._pipeline.job_candidate.job

        return None

    def form_valid(self, form):
        form.instance.date = timezone.localdate()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get only jobs that are not closed
        jobs = Job.objects.filter(status__is_job_open=True)
        jobs = [{'value': str(data.pk), 'text': data.reference_number}
                for data in jobs]
        jobs = json.dumps(jobs)

        context['jobs'] = jobs
        return context


class PipelineUpdateView(
        JobIsClosedMixin,
        IsAllowedToViewOrEditMixin,
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Pipeline
    form_class = PipelineModelForm
    template_name = 'salespipes/pipeline_update_form.html'
    permission_required = 'salespipes.change_pipeline'
    success_msg = 'Pipeline updated.'

    def get_job_object(self):
        pipeline = self._kwargs['pk']
        self._pipeline = Pipeline.objects.select_related(
            'job_candidate__job').filter(pk=pipeline).first()
        if self._pipeline:
            return self._pipeline.job_candidate.job

        return None

    def redirect_to_if_closed(self, job):
        return redirect(
            'salespipes:detail', pk=str(self._pipeline.pk)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jobs = Job.objects.all()
        jobs = [{'value': str(data.pk), 'text': data.reference_number}
                for data in jobs]
        jobs = json.dumps(jobs)

        status_objects = Status.objects.all()
        status_objects = [{'value': str(data.pk), 'text': data.name}
                          for data in status_objects]
        status_objects = json.dumps(status_objects)

        setting = Setting.objects.all().first()
        vat_rate = setting.vat_rate

        context['jobs'] = jobs
        context['job_id'] = self.object.job_candidate.job_id
        context['status_objects'] = status_objects
        context['vat_rate'] = vat_rate
        return context

    def get_success_url(self):
        return reverse(
            'salespipes:detail',
            args=[str(self.object.pk), ])


class PipelineListView(
        DisplayDateFormatMixin,
        FromToViewFilterMixin,
        PermissionRequiredMixin,
        ListView):
    model = Pipeline
    permission_required = 'salespipes.view_pipeline'
    paginate_by = 25

    def get_queryset(self):
        q = super().get_queryset().select_related('status')
        q = q.prefetch_related(
            'job_candidate__job', 'job_candidate__candidate')
        return q


class PipelineDetailView(
        JobIsClosedContextMixin,
        IsAllowedToViewOrEditMixin,
        DisplayDateFormatMixin,
        PermissionRequiredMixin,
        DetailView):
    model = Pipeline
    permission_required = 'salespipes.view_pipeline'

    def get_job_object(self):
        return self.object.job_candidate.job

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related(
            'job_candidate__status',
            'job_candidate__job',
            'job_candidate__candidate',
            'job_candidate__consultant',
            'job_candidate__associate')

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidate = self.object.job_candidate

        context['candidate'] = candidate
        return context
