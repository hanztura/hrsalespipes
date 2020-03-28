import json

from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import (
    JobCreateModelForm, JobUpdateModelForm,
    JobCandidateCreateModelForm, JobCandidateUpdateModelForm,
    InterviewCreateModelForm, InterviewUpdateModelForm, JobStatus)
from .models import Job, JobCandidate, Status, Interview
from .utils import JobIsClosedMixin, JobIsClosedContextMixin
from contacts.models import Client, Candidate, Employee, Supplier as Board
from system.helpers import get_objects_as_choices, ActionMessageViewMixin
from system.models import InterviewMode, Location
from system.utils import (
    PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin,
    DisplayDateFormatMixin, DateAndStatusFilterMixin)


class JobCreateView(
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Job
    form_class = JobCreateModelForm
    template_name = 'jobs/job_create_form.html'
    permission_required = 'jobs.add_job'
    success_msg = 'Job created.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['clients'] = get_objects_as_choices(Client)
        return context


class JobUpdateView(
        JobIsClosedMixin,
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Job
    form_class = JobUpdateModelForm
    template_name = 'jobs/job_update_form.html'
    permission_required = 'jobs.change_job'
    success_msg = 'Job updated.'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['clients'] = get_objects_as_choices(Client)
        context['locations'] = get_objects_as_choices(Location)

        # Job Status
        status_objects = JobStatus.objects.values()
        status_objects = [status for status in status_objects]
        context['job_status_objects'] = json.dumps(status_objects)
        return context

    def get_success_url(self):
        return reverse(
            'jobs:detail',
            args=[str(self.object.pk), ])


class JobListView(
        DisplayDateFormatMixin,
        DateAndStatusFilterMixin,
        PermissionRequiredMixin, ListView):
    model = Job
    permission_required = 'jobs.view_job'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('client', 'status')
        queryset = queryset.prefetch_related('candidates')

        # filter by reference number
        search = self.request.GET.get('q', '')
        if search:

            queryset = queryset.filter(
                Q(reference_number__icontains=search) |
                Q(client__name__icontains=search))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # filter by reference number
        context['q'] = self.request.GET.get('q', '')
        context['status_objects'] = get_objects_as_choices(JobStatus)
        return context


class JobDetailView(
        JobIsClosedContextMixin,
        DisplayDateFormatMixin,
        PermissionRequiredMixin,
        DetailView):
    model = Job
    permission_required = 'jobs.view_job'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.prefetch_related(
            'candidates', 'candidates__candidate',
            'candidates__status', 'candidates__associate',
            'candidates__pipeline__status', 'status',
            'candidates__interviews', 'candidates__pipeline__job_candidate__consultant',
            'candidates__pipeline__job_candidate__associate',)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidates = self.object.candidates.all()
        pipelines = [candidate.pipeline for candidate in candidates
                     if hasattr(candidate, 'pipeline')]

        context['candidates'] = candidates
        context['pipelines'] = pipelines
        context['JOB_POTENTIAL_INCOME_ALIAS'] = \
            settings.JOB_POTENTIAL_INCOME_ALIAS
        context['JOB_REFERENCE_NUMBER_ALIAS'] = \
            settings.JOB_REFERENCE_NUMBER_ALIAS
        return context


class JobCandidateCreateView(
        JobIsClosedMixin,
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = JobCandidate
    form_class = JobCandidateCreateModelForm
    template_name = 'jobs/jobcandidate_create_form.html'
    permission_required = 'jobs.add_jobcandidate'
    success_msg = 'Job Candidate created.'
    job_pk_kwarg = 'job_pk'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        job = self.kwargs['job_pk']
        job = Job.objects.get(pk=job)
        self.job = job

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['job'] = self.job
        kwargs['employee'] = getattr(self.request.user, 'as_employee', None)
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['candidates'] = get_objects_as_choices(Candidate)
        context['job'] = self.job
        return context

    def get_success_url(self):
        return reverse(
            'jobs:candidates_edit',
            args=[str(self.object.job_id), str(self.object.pk)])


class JobCandidateUpdateView(
        JobIsClosedMixin,
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = JobCandidate
    form_class = JobCandidateUpdateModelForm
    template_name = 'jobs/jobcandidate_update_form.html'
    permission_required = 'jobs.change_jobcandidate'
    success_msg = 'Job Candidate updated.'
    job_pk_kwarg = 'job_pk'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('job', 'candidate')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        job = self.kwargs['job_pk']
        job = Job.objects.get(pk=job)

        context['candidates'] = get_objects_as_choices(Candidate)
        context['status_objects'] = get_objects_as_choices(Status)
        context['employees'] = get_objects_as_choices(Employee)
        context['cv_sources'] = get_objects_as_choices(Board)
        context['job'] = job
        return context


class JobCandidateDetailView(
        JobIsClosedContextMixin,
        DisplayDateFormatMixin,
        PermissionRequiredMixin,
        DetailView):
    model = JobCandidate
    permission_required = 'jobs.view_jobcandidate'

    def get_queryset(self):
        q = super().get_queryset().select_related(
            'associate', 'consultant', 'status', 'job', 'candidate',
            'job__status')
        q = q.prefetch_related('interviews__done_by')
        return q

    def get_job_object(self):
        return self.object.job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['interviews'] = self.object.interviews.all()
        return context


class InterviewCreateView(
        JobIsClosedMixin,
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        CreateView):
    model = Interview
    form_class = InterviewCreateModelForm
    permission_required = 'jobs.add_interview'
    success_msg = 'Interview created.'
    job_pk_kwarg = 'job_pk'

    def redirect_to_if_closed(self, job):
        """Redirect here. Override if needed"""
        job_candidate_pk = self._kwargs['candidate_pk']
        return redirect(
            'jobs:candidates_detail',
            pk=job_candidate_pk,
            job_pk=job.pk
        )

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        job_candidate = self.kwargs['candidate_pk']
        job_candidate = JobCandidate.objects.select_related(
            'job', 'candidate').get(pk=job_candidate)
        self.job_candidate = job_candidate

    def form_valid(self, form):
        # set up done_by field
        employee = None
        if hasattr(self.request.user, 'as_employee'):
            employee = self.request.user.as_employee

        form.instance.done_by = employee
        form.instance.job_candidate = self.job_candidate
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status_choices = [{'value': data[0], 'text': data[1]}
                          for data in Interview.STATUS_CHOICES]
        status_choices = json.dumps(status_choices)

        context['modes'] = get_objects_as_choices(InterviewMode)
        context['status_choices'] = status_choices
        context['job_candidate'] = self.job_candidate
        context['form_mode'] = 'New'
        return context

    def get_success_url(self):
        return reverse(
            'jobs:candidates_detail',
            args=[str(self.job_candidate.job_id), str(self.job_candidate.pk)])


class InterviewUpdateView(
        JobIsClosedMixin,
        PermissionRequiredMixin,
        ActionMessageViewMixin,
        UpdateView):
    model = Interview
    form_class = InterviewUpdateModelForm
    permission_required = 'jobs.change_interview'
    success_msg = 'Interview updated.'
    job_pk_kwarg = 'job_pk'

    def redirect_to_if_closed(self, job):
        """Redirect here. Override if needed"""
        job_candidate_pk = self._kwargs['candidate_pk']
        return redirect(
            'jobs:candidates_detail',
            pk=job_candidate_pk,
            job_pk=job.pk
        )

    def get_object(self):
        pk = self.kwargs['pk']
        q = Interview.objects.select_related(
            'job_candidate', 'job_candidate__candidate', 'job_candidate__job')
        q = q.get(pk=pk)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status_choices = [{'value': data[0], 'text': data[1]}
                          for data in Interview.STATUS_CHOICES]
        status_choices = json.dumps(status_choices)

        context['modes'] = get_objects_as_choices(InterviewMode)
        context['status_choices'] = status_choices
        context['job_candidate'] = self.object.job_candidate
        context['employees'] = get_objects_as_choices(Employee)
        context['form_mode'] = 'Edit'
        return context

    def get_success_url(self):
        return reverse(
            'jobs:candidates_detail',
            args=[str(self.object.job_candidate.job_id),
                  str(self.object.job_candidate.pk)])
