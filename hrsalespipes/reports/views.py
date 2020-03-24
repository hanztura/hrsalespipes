import calendar
import math
import xlwt

from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View

from django_weasyprint import WeasyTemplateResponseMixin

from .utils import generate_excel
from contacts.models import Employee
from commissions.models import Commission
from jobs.models import Job, JobCandidate
from system.helpers import get_objects_as_choices
from salespipes.models import Pipeline
from system.utils import (
    PermissionRequiredWithCustomMessageMixin, FromToViewFilterMixin,
    MonthFilterViewMixin)
from system.models import Setting


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'


class MonthlyInvoicesSummaryListView(
        MonthFilterViewMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Pipeline
    template_name = 'reports/monthly_invoices_summary.html'
    permission_required = 'salespipes.view_report_monthly_invoices_summary'
    paginate_by = 0
    TITLE = 'Monthly Invoices Summary'

    def get_queryset(self):
        q = super().get_queryset().filter(invoice_amount__gt=0)
        q = q.select_related(
            'job_candidate__job__client',
            'job_candidate__consultant')

        # filter consultant (optional)
        consultant_pk = self.request.GET.get('consultant', '')  # employee id
        self.consultant = None
        if consultant_pk:
            consultant = Employee.objects.filter(id=consultant_pk)
            if consultant.exists():
                self.consultant = consultant.first()
                q = q.filter(
                    job_candidate__consultant=self.consultant)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        sums = q.aggregate(Sum('invoice_amount'), Sum('vat'))

        context['consultant'] = self.consultant
        context['consultant_pk'] = None
        if self.consultant:
            context['consultant_pk'] = self.consultant.pk

        context['consultants'] = get_objects_as_choices(Employee)

        context['TITLE'] = self.TITLE
        context['TOTAL'] = sums['invoice_amount__sum']
        context['VAT'] = sums['vat__sum']
        return context


class MonthlyInvoicesSummaryPDFView(
        WeasyTemplateResponseMixin,
        MonthlyInvoicesSummaryListView):
    template_name = 'reports/pdf/monthly_invoices_summary.html'
    pdf_attachment = True
    pdf_filename = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pdf_filename = '{}.pdf'.format(self.TITLE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class MonthlyInvoicesSummaryExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'salespipes.view_report_monthly_invoices_summary'
    TITLE = 'Monthly Invoices Summary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        self.month = today.strftime('%Y-%m')

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = \
            'attachment; filename="{}.xls"'.format(self.TITLE)

        month = request.GET.get('month', self.month)  # 'YYYY-MM'
        consultant_pk = self.request.GET.get('consultant', '')

        columns = [
            'Date',
            'Invoice Number',
            'Job Reference Number',
            'Client',
            'Industry',
            'Consultant',
            'Invoice Amount',
            'VAT',
        ]
        values_list = [
            'invoice_date',
            'invoice_number',
            'job_candidate__job__reference_number',
            'job_candidate__job__client__name',
            'job_candidate__job__client__industry',
            'job_candidate__candidate__candidate_owner__name',
            'invoice_amount',
            'vat',
        ]

        invoice_amount_index = 6
        wb = generate_excel(
            self.TITLE,
            month,
            month,
            columns,
            Pipeline,
            (
                'job_candidate__job__client',
                'job_candidate__consultant'
            ),
            values_list,
            (
                (invoice_amount_index, 'invoice_amount'),
                (invoice_amount_index + 1, 'vat')
            ),  # aggregate fields
            invoice_amount_index - 1,  # totals label
            is_month_filter=True,
            consultant_id=consultant_pk
        )

        wb.save(response)
        return response


class CommissionsEarnedSummaryListView(
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Commission
    template_name = 'reports/commissions_earned_summary.html'
    permission_required = 'commissions.view_report_commissions_earned_summary'
    paginate_by = 0

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related(
            'pipeline__job_candidate__job',
            'employee')

        # filter employee
        employee_pk = self.request.GET.get('employee', '')  # employee id
        self.employee = None
        if employee_pk:
            employee = Employee.objects.filter(id=employee_pk)
            if employee.exists():
                self.employee = employee.first()
                q = q.filter(employee=self.employee)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        sums = q.aggregate(Sum('amount'))

        context['employee'] = self.employee
        context['employee_pk'] = None
        if self.employee:
            context['employee_pk'] = self.employee.pk

        context['employees'] = get_objects_as_choices(Employee)
        context['TOTAL'] = sums['amount__sum']
        return context


class CommissionsEarnedSummaryPDFView(
        WeasyTemplateResponseMixin,
        CommissionsEarnedSummaryListView):
    template_name = 'reports/pdf/commissions_earned_summary.html'
    pdf_attachment = True
    pdf_filename = 'Commissions Earned Summary.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class CommissionsEarnedSummaryExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'commissions.view_report_commissions_earned_summary'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = \
            'attachment; filename="Commissions Earned Summary.xls"'

        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)
        employee_pk = self.request.GET.get('employee', '')  # employee id

        columns = [
            'Date',
            'Reference Number',
            'Employee',
            'Role Type',
            'Paid?',
            'Amount',
        ]
        values_list = [
            'date',
            'pipeline__job_candidate__job__reference_number',
            'employee__name',
            'rate_role_type',
            'is_paid',
            'amount',
        ]

        wb = generate_excel(
            'Commissions Earned Summary',
            date_from,
            date_to,
            columns,
            Commission,
            ('pipeline__job_candidate__job', 'employee'),
            values_list,
            ((5, 'amount'), ),
            4,
            employee_pk
        )

        wb.save(response)
        return response


class PipelineSummaryListView(
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Pipeline
    template_name = 'reports/pipeline_summary.html'
    permission_required = 'salespipes.view_report_pipeline_summary'
    paginate_by = 0

    def get_queryset(self):
        q = super().get_queryset()

        q = q.select_related(
            'status',
            'job',
            'job_candidate__candidate',
            'job_candidate__job__client',
            'job_candidate__consultant')

        # filter consultant (optional)
        consultant_pk = self.request.GET.get('consultant', '')  # employee id
        self.consultant = None
        if consultant_pk:
            consultant = Employee.objects.filter(id=consultant_pk)
            if consultant.exists():
                self.consultant = consultant.first()
                q = q.filter(
                    job_candidate__consultant=self.consultant)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        aggregate_fields = ['invoice_amount', 'vat', 'potential_income']
        aggregate_fields = [Sum(field) for field in aggregate_fields]
        sums = q.aggregate(*aggregate_fields)

        # create context item for aggregate fields
        for key, value in sums.items():
            context[key] = value

        context['consultant'] = self.consultant
        context['consultant_pk'] = None
        if self.consultant:
            context['consultant_pk'] = self.consultant.pk

        context['consultants'] = get_objects_as_choices(Employee)
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

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; \
            filename="Pipeline Summary.xls"'

        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)

        consultant_pk = self.request.GET.get('consultant', '')

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
            'Consultant',
            'Potential Income',
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
            'status', 'job_candidate__candidate', 'job_candidate__job__client',
            'job_candidate__consultant')

        if date_from and date_to:
            try:
                rows = rows.filter(date__gte=date_from, date__lte=date_to)

                if consultant_pk:
                    consultant = Employee.objects.filter(id=consultant_pk)
                    if consultant.exists():
                        consultant = consultant.first()
                        rows = rows.filter(
                            job_candidate__consultant=consultant)
            except Exception as e:
                rows = Pipeline.objects.none()

        for row in rows:
            row_num += 1
            job_candidate = row.job_candidate
            if job_candidate:
                candidate = job_candidate.candidate
                candidate_name = candidate.name
                candidate_code = candidate.code
                consultant_name = ''
                if hasattr(job_candidate, 'consultant'):
                    consultant_name = job_candidate.consultant.name

            else:
                candidate_name = ''
                candidate_code = ''
                consultant_name = ''

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
                consultant_name,
                row.potential_income,
                row.invoice_date,
                row.invoice_number,
                row.invoice_amount,
                row.vat
            ]

            for i, col in enumerate(columns):
                ws.write(row_num, i, values[i], font_style)

        # total row
        row_num += 1
        total_index = 9
        if rows:
            aggregate_fields = [
                ('invoice_amount', total_index + 1),
                ('vat', total_index + 4),
                ('potential_income', total_index + 5)
            ]
            aggregate_fields_name = [
                Sum(field[0]) for field in aggregate_fields
            ]
            sums = rows.aggregate(*aggregate_fields_name)

            ws.write(
                row_num,
                total_index,
                'TOTAL',
                font_style)

            for field, index in aggregate_fields:
                aggregate_name = '{}__sum'.format(field)
                ws.write(
                    row_num,
                    index,
                    sums[aggregate_name],
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
        q = q.select_related('client')
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

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="jobs-summary.xls"'

        date_from = request.GET.get('from', self.month_first_day)
        date_to = request.GET.get('to', self.month_last_day)

        columns = ['Date', 'Reference Number', 'Client',
                   'Position', 'Location', 'Potential Income', ]
        values_list = [
            'date', 'reference_number', 'client__name',
            'position', 'location', 'potential_income'
        ]

        wb = generate_excel(
            'Jobs Summary',
            date_from,
            date_to,
            columns,
            Job,
            ('client',),
            values_list,
            ((5, 'potential_income'), ),
            4
        )

        wb.save(response)
        return response


class JobToPipelineAnalysisListView(
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = JobCandidate
    template_name = 'reports/job_to_pipeline_analysis.html'
    permission_required = 'jobs.view_report_job_to_pipeline_analysis'
    paginate_by = 0

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('job', 'candidate').prefetch_related('pipeline')
        q = q.filter(pipeline__isnull=False)

        # compute job to pipeline days
        num_of_days_data = []
        for job_candidate in q:
            registration_date = job_candidate.registration_date
            if hasattr(job_candidate, 'pipeline'):
                pipeline_date = job_candidate.pipeline.date
            else:
                pipeline_date = timezone.localdate()

            num_of_days = pipeline_date - registration_date
            num_of_days = num_of_days.days
            job_candidate.num_of_days = num_of_days

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

        today = timezone.localdate()
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
            'Candidate',
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

        rows = JobCandidate.objects.all().select_related('job', 'candidate')
        rows = rows.prefetch_related('pipeline', 'job__client')
        rows = rows.filter(pipeline__isnull=False)

        if date_from and date_to:
            try:
                rows = rows.filter(
                    registration_date__gte=date_from,
                    registration_date__lte=date_to)

                # compute job to pipeline days
                num_of_days_data = []
                for job_candidate in rows:
                    job_date = job_candidate.registration_date
                    if hasattr(job_candidate, 'pipeline'):
                        pipeline_date = job_candidate.pipeline.date
                    else:
                        pipeline_date = timezone.localdate()

                    num_of_days = pipeline_date - job_date
                    num_of_days = num_of_days.days
                    job_candidate.num_of_days = num_of_days

                    num_of_days_data.append(num_of_days)

                total_days = sum(num_of_days_data)
                AVERAGE = total_days / len(num_of_days_data)
                MAX = max(num_of_days_data)
                MIN = min(num_of_days_data)
            except Exception as e:
                rows = JobCandidate.objects.none()

        # right data
        for row in rows:
            row_num += 1
            if hasattr(row, 'pipeline'):
                pipeline_date = row.pipeline.date
            else:
                pipeline_date = timezone.localdate()

            values = [
                row.candidate.name,
                row.job.reference_number,
                row.job.client.name,
                row.job.position,
                row.registration_date,
                pipeline_date,
                row.num_of_days
            ]
            for i, value in enumerate(values):
                ws.write(row_num, i, value, font_style)

        # total row
        footer_label_index = 5
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
