import datetime
import json

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import JobCreateModelForm, JobUpdateModelForm
from .models import Job
from contacts.models import Client
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
