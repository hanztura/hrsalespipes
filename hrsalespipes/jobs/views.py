import datetime
import json

from django.conf import settings
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import (JobCreateModelForm, JobUpdateModelForm,
                    JobCandidateCreateModelForm, JobCandidateUpdateModelForm,
                    InterviewModelForm)
from .models import Job, JobCandidate, Status, Interview
from contacts.models import Client, Candidate, Employee
from salespipes.models import Pipeline
from system.helpers import get_objects_as_choices
from system.models import User, InterviewMode
from system.utils import PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin


class JobCreateView(PermissionRequiredMixin, CreateView):
    model = Job
    form_class = JobCreateModelForm
    template_name = 'jobs/job_create_form.html'
    permission_required = 'jobs.add_job'

    def form_valid(self, form):
        form.instance.date = datetime.date.today()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['clients'] = get_objects_as_choices(Client)
        return context


class JobUpdateView(PermissionRequiredMixin, UpdateView):
    model = Job
    form_class = JobUpdateModelForm
    template_name = 'jobs/job_update_form.html'
    permission_required = 'jobs.change_job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['clients'] = get_objects_as_choices(Client)
        return context


class JobListView(PermissionRequiredMixin, ListView):
    model = Job
    permission_required = 'jobs.view_job'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('client')
        return queryset


class JobDetailView(PermissionRequiredMixin, DetailView):
    model = Job
    permission_required = 'jobs.view_job'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.prefetch_related(
            'candidates', 'candidates__candidate',
            'candidates__status', 'candidates__associate', 'pipeline')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            pipeline = self.object.pipeline
        except Exception as e:
            pipeline = None

        context['candidates'] = self.object.candidates.all()
        context['pipeline'] = pipeline
        context['JOB_POTENTIAL_INCOME_ALIAS'] = settings.JOB_POTENTIAL_INCOME_ALIAS
        context['JOB_REFERENCE_NUMBER_ALIAS'] = settings.JOB_REFERENCE_NUMBER_ALIAS
        return context


class JobCandidateCreateView(PermissionRequiredMixin, CreateView):
    model = JobCandidate
    form_class = JobCandidateCreateModelForm
    template_name = 'jobs/jobcandidate_create_form.html'
    permission_required = 'jobs.add_jobcandidate'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        job = self.kwargs['job_pk']
        job = Job.objects.get(pk=job)
        self.job = job

    def form_valid(self, form):
        form.instance.job = self.job
        form.instance.associate = self.request.user.as_employee
        form.instance.registration_date = datetime.date.today()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['candidates'] = get_objects_as_choices(Candidate)
        context['job'] = self.job
        return context

    def get_success_url(self):
        return reverse(
            'jobs:candidates_edit',
            args=[str(self.object.job_id), str(self.object.pk)])


class JobCandidateUpdateView(PermissionRequiredMixin, UpdateView):
    model = JobCandidate
    form_class = JobCandidateUpdateModelForm
    template_name = 'jobs/jobcandidate_update_form.html'
    permission_required = 'jobs.change_jobcandidate'

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
        context['job'] = job
        return context


class JobCandidateDetailView(PermissionRequiredMixin, DetailView):
    model = JobCandidate
    permission_required = 'jobs.view_jobcandidate'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.prefetch_related(
            'candidate', 'job', 'status', 'interviews', 'associate')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interviews'] = self.object.interviews.all()
        return context


class InterviewCreateView(PermissionRequiredMixin, CreateView):
    model = Interview
    form_class = InterviewModelForm
    permission_required = 'jobs.add_interview'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        job_candidate = self.kwargs['candidate_pk']
        job_candidate = JobCandidate.objects.select_related(
            'job', 'candidate').get(pk=job_candidate)
        self.job_candidate = job_candidate

    def form_valid(self, form):
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


class InterviewUpdateView(PermissionRequiredMixin, UpdateView):
    model = Interview
    form_class = InterviewModelForm
    permission_required = 'jobs.change_interview'

    def get_object(self):
        pk = self.kwargs['pk']
        q = Interview.objects.select_related(
            'job_candidate', 'job_candidate__candidate', 'job_candidate__job').get(pk=pk)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        status_choices = [{'value': data[0], 'text': data[1]}
                          for data in Interview.STATUS_CHOICES]
        status_choices = json.dumps(status_choices)

        context['modes'] = get_objects_as_choices(InterviewMode)
        context['status_choices'] = status_choices
        context['job_candidate'] = self.object.job_candidate
        context['form_mode'] = 'Edit'
        return context

    def get_success_url(self):
        return reverse(
            'jobs:candidates_detail',
            args=[str(self.object.job_candidate.job_id),
                  str(self.object.job_candidate.pk)])
