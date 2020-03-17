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

from .utils import generate_excel
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
        aggregate_fields = ['invoice_amount', 'vat']
        aggregate_fields = [Sum(field) for field in aggregate_fields]
        sums = q.aggregate(*aggregate_fields)
        context['invoice_amount__sum'] = sums['invoice_amount__sum']
        context['vat__sum'] = sums['vat__sum']
        return context


class PipelineSummaryPDFView(
        WeasyTemplateResponseMixin,
        PipelineSummaryListView):
    template_name = 'reports/pdf/pipeline_summary.html'
    pdf_attachment = True
    pdf_filename = 'pipeline-summary.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class PipelineSummaryExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'salespipes.view_report_pipeline_summary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; \
            filename="pipeline-summary.xls"'

        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)

        columns = (
            'Date',
            'Status',
            'Job Reference Number',
            'Job Date',
            'Position',
            'Candidate Code',
            'Candidate',
            'Client',
            'Industry',
            'Invoice Date',
            'Invoice Number',
            'Invoice Amount',
            'VAT',
        )
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('PipelineSummary')

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        heading = [
            'Pipeline Summary',
            Setting.objects.first().company_name,
            'For the period {} to {}'.format(date_from, date_to)
        ]
        for head in heading:
            ws.write(row_num, 0, head, font_style)
            row_num += 1
        row_num += 1  # blank row

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        job__candidates_queryset = JobCandidate.objects.select_related(
            'status', 'candidate').filter(status__probability__gte=1)
        rows = Pipeline.objects.all()

        rows = rows.select_related('job', 'status')
        rows = rows.prefetch_related(
            'job__client',
            Prefetch('job__candidates', queryset=job__candidates_queryset))

        if date_from and date_to:
            try:
                data = rows.filter(date__gte=date_from, date__lte=date_to)
            except Exception as e:
                data = None
                rows = Pipeline.objects.none()

        for row in rows:
            row_num += 1
            job_candidates = row.job.candidates
            if job_candidates:
                candidate = job_candidates.first().candidate
                candidate_name = candidate.name
                candidate_code = candidate.code
            else:
                candidate_name = ''
                candidate_code = ''

            job = row.job
            client = row.job.client

            values = [
                row.date,
                row.status.name,
                job.reference_number,
                job.date,
                job.position,
                candidate_name,
                candidate_code,
                client.name,
                client.industry,
                row.invoice_date,
                row.invoice_number,
                row.invoice_amount,
                row.vat
            ]

            for i, col in enumerate(columns):
                ws.write(row_num, i, values[i], font_style)

        # total row
        row_num += 1
        if data:
            sums = data.aggregate(Sum('invoice_amount'), Sum('vat'))
            ws.write(
                row_num,
                10,
                'TOTAL',
                font_style)

            ws.write(
                row_num,
                11,
                sums['invoice_amount__sum'],
                font_style)

            ws.write(
                row_num,
                12,
                sums['vat__sum'],
                font_style)

        wb.save(response)
        return response


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
    pdf_attachment = True
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

        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)

        columns = ['Date', 'Board', 'Reference Number', 'Client',
                   'Position', 'Location', 'Potential Income', ]
        values_list = [
            'date', 'board__name', 'reference_number', 'client__name',
            'position', 'location', 'potential_income'
        ]

        wb = generate_excel(
            'Jobs Summary',
            date_from,
            date_to,
            columns,
            Job,
            ('board', 'client'),
            values_list,
            ((6, 'potential_income'), ),
            5
        )

        wb.save(response)
        return response
