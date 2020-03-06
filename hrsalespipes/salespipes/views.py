import datetime
import json

from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView, ListView

from .forms import PipelineCreateModelForm, PipelineModelForm
from .models import Pipeline
from jobs.models import Job


class PipelineCreateView(CreateView):
    model = Pipeline
    form_class = PipelineCreateModelForm
    template_name = 'salespipes/pipeline_create_form.html'

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


class PipelineUpdateView(UpdateView):
    model = Pipeline
    form_class = PipelineModelForm
    template_name = 'salespipes/pipeline_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        jobs = Job.objects.all()
        jobs = [{'value': str(data.pk), 'text': data.reference_number}
                for data in jobs]
        jobs = json.dumps(jobs)

        context['jobs'] = jobs
        return context


class PipelineListView(ListView):
    model = Pipeline


class PipelineDetailView(DetailView):
    model = Pipeline
