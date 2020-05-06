import calendar
import math
import xlwt

from django.db.models import Sum, Q, Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, ListView
from django.views.generic.base import View

from django_weasyprint import WeasyTemplateResponseMixin

from .helpers import get_successful_jobs_queryset
from .utils import (
    generate_excel, EmployeeFilterMixin, filter_queryset_by_employee)
from contacts.models import Employee, Client
from commissions.models import Commission
from commissions.views import CommissionListView
from jobs.models import Job, JobCandidate, JobStatus, Interview
from system.helpers import get_objects_as_choices
from salespipes.models import Pipeline
from salespipes.views import PipelineListView
from system.models import Setting, Industry
from system.utils import (
    PermissionRequiredWithCustomMessageMixin, FromToViewFilterMixin,
    MonthFilterViewMixin, DisplayDateFormatMixin, DateAndStatusFilterMixin,
    ContextUrlBuildersMixin)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/index.html'


class StartDatePerWeekMonthListView(
        DisplayDateFormatMixin,
        ContextUrlBuildersMixin,
        MonthFilterViewMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = JobCandidate
    template_name = 'reports/start_date_per_week_month.html'
    permission_required = 'jobs.view_start_date_per_week_month'
    paginate_by = 200
    context_urls_filter_fields = ('month',)
    queryset = JobCandidate.tentative_joining.all()

    TITLE = 'Start date per week/month'

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_start_date_per_week_month')),
            ('excel_url', reverse('reports:excel_start_date_per_week_month')),
        )
        return context_urls

    def get_month_filter_expression(self, month, year):
        filter_expression = Q(
            tentative_date_of_joining__month=month,
            tentative_date_of_joining__year=year) | Q(
            tentative_date_of_joining__isnull=True)
        return filter_expression

    def get_queryset(self):
        q = super().get_queryset().prefetch_related('pipeline')
        q = q.select_related(
            'job__client', 'candidate', 'status', 'associate', 'consultant')
        q = q.order_by(
            'tentative_date_of_joining')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        aggregate_fields = ['pipeline__invoice_amount', ]
        aggregate_fields = [Sum(field) for field in aggregate_fields]
        sums = q.aggregate(*aggregate_fields)

        # create context item for aggregate fields
        for key, value in sums.items():
            context[key] = value

        context['TITLE'] = self.TITLE
        return context


class StartDatePerWeekMonthPDFView(
        WeasyTemplateResponseMixin,
        StartDatePerWeekMonthListView):
    template_name = 'reports/pdf/start_date_per_week_month.html'
    pdf_attachment = True
    pdf_filename = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pdf_filename = '{}.pdf'.format(self.TITLE)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class StartDatePerWeekMonthExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'jobs.view_start_date_per_week_month'
    TITLE = 'Start date per week-month'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        self.month = today.strftime('%Y-%m')

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = \
            'attachment; filename="{}.xls"'.format(self.TITLE)

        month = request.GET.get('month', self.month)  # 'YYYY-MM'
        _year, _month = month.split('-')
        queryset = JobCandidate.tentative_joining.prefetch_related('pipeline')
        queryset = queryset.select_related(
            'job__client', 'candidate', 'status').order_by(
            'tentative_date_of_joining')
        filter_expression = Q(
            tentative_date_of_joining__month=_month,
            tentative_date_of_joining__year=_year) | Q(
            tentative_date_of_joining__isnull=True)

        columns = [
            'Tentative Date of Joining',
            'Status',
            'Candidate',
            'Reference Number',
            'Client',
            'Associate',
            'Consultant',
            'Invoice Number',
            'Invoice Amount',
        ]
        values_list = [
            'tentative_date_of_joining',
            'status__name',
            'candidate__name',
            'job__reference_number',
            'job__client__name',
            'associate__name',
            'consultant__name',
            'pipeline__invoice_number',
            'pipeline__invoice_amount',
        ]

        invoice_amount_index = 8
        wb = generate_excel(
            self.TITLE,
            month,
            month,
            columns,
            JobCandidate,
            (
                'job__client',
                'candidate'
            ),
            values_list,
            (
                (invoice_amount_index, 'pipeline__invoice_amount'),
            ),  # aggregate fields
            invoice_amount_index - 1,  # totals label
            is_month_filter=True,
            user=self.request.user,
            queryset=queryset,
            date_filter_expression=filter_expression,
        )

        wb.save(response)
        return response


class MonthlyInvoicesSummaryListView(
        EmployeeFilterMixin,
        DisplayDateFormatMixin,
        ContextUrlBuildersMixin,
        MonthFilterViewMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Pipeline
    template_name = 'reports/monthly_invoices_summary.html'
    permission_required = 'salespipes.view_report_monthly_invoices_summary'
    paginate_by = 0
    TITLE = 'Monthly Invoices Summary'
    context_urls_filter_fields = ('month', 'consultant')

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_monthly_invoices_summary')),
            ('excel_url', reverse('reports:excel_monthly_invoices_summary')),
        )
        return context_urls

    def get_month_filter_expression(self, month, year):
        filter_expression = Q(
            invoice_date__month=month,
            invoice_date__year=year) | Q(
            invoice_date__isnull=True)
        return filter_expression

    def get_queryset(self):
        q = super().get_queryset().filter(
            invoice_amount__gt=0,
            invoice_number__isnull=False).exclude(invoice_number__exact='')
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
        sums = q.aggregate(
            Sum('invoice_amount'),
            Sum('vat'),
            Sum('potential_income'))

        context['consultant'] = self.consultant
        context['consultant_pk'] = None
        if self.consultant:
            context['consultant_pk'] = self.consultant.pk

        context['consultants'] = get_objects_as_choices(Employee)

        context['TITLE'] = self.TITLE
        context['TOTAL_POTENTIAL_INCOME'] = sums['potential_income__sum']
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
        queryset = Pipeline.objects.filter(
            invoice_amount__gt=0,
            invoice_number__isnull=False).exclude(invoice_number__exact='')

        columns = [
            'Date',
            'Invoice Number',
            'Job Reference Number',
            'Client',
            'Industry',
            'Consultant',
            'Income',
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
            'potential_income',
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
                (invoice_amount_index - 1, 'potential_income'),
                (invoice_amount_index, 'invoice_amount'),
                (invoice_amount_index + 1, 'vat'),
            ),  # aggregate fields
            invoice_amount_index - 2,  # totals label
            is_month_filter=True,
            consultant_id=consultant_pk,
            user=self.request.user,
            queryset=queryset
        )

        wb.save(response)
        return response


class CommissionsEarnedSummaryListView(
        ContextUrlBuildersMixin,
        FromToViewFilterMixin,
        CommissionListView):
    model = Commission
    template_name = 'reports/commissions_earned_summary.html'
    permission_required = 'commissions.view_report_commissions_earned_summary'
    paginate_by = 0
    context_urls_filter_fields = ('from', 'to', 'employee', 'is_paid')

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_commissions_earned_summary')),
            ('excel_url', reverse('reports:excel_commissions_earned_summary')),
        )
        return context_urls

    def get_queryset(self):
        q = super().get_queryset()

        # filter employee
        employee_pk = self.request.GET.get('employee', '')  # employee id
        self.employee = None
        if employee_pk:
            employee = Employee.objects.filter(id=employee_pk)
            if employee.exists():
                self.employee = employee.first()
                q = q.filter(employee=self.employee)

        # filter is_paid
        is_paid = self.request.GET.get('is_paid', '')
        self.is_paid = is_paid
        possible_values = {
            'true': True,
            'false': False
        }
        is_paid = is_paid.split(',') if is_paid else []
        is_paid = [possible_values[p] for p in is_paid]
        if is_paid:
            q = q.filter(is_paid__in=is_paid)

        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        sums = q.aggregate(Sum('amount'))

        context['employee'] = self.employee
        context['search_is_paid'] = self.is_paid
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

        # filter is_paid
        is_paid = self.request.GET.get('is_paid', '')
        self.is_paid = is_paid
        possible_values = {
            'true': True,
            'false': False
        }
        is_paid = is_paid.split(',') if is_paid else []
        is_paid = [possible_values[p] for p in is_paid]

        q = Commission.objects.all()
        if is_paid:
            q = q.filter(is_paid__in=is_paid)

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

        employee = getattr(self.request.user, 'as_employee', None)
        empty_if_no_filter = False
        filter_expression = None
        filter_expression_employee_pk = getattr(employee, 'pk', None)
        if filter_expression_employee_pk:
            filter_expression = Q(employee_id=employee.pk)
            empty_if_no_filter = True

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
            employee_pk,
            user=self.request.user,
            filter_expression=filter_expression,
            empty_if_no_filter=empty_if_no_filter,
            queryset=q
        )

        wb.save(response)
        return response


class PipelineSummaryListView(
        ContextUrlBuildersMixin,
        PipelineListView):
    model = Pipeline
    template_name = 'reports/pipeline_summary.html'
    permission_required = 'salespipes.view_report_pipeline_summary'
    paginate_by = 0
    context_urls_filter_fields = ('from', 'to', 'consultant')

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_pipeline_summary')),
            ('excel_url', reverse('reports:excel_pipeline_summary')),
        )
        return context_urls

    def get_queryset(self):
        q = super().get_queryset()

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

        # filter by employee or allowed all
        rows = filter_queryset_by_employee(rows, self.request.user, Pipeline)

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


class SuccessfulJobsListView(
        PipelineSummaryListView):
    template_name = 'reports/successful_jobs.html'
    permission_required = 'salespipes.view_report_successful_jobs'
    paginate_by = 0
    TITLE = 'Successful Jobs'
    context_urls_filter_fields = ('from', 'to', 'consultant', 'industry')

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_successful_jobs')),
            # ('excel_url', reverse('reports:excel_monthly_invoices_summary')),
        )
        return context_urls

    def get_queryset(self):
        q = self.model.successful_jobs.all()
        q = q.select_related(
            'job_candidate__job__client',
            'job_candidate__consultant')

        # filter consultant (optional)
        consultant_pk = self.request.GET.get('consultant', '')  # employee id
        industry = self.request.GET.get('industry', '')  # string
        self.industry = industry  # industry is charfield
        self.consultant = None
        if consultant_pk:
            consultant = Employee.objects.filter(id=consultant_pk)
            if consultant.exists():
                self.consultant = consultant.first()

        return get_successful_jobs_queryset(
            q, self.date_from, self.date_to, consultant_pk, industry)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['industry'] = self.industry
        context['industries'] = get_objects_as_choices(Industry)

        return context


class SuccessfulJobsPDFView(
        WeasyTemplateResponseMixin,
        SuccessfulJobsListView):
    template_name = 'reports/pdf/successful_jobs.html'
    pdf_attachment = True
    pdf_filename = 'Successful Jobs.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class JobsDetailListView(
        DisplayDateFormatMixin,
        ContextUrlBuildersMixin,
        DateAndStatusFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Job
    template_name = 'reports/jobs_detail.html'
    permission_required = 'jobs.view_report_jobs_detail'
    paginate_by = 20
    context_urls_filter_fields = ('from', 'to', 'status')

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_jobs_detail')),
            # ('excel_url', reverse('reports:excel_monthly_invoices_summary')),
        )
        return context_urls

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('client', 'status')
        q = q.prefetch_related(
            'candidates__candidate', 'candidates__status',
            'candidates__associate', 'candidates__consultant')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_objects'] = get_objects_as_choices(JobStatus)
        return context


class JobsDetailPDFView(
        WeasyTemplateResponseMixin,
        JobsDetailListView):
    template_name = 'reports/pdf/jobs_detail.html'
    pdf_attachment = True
    pdf_filename = 'Jobs Detail.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class JobsSummaryListView(
        DisplayDateFormatMixin,
        ContextUrlBuildersMixin,
        DateAndStatusFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Job
    template_name = 'reports/jobs_summary.html'
    permission_required = 'jobs.view_report_jobs_summary'
    paginate_by = 0
    context_urls_filter_fields = ('from', 'to', 'status')

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('client', 'status')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        sums = q.aggregate(Sum('potential_income'))
        context['potential_income__sum'] = sums['potential_income__sum']
        context['status_objects'] = get_objects_as_choices(JobStatus)
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
        status_pk = request.GET.get('status', '')

        columns = [
            'Date',
            'Status',
            'Reference Number',
            'Client',
            'Position',
            'Location',
            'Potential Income',
        ]
        values_list = [
            'date', 'status__name', 'reference_number', 'client__name',
            'position', 'location', 'potential_income'
        ]

        total_index = 5
        wb = generate_excel(
            'Jobs Summary',
            date_from,
            date_to,
            columns,
            Job,
            ('client',),
            values_list,
            ((total_index + 1, 'potential_income'), ),
            total_index,
            job_status_pk=status_pk
        )

        wb.save(response)
        return response


class JobToPipelineAnalysisListView(
        EmployeeFilterMixin,
        DisplayDateFormatMixin,
        ContextUrlBuildersMixin,
        FromToViewFilterMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = JobCandidate
    template_name = 'reports/job_to_pipeline_analysis.html'
    permission_required = 'jobs.view_report_job_to_pipeline_analysis'
    paginate_by = 0

    # EmployeeFilterMixin
    empty_if_no_filter = True

    def get_filter_expression(self):
        filter_expression = None

        employee = getattr(self.request.user, 'as_employee', None)
        if employee:
            filter_expression = (Q(consultant_id=employee.pk) |
                Q(associate_id=employee.pk))
        return filter_expression

    # FromToViewFilterMixin
    def get_from_to_filter_expression(self, date_from, date_to):
        expression = Q(job__date__gte=date_from, job__date__lte=date_to)
        return expression

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_job_to_pipeline_analysis')),
            ('excel_url', reverse('reports:excel_job_to_pipeline_analysis')),
        )
        return context_urls

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related(
            'job__status', 'candidate').prefetch_related('pipeline')
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
        self.average_num_of_days = 0
        self.max_num_of_days = 0
        self.min_num_of_days = 0
        if total_days != 0:
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
            'Job Status',
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

        rows = JobCandidate.objects.all().select_related(
            'job__status', 'candidate')
        rows = rows.prefetch_related('pipeline', 'job__client')
        rows = rows.filter(pipeline__isnull=False)

        # filter by employee or allowed all
        employee = getattr(self.request.user, 'as_employee', None)
        empty_if_no_filter = False
        filter_expression = None
        filter_expression_employee_pk = getattr(employee, 'pk', None)
        if filter_expression_employee_pk:
            filter_expression = (Q(consultant_id=employee.pk) |
                                 Q(associate_id=employee.pk))
            empty_if_no_filter = True

        rows = filter_queryset_by_employee(
            rows, self.request.user, Pipeline,
            filter_expression, empty_if_no_filter)

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

            job_status = row.job.status
            values = [
                job_status.name if job_status else '',
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
        footer_label_index = 6
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


class InterviewsReportListView(
        EmployeeFilterMixin,
        DisplayDateFormatMixin,
        FromToViewFilterMixin,
        ContextUrlBuildersMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Interview
    template_name = 'reports/interviews.html'
    permission_required = 'jobs.view_report_interviews'
    paginate_by = 0

    # EmployeeFilterMixin
    empty_if_no_filter = True
    all_permission = 'jobs.view_all_interviews'

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_interviews')),
            ('excel_url', reverse('reports:excel_interviews')),
        )
        return context_urls

    def get_filter_expression(self):
        filter_expression = None

        employee = getattr(self.request.user, 'as_employee', None)
        if employee:
            filter_expression = Q(done_by_id=employee.pk)
        return filter_expression

    def get_from_to_filter_expression(self, date_from, date_to):
        expression = Q(date_time__gte=date_from, date_time__lte=date_to)
        return expression

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('job_candidate__candidate', 'mode', 'done_by')
        return q


class InterviewsReportPDFView(
        WeasyTemplateResponseMixin,
        InterviewsReportListView):
    template_name = 'reports/pdf/interviews.html'
    pdf_attachment = True
    pdf_filename = 'Interviews Report.pdf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class InterviewsExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'jobs.view_report_interviews'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Interviews Report.xls"'

        date_from = self.request.GET.get('from', '')
        date_from = date_from if date_from else self.month_first_day

        date_to = self.request.GET.get('to', '')
        date_to = date_to if date_to else self.month_last_day

        columns = [
            'Candidate',
            'Current Location',
            'Nationality',
            'Email Address',
            'Contact Number',
            'Date/Time',
            'Mode',
            'Conducted by',
        ]
        values_list = [
            'job_candidate__candidate__name',
            'job_candidate__candidate__location',
            'job_candidate__candidate__nationality',
            'job_candidate__candidate__email_address',
            'job_candidate__candidate__contact_number',
            'date_time',
            'mode__name',
            'done_by__name',
        ]

        user = self.request.user
        employee = getattr(self.request.user, 'as_employee', None)
        filter_expression = None if not employee else Q(done_by_id=employee.pk)
        wb = generate_excel(
            'Interviews Report',
            date_from,
            date_to,
            columns,
            Interview,
            ('job_candidate__candidate', 'mode', 'done_by'),
            values_list,
            user=user,
            filter_expression=filter_expression,
            empty_if_no_filter=True,
            is_datetime=True
        )

        wb.save(response)
        return response


class CVSentReportListView(
        EmployeeFilterMixin,
        DisplayDateFormatMixin,
        FromToViewFilterMixin,
        ContextUrlBuildersMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = JobCandidate
    template_name = 'reports/cv_sent.html'
    permission_required = 'jobs.view_report_cv_sent'
    paginate_by = 200
    queryset = JobCandidate.cv_sent.all()

    # EmployeeFilterMixin
    empty_if_no_filter = True
    all_permission = 'jobs.view_all_job_candidates'

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_cv_sent')),
            ('excel_url', reverse('reports:excel_cv_sent')),
        )
        return context_urls

    def get_filter_expression(self):
        filter_expression = None

        employee = getattr(self.request.user, 'as_employee', None)
        if employee:
            filter_expression = Q(associate_id=employee.pk) | Q(
                consultant_id=employee.pk)
        return filter_expression

    def get_from_to_filter_expression(self, date_from, date_to):
        expression = Q(
            cv_date_shared__gte=date_from, cv_date_shared__lte=date_to)
        return expression

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related(
            'candidate', 'job__client', 'status', 'associate', 'consultant')
        q = q.order_by('job__client__name')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        aggregates = q.aggregate(Count('id'))

        context['COUNT'] = aggregates['id__count']
        return context


class CVSentReportPDFView(
        WeasyTemplateResponseMixin,
        CVSentReportListView):
    template_name = 'reports/pdf/cv_sent.html'
    pdf_attachment = True
    pdf_filename = 'CV Sent to Clients Report.pdf'
    paginate_by = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class CVSentExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'jobs.view_report_cv_sent'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; \
            filename="CV Sent to Clients Report.xls"'

        date_from = self.request.GET.get('from', '')
        date_from = date_from if date_from else self.month_first_day

        date_to = self.request.GET.get('to', '')
        date_to = date_to if date_to else self.month_last_day

        columns = [
            'Client',
            'CV Source',
            'Date Shared',
            'Candidate',
            'Status',
            'Reference Number',
            'Position',
            'Associate',
            'Consultant',
        ]
        values_list = [
            'job__client__name',
            'cv_source',
            'cv_date_shared',
            'candidate__name',
            'status__name',
            'job__reference_number',
            'job__position',
            'associate__name',
            'consultant__name',
        ]

        user = self.request.user
        employee = getattr(self.request.user, 'as_employee', None)
        filter_expression = Q(consultant_id=employee.pk) | Q(
            associate_id=employee.pk)
        filter_expression = None if not employee else filter_expression
        wb = generate_excel(
            'CV Sent to Clients Report',
            date_from,
            date_to,
            columns,
            JobCandidate,
            ('candidate', 'job__client', 'status', 'associate', 'consultant'),
            values_list,
            user=user,
            filter_expression=filter_expression,
            empty_if_no_filter=True,
            date_filter_expression=Q(
                cv_date_shared__gte=date_from,
                cv_date_shared__lte=date_to),
        )

        wb.save(response)
        return response


class NewlySignedClientsReportListView(
        DisplayDateFormatMixin,
        FromToViewFilterMixin,
        ContextUrlBuildersMixin,
        PermissionRequiredWithCustomMessageMixin,
        ListView):
    model = Client
    template_name = 'reports/newly_signed_clients.html'
    permission_required = 'contacts.view_client'
    paginate_by = 200
    queryset = Client.newly_signed.all()

    def get_context_urls(self):
        # pdf/excel buttons url builder
        context_urls = (
            ('pdf_url', reverse('reports:pdf_newly_signed_clients')),
            ('excel_url', reverse('reports:excel_newly_signed_clients')),
        )
        return context_urls

    def get_from_to_filter_expression(self, date_from, date_to):
        expression = Q(
            signed_on__gte=date_from, signed_on__lte=date_to)
        return expression

    def get_queryset(self):
        q = super().get_queryset()
        q = q.select_related('business_development_person')
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = context['object_list']
        aggregates = q.aggregate(Count('id'))

        context['COUNT'] = aggregates['id__count']
        return context


class NewlySignedClientsPDFView(
        WeasyTemplateResponseMixin,
        NewlySignedClientsReportListView):
    template_name = 'reports/pdf/newly_signed_clients.html'
    pdf_attachment = True
    pdf_filename = 'Newly Signed clients.pdf'
    paginate_by = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['COMPANY'] = Setting.objects.first().company_name
        return context


class NewlySignedClientsExcelView(
        PermissionRequiredWithCustomMessageMixin,
        View):
    permission_required = 'jobs.view_client'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        today = timezone.localdate()
        last_day_of_the_month = calendar.monthrange(today.year, today.month)[1]
        self.month_first_day = str(today.replace(day=1))
        self.month_last_day = str(today.replace(day=last_day_of_the_month))

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; \
            filename="Newly Signed Clients Report.xls"'

        date_from = self.request.GET.get('from', '')
        date_from = date_from if date_from else self.month_first_day

        date_to = self.request.GET.get('to', '')
        date_to = date_to if date_to else self.month_last_day

        columns = [
            'Name',
            'Agreement Term',
            'Agreement Fee',
            'Refund Scheme',
            'Business Development Person',
            'Validity',
            'Signed on',
        ]
        values_list = [
            'name',
            'agreement_term',
            'agreement_fee',
            'refund_scheme',
            'business_development_person__name',
            'validity',
            'signed_on',
        ]

        wb = generate_excel(
            'Newly Signed Clients Report',
            date_from,
            date_to,
            columns,
            Client,
            ('business_development_person',),
            values_list,
            date_filter_expression=Q(
                signed_on__gte=date_from,
                signed_on__lte=date_to),
            queryset=Client.newly_signed.all()
        )

        wb.save(response)
        return response
