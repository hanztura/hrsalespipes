import datetime
import json

from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import PipelineCreateModelForm, PipelineModelForm
from .models import Pipeline, Status
from jobs.models import Job
from system.models import Setting
from system.utils import PermissionRequiredWithCustomMessageMixin as PermissionRequiredMixin


class PipelineCreateView(PermissionRequiredMixin, CreateView):
    model = Pipeline
    form_class = PipelineCreateModelForm
    template_name = 'salespipes/pipeline_create_form.html'
    permission_required = 'salespipes.add_pipeline'

    def form_valid(self, form):
        form.instance.date = datetime.date.today()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jobs = Job.objects.all()
        jobs = [{'value': str(data.pk), 'text': data.reference_number}
                for data in jobs]
        jobs = json.dumps(jobs)

        context['jobs'] = jobs
        return context


class PipelineUpdateView(PermissionRequiredMixin, UpdateView):
    model = Pipeline
    form_class = PipelineModelForm
    template_name = 'salespipes/pipeline_update_form.html'
    permission_required = 'salespipes.change_pipeline'

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
        context['status_objects'] = status_objects
        context['vat_rate'] = vat_rate
        return context

    def get_success_url(self):
        return reverse(
            'salespipes:detail',
            args=[str(self.object.pk), ])


class PipelineListView(PermissionRequiredMixin, ListView):
    model = Pipeline
    permission_required = 'salespipes.view_pipeline'


class PipelineDetailView(PermissionRequiredMixin, DetailView):
    model = Pipeline
    permission_required = 'salespipes.view_pipeline'
