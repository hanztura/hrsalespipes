import calendar
import datetime

from django.db.models import Prefetch
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView

from jobs.models import JobCandidate
from salespipes.models import Pipeline
from system.utils import (
    PermissionRequiredWithCustomMessageMixin, FromToViewFilterMixin)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get_queryset(self):
        q = super().get_queryset()

        job__candidates_queryset = JobCandidate.objects.select_related(
            'status', 'candidate').filter(status__probability__gte=1)
        q = q.select_related('status', 'job')
        q = q.prefetch_related(
            'job__client',
            Prefetch('job__candidates', queryset=job__candidates_queryset))

        return q
