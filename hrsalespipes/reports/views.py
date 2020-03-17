import calendar
import datetime
import math
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

        q = q.select_related(
            'status',
            'job',
            'job_candidate__candidate',
            'job_candidate__job__client')

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
    pdf_filename = 'Pipeline Summary.pdf'

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
            filename="Pipeline Summary.xls"'

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

        rows = Pipeline.objects.all()

        rows = rows.select_related(
            'status', 'job_candidate__candidate', 'job_candidate__job__client')

        if date_from and date_to:
            try:
                data = rows.filter(date__gte=date_from, date__lte=date_to)
            except Exception as e:
                data = None
                rows = Pipeline.objects.none()

        for row in rows:
            row_num += 1
            job_candidate = row.job_candidate
            if job_candidate:
                candidate = job_candidate.candidate
                candidate_name = candidate.name
                candidate_code = candidate.code
            else:
                candidate_name = ''
                candidate_code = ''

            job = row.job_candidate.job
            client = job.client

            values = [
                row.date,
                row.status.name,
                job.reference_number,
                job.date,
                job.position,
                candidate_code,
                candidate_name,
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


class JobToPipelineAnalysisListView(
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Job
    template_name = 'reports/job_to_pipeline_analysis.html'
    permission_required = 'jobs.view_report_job_to_pipeline_analysis'
    paginate_by = 0

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('board', 'client').prefetch_related('pipeline')

        # compute job to pipeline days
        num_of_days_data = []
        for job in q:
            job_date = job.date
            if hasattr(job, 'pipeline'):
                pipeline_date = job.pipeline.date
            else:
                pipeline_date = datetime.date.today()

            num_of_days = pipeline_date - job_date
            num_of_days = num_of_days.days
            job.num_of_days = num_of_days

            num_of_days_data.append(num_of_days)

        total_days = sum(num_of_days_data)
        self.average_num_of_days = total_days / len(num_of_days_data)
        self.max_num_of_days = max(num_of_days_data)
        self.min_num_of_days = min(num_of_days_data)
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['AVERAGE'] = math.ceil(self.average_num_of_days)
        context['MAX'] = self.max_num_of_days
        context['MIN'] = self.min_num_of_days
        return context


class JobToPipelineAnalysisPDFView(
        WeasyTemplateResponseMixin,
        JobToPipelineAnalysisListView):
    template_name = 'reports/pdf/job_to_pipeline_analysis.html'
    pdf_attachment = True
    pdf_filename = 'Job to Pipeline Analysis.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class JobToPipelineAnalysisExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'jobs.view_report_job_to_pipeline_analysis'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = datetime.date.today()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; \
            filename="Job to Pipeline Analysis.xls"'

        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)

        columns = [
            'Reference Number',
            'Client',
            'Position',
            'Job Date',
            'Pipeline Date',
            'Job to Pipeline # of Days',
        ]
        heading_title = 'Job to Pipeline Analysis'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(heading_title)

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        heading = [
            heading_title,
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

        rows = Job.objects.all().select_related('board', 'client')
        rows = rows.prefetch_related('pipeline')

        if date_from and date_to:
            try:
                rows = rows.filter(date__gte=date_from, date__lte=date_to)

                # compute job to pipeline days
                num_of_days_data = []
                for job in rows:
                    job_date = job.date
                    if hasattr(job, 'pipeline'):
                        pipeline_date = job.pipeline.date
                    else:
                        pipeline_date = datetime.date.today()

                    num_of_days = pipeline_date - job_date
                    num_of_days = num_of_days.days
                    job.num_of_days = num_of_days

                    num_of_days_data.append(num_of_days)

                total_days = sum(num_of_days_data)
                AVERAGE = total_days / len(num_of_days_data)
                MAX = max(num_of_days_data)
                MIN = min(num_of_days_data)
            except Exception as e:
                rows = Job.objects.none()

        # right data
        for row in rows:
            row_num += 1
            if hasattr(job, 'pipeline'):
                pipeline_date = job.pipeline.date
            else:
                pipeline_date = datetime.date.today()

            values = [
                row.reference_number,
                row.client.name,
                row.position,
                row.date,
                pipeline_date,
                row.num_of_days
            ]
            for i, value in enumerate(values):
                ws.write(row_num, i, value, font_style)

        # total row
        footer_label_index = 4
        footer = (('AVERAGE', AVERAGE), ('MAX', MAX), ('MIN', MIN))
        for label, value in footer:
            row_num += 1
            ws.write(
                row_num,
                footer_label_index,
                label,
                font_style)
            ws.write(
                row_num,
                footer_label_index + 1,
                math.ceil(value),
                font_style)

        wb.save(response)
        return response
