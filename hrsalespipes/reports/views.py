from django.db.models import Prefetch, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from django_weasyprint import WeasyTemplateResponseMixin

from jobs.models import Job, JobCandidate
from salespipes.models import Pipeline
from system.utils import (
    PermissionRequiredWithCustomMessageMixin, FromToViewFilterMixin)
from system.models import Setting


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'


class PipelineSummaryListView(
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Pipeline
    template_name = 'reports/pipeline_summary.html'
    permission_required = 'salespipes.view_report_pipeline_summary'
    paginate_by = 25

    def get_queryset(self):
        q = super().get_queryset()

        job__candidates_queryset = JobCandidate.objects.select_related(
            'status', 'candidate').filter(status__probability__gte=1)
        q = q.select_related('status', 'job')
        q = q.prefetch_related(
            'job__client',
            Prefetch('job__candidates', queryset=job__candidates_queryset))

        return q


class JobsSummaryListView(
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Job
    template_name = 'reports/jobs_summary.html'
    permission_required = 'jobs.view_report_jobs_summary'
    paginate_by = 0

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('board', 'client')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        sums = q.aggregate(Sum('potential_income'))
        context['potential_income__sum'] = sums['potential_income__sum']
        return context


class JobsSummaryPDFView(
        WeasyTemplateResponseMixin,
        JobsSummaryListView):
    template_name = 'reports/pdf/jobs_summary.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context
