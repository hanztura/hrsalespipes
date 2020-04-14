from django.db import models

from .utils import custom_permissions
from system.db import SingletonModel


class Dashboard(SingletonModel):

    class Meta:
        permissions = custom_permissions
        verbose_name = 'Dashboard Settings'
        verbose_name_plural = 'Dashboard Settings'

    consultant_leaderboard_dashboard_this_month_label = models.CharField(
        max_length=100,
        blank=True,
        default='Total NFI generated per consultant this month')
    consultant_leaderboard_dashboard_ytd_label = models.CharField(
        max_length=100,
        blank=True,
        default='Total NFI generated per consultant YTD')
    consultant_leaderboard_dashboard_last_12_months_label = models.CharField(
        max_length=100,
        blank=True,
        default='Total NFI generated per consultant last 12 months')
    ytd_client_performance_label = models.CharField(
        max_length=100,
        blank=True,
        default='YTD Client Performance')
    ytd_industry_performance_label = models.CharField(
        max_length=100,
        blank=True,
        default='YTD Industry Performance')
    sjpc_this_month_label = models.CharField(
        max_length=100,
        blank=True,
        default='Successful job placements per consultant this month')
    sjpc_ytd_label = models.CharField(
        max_length=100,
        blank=True,
        default='Successful job placements per consultant YTD')
    sjatpi_label = models.CharField(
        max_length=100,
        blank=True,
        default='Successful job placements per industry')

    def __str__(self):
        return 'Dashboard settings'
