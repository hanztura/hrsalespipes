import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from dateutil.relativedelta import relativedelta

from .utils import (
    custom_permissions, template_names, get_data_dashboard_items_number)
from .models import Dashboard
from jobs.models import Interview, JobCandidate, Job
from salespipes.models import Pipeline
from system.utils import ContextFromToMixin


class DashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'


class DashboardView(
    ContextFromToMixin,
    LoginRequiredMixin,
    TemplateView):
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
        all_job_candidates = JobCandidate.objects.all()
        all_jobs = Job.objects.all().select_related('status')

        # prepare data for dashboard items
        dashboard_items_number = []
        if self.dashboard_index in [1, 2, 0]:  # dashboard for One Two Three

            # cv shared to client
            cv_sent_to_clients = all_job_candidates.filter(
                cv_date_shared__isnull=False)
            if self.dashboard_index == 0:  # Three Dashboard
                context['data_note'] = \
                    'All employees\' data are used in this dashboard.'

                (active_jobs, successful_jobs,
                 tpi, tpi_last_month,
                 sjatpi, sjpc, tnfipc,
                 tnfipcp12m, ytdcp) = get_data_dashboard_items_number(
                    all_pipelines, all_jobs=all_jobs)
            else:  # One Two dashboard
                context['data_note'] = \
                    'Only your data are used in this dashboard. \
                     Unless not applicable'
                employee = None
                if hasattr(user, 'as_employee'):
                    employee = user.as_employee

                if employee:
                    (active_jobs, successful_jobs,
                     tpi, tpi_last_month,
                     sjatpi, sjpc, tnfipc,
                     tnfipcp12m, ytdcp) = get_data_dashboard_items_number(
                        all_pipelines, employee=employee, all_jobs=all_jobs)

                    # interview data
                    all_interviews = all_interviews.filter(done_by=employee)
                    cv_sent_to_clients = cv_sent_to_clients.filter(
                        Q(associate=employee) | Q(consultant=employee))
                else:
                    null_pipeline = Pipeline.objects.none()
                    active_jobs = null_pipeline
                    successful_jobs = null_pipeline
                    tpi = 0
                    tpi_last_month = 0
                    sjatpi = []
                    sjpc = []
                    tnfipc = []
                    tnfipcp12m = []
                    ytdcp = []
                    all_interviews = Interview.objects.none()
                    cv_sent_to_clients = JobCandidate.objects.none()

            # prepare to be included in context
            data = [
                {
                    'type': 'number',  # number, graph
                    'title': 'Active jobs',
                    'value': active_jobs.count(),
                    'icon': 'mdi-briefcase-account'
                },
                {
                    'type': 'number',
                    'title': 'Succesful job placements this month',
                    'value': successful_jobs.count(),
                    'icon': 'mdi-briefcase-account'
                },
                {
                    'type': 'number',
                    'title': 'Interviews Arranged',
                    'value': round(float(all_interviews.count())),
                    'icon': 'mdi-briefcase-check'
                },
                {
                    'type': 'number',
                    'title': 'CVs sent to clients',
                    'value': round(float(cv_sent_to_clients.count())),
                    'icon': 'mdi-send-check'
                },
                {
                    'type': 'number',
                    'title': 'NFI generated this month',
                    'value': round(float(tpi)),
                    'icon': 'mdi-calendar-month'
                },
                {
                    'type': 'number',
                    'title': 'NFI generated last month',
                    'value': round(float(tpi_last_month)),
                    'icon': 'mdi-calendar-import'
                },
            ]

            dashboard_items_number += data

            from_to_url_params_this_month = '?from{}&to={}'.format(
                self.month_first_day,
                self.month_last_day)
            successful_jobs_url = reverse('reports:successful_jobs')
            sjatpi_url = '{}?from=ALL&to=ALL'.format(successful_jobs_url)
            sjpc_url = '{}{}'.format(
                successful_jobs_url,
                from_to_url_params_this_month)
            tnfipc_url = '{}{}'.format(
                successful_jobs_url,
                from_to_url_params_this_month)

            today = timezone.localdate()
            first_day = today.replace(day=1)
            last_month = first_day - relativedelta(days=1)
            past_12_month = today - relativedelta(months=12)

            from_to_url_params_last_12_months = '?from={}&to={}'.format(
                past_12_month.replace(day=1),
                last_month)
            tnfipcp12m_url = '{}{}'.format(
                successful_jobs_url,
                from_to_url_params_last_12_months)

            from_to_url_params_ytd = '?from={}&to={}'.format(
                today.replace(month=1, day=1),
                today)
            ytdcp_url = '{}{}'.format(
                successful_jobs_url,
                from_to_url_params_ytd)

            dashboard_settings = Dashboard.load()
            dashboard_items_graph = [
                {
                    'code': 'sjatpi',
                    'type': 'graph',
                    'title': dashboard_settings.sjatpi_label,
                    'value': sjatpi,
                    'url': sjatpi_url
                },
                {
                    'code': 'sjpc',
                    'type': 'graph',
                    'title': dashboard_settings.sjpc_this_month_label,
                    'value': sjpc,
                    'url': sjpc_url
                },
                {
                    'code': 'tnfipc',
                    'type': 'graph',
                    'title': getattr(
                        dashboard_settings,
                        'consultant_leaderboard_dashboard_this_month_label',
                        ''),
                    'value': tnfipc,
                    'url': tnfipc_url
                },
                {
                    'code': 'tnfipcp12m',
                    'type': 'graph',
                    'title': getattr(
                        dashboard_settings,
                        'consultant_leaderboard_dashboard_last_12_months_label',
                        ''),
                    'value': tnfipcp12m,
                    'url': tnfipcp12m_url
                },
                {
                    'code': 'ytdcp',
                    'type': 'graph',
                    'title': dashboard_settings.ytd_client_performance_label,
                    'value': ytdcp,
                    'url': ytdcp_url
                }
            ]

            for graph_item in dashboard_items_graph:
                context[graph_item['code']] = json.dumps(graph_item)

        context['dashboard_items_number'] = json.dumps(dashboard_items_number)
        return context
