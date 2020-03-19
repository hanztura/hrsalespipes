import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags import humanize
from django.db.models import Q, Sum
from django.views.generic import TemplateView

from .utils import custom_permissions, template_names
from salespipes.models import Pipeline


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    dashboard_index = None  # 1 2 3 4

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        # set up dashboard allowed for the user
        user = self.request.user
        dashboard_three = 'dashboard.{}'.format(custom_permissions[0][0])
        dashboard_two = 'dashboard.{}'.format(custom_permissions[1][0])
        dashboard_one = 'dashboard.{}'.format(custom_permissions[2][0])
        if user.has_perm(dashboard_three):
            self.dashboard_index = 0
        elif user.has_perm(dashboard_two):
            self.dashboard_index = 1
        elif user.has_perm(dashboard_one):
            self.dashboard_index = 2
        else:
            self.dashboard_index = 3

    def get_template_names(self):
        return [template_names[self.dashboard_index]]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # prepare data for dashboard items
        dashboard_items_number = []
        if self.dashboard_index in [1, 2]:  # dashboard for One or Two user
            employee = None
            if hasattr(user, 'as_employee'):
                employee = user.as_employee

            pipelines = Pipeline.objects.all().select_related('status')

            if employee:
                employee_pipelines = pipelines.filter(
                    Q(job_candidate__associate_id=employee.pk) |
                    Q(job_candidate__consultant_id=employee.pk)
                )

                active_jobs = employee_pipelines.filter(
                    status__is_closed=False)

                # compute amount of successful jobs
                today = datetime.date.today()
                successful_jobs = employee_pipelines.filter(
                    status__probability__gte=1)
                successful_jobs = employee_pipelines.filter(
                    successful_date__month=today.month,
                    successful_date__year=today.year)

                total_potential_income = successful_jobs.aggregate(
                    Sum('potential_income'))['potential_income__sum']
                tpi = total_potential_income if total_potential_income else 0

                # compute amount of successful jobs last  month
                first_day = today.replace(day=1)
                last_month = first_day - datetime.timedelta(days=1)
                successful_jobs_last_month = employee_pipelines.filter(
                    successful_date__month=last_month.month,
                    successful_date__year=last_month.year)

                tpi_last_month = successful_jobs_last_month.aggregate(
                    Sum('potential_income'))['potential_income__sum']
                tpi_last_month = tpi_last_month if tpi_last_month else 0

            else:  # if user is not employee
                null_pipeline = Pipeline.objects.none()
                active_jobs = null_pipeline
                successful_jobs = null_pipeline
                tpi = 0
                tpi_last_month = 0

            data = [
                {
                    'type': 'number',  # number, graph
                    'title': 'Active jobs',
                    'value': active_jobs.count()
                },
                {
                    'type': 'number',
                    'title': 'Succesful jobs this month',
                    'value': successful_jobs.count()
                },
                {
                    'type': 'number',
                    'title': 'NFI generated this month',
                    'value': humanize.intcomma(
                        round(float(tpi))
                    )
                },
                {
                    'type': 'number',
                    'title': 'NFI generated last month',
                    'value': humanize.intcomma(
                        round(float(tpi_last_month))
                    )
                },
            ]
            dashboard_items_number += data

        elif self.dashboard_index == 0:  # dashboard for Three user
            pass

        context['dashboard_items_number'] = json.dumps(dashboard_items_number)
        return context
