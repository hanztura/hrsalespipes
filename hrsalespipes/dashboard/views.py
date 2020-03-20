import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags import humanize
from django.db.models import Q, Sum, Count
from django.views.generic import TemplateView

from .utils import (
    custom_permissions, template_names, get_data_dashboard_items_number)
from jobs.models import Interview
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

        # queryset to be used by dashboard items
        all_pipelines = Pipeline.objects.all().select_related(
            'status', 'job_candidate__job__client')
        all_interviews = Interview.objects.all().select_related(
            'job_candidate__associate', 'job_candidate__consultant')

        # prepare data for dashboard items
        dashboard_items_number = []
        if self.dashboard_index in [1, 2, 0]:  # dashboard for One Two Three

            if self.dashboard_index == 0:  # Three Dashboard
                context['data_note'] = \
                    'All employees\' data are used in this dashboard.'

                active_jobs, successful_jobs, tpi, tpi_last_month, sjatpi = get_data_dashboard_items_number(all_pipelines)
            else:  # One Two dashboard
                employee = None
                if hasattr(user, 'as_employee'):
                    employee = user.as_employee

                if employee:
                    active_jobs, successful_jobs, tpi, tpi_last_month, sjatpi = get_data_dashboard_items_number(all_pipelines, employee)

                    # interview data
                    all_interviews = all_interviews.filter(done_by=employee)
                else:
                    null_pipeline = Pipeline.objects.none()
                    active_jobs = null_pipeline
                    successful_jobs = null_pipeline
                    tpi = 0
                    tpi_last_month = 0
                    sjatpi = []
                    all_interviews = Interview.objects.none()

            # prepare to be included in context
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
                    'title': 'Interviews Arranged',
                    'value': round(float(all_interviews.count()))
                },
                {
                    'type': 'number',
                    'title': 'NFI generated this month',
                    'value': round(float(tpi))
                },
                {
                    'type': 'number',
                    'title': 'NFI generated last month',
                    'value': round(float(tpi_last_month))
                },
            ]

            dashboard_items_number += data

        sjatpi = {
            'type': 'graph',
            'title': 'Successful jobs per industry',
            'value': sjatpi
        }

        context['sjatpi'] = json.dumps(sjatpi)
        context['dashboard_items_number'] = json.dumps(dashboard_items_number)
        return context
