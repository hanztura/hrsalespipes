import datetime
import json

from django.conf import settings
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import (JobCreateModelForm, JobUpdateModelForm,
                    JobCandidateCreateModelForm, JobCandidateUpdateModelForm)
from .models import Job, JobCandidate, Status
from contacts.models import Client, Candidate
from system.models import User


class JobCreateView(CreateView):
    model = Job
    form_class = JobCreateModelForm
    template_name = 'jobs/job_create_form.html'

    def form_valid(self, form):
        form.instance.consultant = self.request.user
        form.instance.date = datetime.date.today()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clients = Client.objects.all()
        clients = [{'value': str(data.pk), 'text': data.name}
                   for data in clients]
        clients = json.dumps(clients)

        context['clients'] = clients
        return context


class JobUpdateView(UpdateView):
    model = Job
    form_class = JobUpdateModelForm
    template_name = 'jobs/job_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        clients = Client.objects.all()
        clients = [{'value': str(data.pk), 'text': data.name}
                   for data in clients]
        clients = json.dumps(clients)

        users = User.objects.all()
        users = [{'value': str(data.pk), 'text': str(data)} for data in users]
        users = json.dumps(users)

        context['clients'] = clients
        context['users'] = users
        return context


class JobListView(ListView):
    model = Job

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('consultant', 'client')
        return queryset


class JobDetailView(DetailView):
    model = Job

    def get_queryset(self):
        q = super().get_queryset()
        q = q.prefetch_related(
            'consultant', 'candidates', 'candidates__candidate',
            'candidates__status')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['candidates'] = self.object.candidates.all()
        context['JOB_POTENTIAL_INCOME_ALIAS'] = settings.JOB_POTENTIAL_INCOME_ALIAS
        context['JOB_REFERENCE_NUMBER_ALIAS'] = settings.JOB_REFERENCE_NUMBER_ALIAS
        return context


class JobCandidateCreateView(CreateView):
    model = JobCandidate
    form_class = JobCandidateCreateModelForm
    template_name = 'jobs/jobcandidate_create_form.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        job = self.kwargs['job_pk']
        job = Job.objects.get(pk=job)
        self.job = job

    def form_valid(self, form):
        form.instance.job = self.job
        form.instance.registration_date = datetime.date.today()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidates = Candidate.objects.all()
        candidates = [{'value': str(data.pk), 'text': data.name}
                      for data in candidates]
        candidates = json.dumps(candidates)

        context['candidates'] = candidates
        context['job'] = self.job
        return context

    def get_success_url(self):
        return reverse(
            'jobs:candidates_edit',
            args=[str(self.object.job_id), str(self.object.pk)])


class JobCandidateUpdateView(UpdateView):
    model = JobCandidate
    form_class = JobCandidateUpdateModelForm
    template_name = 'jobs/jobcandidate_update_form.html'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('job', 'candidate')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        candidates = Candidate.objects.all()
        candidates = [{'value': str(data.pk), 'text': data.name}
                      for data in candidates]
        candidates = json.dumps(candidates)

        status_objects = Status.objects.all()
        status_objects = [{'value': str(data.pk), 'text': data.name}
                          for data in status_objects]
        status_objects = json.dumps(status_objects)

        job = self.kwargs['job_pk']
        job = Job.objects.get(pk=job)

        context['candidates'] = candidates
        context['status_objects'] = status_objects
        context['job'] = job
        return context


class JobCandidateDetailView(DetailView):
    model = JobCandidate

    def get_queryset(self):
        q = super().get_queryset().select_related('candidate', 'job', 'status')
        return q
