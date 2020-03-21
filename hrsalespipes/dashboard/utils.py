import datetime
from django.db.models import Q, Sum, Count


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


def get_data_dashboard_items_number(all_pipelines, employee=None):
    pipelines = all_pipelines
    if employee:
        pipelines = pipelines.filter(
            Q(job_candidate__associate_id=employee.pk) |
            Q(job_candidate__consultant_id=employee.pk)
        )
        pipelines_for_sjpc = pipelines.filter(
            job_candidate__consultant_id=employee.pk)

    active_jobs = pipelines.filter(
        status__is_closed=False)

    # compute amount of successful jobs
    today = datetime.date.today()
    successful_jobs_all_time = pipelines.filter(
        status__probability__gte=1)
    successful_jobs = successful_jobs_all_time.filter(
        successful_date__month=today.month,
        successful_date__year=today.year)

    # this month's potential income
    total_potential_income = successful_jobs.aggregate(
        Sum('potential_income'))['potential_income__sum']
    tpi = total_potential_income if total_potential_income else 0

    # compute amount of successful jobs last  month
    first_day = today.replace(day=1)
    last_month = first_day - datetime.timedelta(days=1)
    successful_jobs_last_month = pipelines.filter(
        successful_date__month=last_month.month,
        successful_date__year=last_month.year)

    tpi_last_month = successful_jobs_last_month.aggregate(
        Sum('potential_income'))['potential_income__sum']
    tpi_last_month = tpi_last_month if tpi_last_month else 0

    # successful jobs per industry, all time
    field_lookup = 'job_candidate__job__client__industry'
    sjatpi = successful_jobs_all_time.values(
        field_lookup).annotate(value=Count('id'))
    sjatpi = sjatpi.order_by(field_lookup)
    sjatpi = [s for s in sjatpi]

    # successful jobs per consultant. this month
    sjpc = pipelines_for_sjpc.filter(
        status__probability__gte=1)
    sjpc = sjpc.filter(
        successful_date__month=today.month,
        successful_date__year=today.year)
    sjpc = sjpc.values('job_candidate__consultant__name')
    sjpc = sjpc.annotate(value=Count('id')).order_by(
        'job_candidate__consultant_name')
    sjpc = [s for s in sjpc]

    return (
        active_jobs,
        successful_jobs,
        tpi,
        tpi_last_month,
        sjatpi,
        sjpc
    )
