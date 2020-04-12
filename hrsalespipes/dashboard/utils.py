import datetime

from django.db.models import Q, Sum, Count
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from reports.helpers import get_successful_jobs_queryset
from system.helpers import get_last_day_of_month


custom_permissions = [
    (
        'view_dashboard_type_three',
        'Can view Dashboard Type Three'
    ),
    (
        'view_dashboard_type_two',
        'Can view Dashboard Type Two'
    ),
    (
        'view_dashboard_type_one',
        'Can view Dashboard Type One'
    ),
]

template_names = (
    'dashboard/dashboard_three.html',
    'dashboard/dashboard_two.html',
    'dashboard/dashboard_one.html',
    'dashboard/index.html'
)


def get_data_dashboard_items_number(
        all_pipelines, employee=None, all_jobs=None):
    pipelines = all_pipelines
    if employee:
        pipelines = pipelines.filter(
            Q(job_candidate__associate_id=employee.pk) |
            Q(job_candidate__consultant_id=employee.pk)
        )

    active_jobs = all_jobs.filter(
        status__is_job_open=True)

    # compute amount of SUCCESSFUL JOB PLACEMENTS
    today = timezone.localdate()
    successful_jobs_all_time = get_successful_jobs_queryset(
        pipelines, date_from="ALL", date_to="ALL")
    successful_jobs = successful_jobs_all_time.filter(
        invoice_date__month=today.month,
        invoice_date__year=today.year)

    # this month's potential income
    total_potential_income = successful_jobs.aggregate(
        Sum('potential_income'))['potential_income__sum']
    tpi = total_potential_income if total_potential_income else 0

    # compute amount of successful jobs last  month
    first_day = today.replace(day=1)
    first_day_this_year = today.replace(day=1, month=1)
    last_month = first_day - datetime.timedelta(days=1)
    successful_jobs_ytd = successful_jobs_all_time.filter(
        invoice_date__gte=first_day_this_year,
        invoice_date__lte=today)
    successful_jobs_last_month = successful_jobs_all_time.filter(
        invoice_date__month=last_month.month,
        invoice_date__year=last_month.year)

    tpi_last_month = successful_jobs_last_month.aggregate(
        Sum('potential_income'))['potential_income__sum']
    tpi_last_month = tpi_last_month if tpi_last_month else 0

    # compute amount of successful jobs
    tpi_ytd = successful_jobs_ytd.aggregate(
        Sum('potential_income'))['potential_income__sum']
    tpi_ytd = tpi_ytd if tpi_ytd else 0

    # successful jobs per industry, all time
    field_lookup = 'job_candidate__job__client__industry'
    sjatpi = successful_jobs_all_time.values(
        field_lookup).annotate(value=Count('id'))
    sjatpi = sjatpi.order_by(field_lookup)
    sjatpi = [s for s in sjatpi]

    sj_per_consultant_all_time = successful_jobs_all_time
    if employee:
        sj_per_consultant_all_time = sj_per_consultant_all_time.filter(
            job_candidate__consultant_id=employee.pk)
    # successful jobs per consultant. this month
    sj_per_consultant = sj_per_consultant_all_time.filter(
        invoice_date__month=today.month,
        invoice_date__year=today.year)
    key_field = 'job_candidate__consultant__name'
    sjpc = sj_per_consultant.values(
        key_field)
    sjpc = sjpc.annotate(value=Count('id')).order_by(
        key_field)
    sjpc = [s for s in sjpc]

    # total NFI per consultant this.month
    tnfipc = sj_per_consultant.values(key_field)
    tnfipc = tnfipc.annotate(value=Sum('potential_income')).order_by(key_field)
    tnfipc = [
        {key_field: s[key_field], 'value': float(s['value'])} for s in tnfipc
    ]

    # total NFI per consultant for the last 12 months
    past_12_month = today - relativedelta(months=12)
    tnfipcp12m = get_successful_jobs_queryset(
        sj_per_consultant_all_time,
        date_from=past_12_month.replace(day=1),
        date_to=last_month)
    tnfipcp12m = tnfipcp12m.values(key_field)
    tnfipcp12m = tnfipcp12m.annotate(value=Sum('potential_income')).order_by(
        key_field)  # order by jobconsultant name
    tnfipcp12m = [
        {key_field: s[key_field], 'value': float(s['value'])} for s in tnfipcp12m
    ]

    # YTD client performance
    year_beginning = today.replace(month=1, day=1)
    ytdcp = get_successful_jobs_queryset(
        successful_jobs_all_time, date_from=year_beginning, date_to=today)
    ytdcp = ytdcp.values(
        'job_candidate__job__client',
        'job_candidate__job__client__name',
        'job_candidate__cv_source')
    ytdcp = ytdcp.annotate(value=Sum('potential_income')).order_by(
        'job_candidate__job__client__name')
    ytdcp = [
        {
            'id': str(s['job_candidate__job__client']),
            'client': s['job_candidate__job__client__name'],
            'cvSource': s['job_candidate__cv_source'],
            'value': float(s['value'])
        } for s in ytdcp
    ]

    return (
        active_jobs,
        successful_jobs,
        tpi,
        tpi_last_month,
        tpi_ytd,
        sjatpi,
        sjpc,
        tnfipc,
        tnfipcp12m,
        ytdcp,
    )
