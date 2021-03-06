from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from .db import SingletonModel


class User(AbstractUser):
    pass


class Setting(SingletonModel):
    initial_data_runned = models.BooleanField(default=False, blank=True)
    runned_locations_initial_data = models.BooleanField(
        default=False,
        blank=True)
    runned_nationalities_initial_data = models.BooleanField(
        default=False,
        blank=True)
    vat_rate = models.DecimalField(
        max_digits=2, decimal_places=2, default=0.05)
    company_name = models.CharField(max_length=128, blank=True)
    display_date_format = models.CharField(
        max_length=50,
        choices=(
            ('d M Y', '01 Jan 2020'),
            ('d F Y', '01 January 2020'),
            ('M d, Y', 'Jan 01, 2020'),
            ('F d, Y', 'January 01, 2020'),
        ),
        default='d M Y'
    )
    project_label = models.CharField(max_length=50, blank=True)
    cv_label = models.CharField(max_length=50, default='CV')
    newly_signed_clients_number_of_days = models.PositiveSmallIntegerField(
        default=7)

    def __str__(self):
        return 'System Wide Settings'

    def get_project_label(self):
        default = settings.PROJECT_NAME
        return self.project_label if self.project_label else default


class VisaStatus(models.Model):

    class Meta:
        verbose_name_plural = 'Visa Status'

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = 'Nationalities'
        ordering = 'name',

    def __str__(self):
        return self.name


class InterviewMode(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Industries'
        ordering = 'name',

    def __str__(self):
        return self.name
