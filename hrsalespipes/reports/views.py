from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from salespipes.models import Pipeline
from system.utils import PermissionRequiredWithCustomMessageMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'


class PipelineSummaryListView(
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Pipeline
    template_name = 'reports/pipeline_summary.html'
    permission_required = 'salespipes.view_report_pipeline_summary'

    def get_queryset(self):
        q = super().get_queryset()
        q = q.prefetch_related(
            'job__client',
            'job__candidates__candidate',
            'job__candidates__status')
        return q
