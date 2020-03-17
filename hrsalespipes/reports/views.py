import calendar
import datetime
import uuid
import xlwt

from django.db.models import Prefetch, Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        sums = q.aggregate(Sum('invoice_amount'), Sum('vat'))
        context['invoice_amount__sum'] = sums['invoice_amount__sum']
        context['vat__sum'] = sums['vat__sum']
        return context


class PipelineSummaryPDFView(
        WeasyTemplateResponseMixin,
        PipelineSummaryListView):
    template_name = 'reports/pdf/pipeline_summary.html'
    pdf_attachment = False
    pdf_filename = 'pipeline-summary.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


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
    pdf_attachment = False
    pdf_filename = 'jobs-summary.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class JobsSummaryExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'jobs.view_report_jobs_summary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="jobs-summary.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('JobsSummary')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True


        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)

        heading = [
            'Jobs Summary',
            Setting.objects.first().company_name,
            'For the period {} to {}'.format(date_from, date_to)
        ]
        for head in heading:
            ws.write(row_num, 0, head, font_style)
            row_num += 1

        columns = ['Date', 'Board', 'Reference Number', 'Client',
                   'Position', 'Location', 'Potential Income', ]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = Job.objects.all().select_related('board', 'client')

        if date_from and date_to:
            try:
                values_list = [
                    'date', 'board__name', 'reference_number', 'client__name',
                    'position', 'location', 'potential_income'
                ]
                data = rows.filter(date__gte=date_from, date__lte=date_to)
                print(rows)
                rows = data.values_list(*values_list)
            except Exception as e:
                data = None
                rows = Job.objects.none()


        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                val = row[col_num]
                if type(val) == uuid.UUID:
                    val = str(val)

                ws.write(row_num, col_num, val, font_style)

        # total row
        row_num += 1
        if data:
            sums = data.aggregate(Sum('potential_income'))
            ws.write(
                row_num,
                len(columns) - 2,
                'TOTAL',
                font_style)

            ws.write(
                row_num,
                len(columns) - 1,
                sums['potential_income__sum'],
                font_style)

        wb.save(response)
        return response
