from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from contacts.models import Candidate, Client, Employee
from system.models import InterviewMode


class Status(models.Model):
    """Status to be used by the candidate"""
    class Meta:
        verbose_name = 'Job Candidate Status'
        verbose_name_plural = 'Job Candidate Status'
        ordering = 'probability', 'name'

    name = models.CharField(max_length=100)
    probability = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)
    should_create_pipeline = models.BooleanField(
        default=False,
        verbose_name='should create pipeline if selected')

    def __str__(self):
        return self.name


class JobStatus(models.Model):
    """Status to be used by Job"""
    class Meta:
        verbose_name_plural = 'Job Status'
        ordering = 'order',

    name = models.CharField(max_length=100)
    is_job_open = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False, blank=True)
    order = models.PositiveSmallIntegerField(
        help_text='Display order. 1 positioned at the top',
        unique=True)

    def __str__(self):
        return self.name

    @property
    def job_is_closed(self):
        return not self.is_job_open

    @classmethod
    def get_active_status_as_list(cls):
        status = cls.objects.filter(is_job_open=True).values_list('id')
        status = [str(s[0]) for s in status]
        return status


class Job(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reference_number = models.CharField(
        max_length=100,
        verbose_name=settings.JOB_REFERENCE_NUMBER_ALIAS)
    date = models.DateField(verbose_name=settings.JOB_DATE_ALIAS)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=64, blank=True)
    potential_income = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=settings.JOB_POTENTIAL_INCOME_ALIAS)
    status = models.ForeignKey(
        JobStatus,
        on_delete=models.PROTECT,
        null=True,
        blank=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ['-date', '-reference_number']
        permissions = [
            (
                'view_report_jobs_summary',
                'Can view report Jobs Summary'
            ),
            (
                'view_report_job_to_pipeline_analysis',
                'Can view report Job to Pipeline Analysis'
            ),
            (
                'view_report_interviews',
                'Can view report Interviews'
            ),
            (
                'can_edit_closed_job',
                'Can edit closed Job'
            ),
        ]

    def __str__(self):
        return self.reference_number

    @property
    def edit_href(self):
        return reverse('jobs:edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('jobs:detail', args=[str(self.pk), ])

    @property
    def closed_job_msg(self):
        return 'Job is closed, and your account is not allowed to edit. \
                Please contact your admin if you wish to continue.'

    def get_absolute_url(self):
        return self.edit_href


class JobCandidate(TimeStampedModel):
    class Meta:
        ordering = ['-registration_date', 'job', 'candidate__name']
        permissions = [
            (
                'view_all_job_candidates',
                'Can view all Job Candidates'
            ),
        ]

    job = models.ForeignKey(
        Job, on_delete=models.PROTECT, related_name='candidates')
    candidate = models.ForeignKey(
        Candidate, on_delete=models.PROTECT, related_name='jobs')
    registration_date = models.DateField()
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    cv_source = models.CharField(
        max_length=100,
        blank=True)
    cv_date_shared = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    salary_offered_currency = models.CharField(max_length=3, blank=True)
    salary_offered = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        null=True,
        blank=True)
    tentative_date_of_joining = models.DateField(null=True, blank=True)
    associate = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='as_associate',
        null=True,
        blank=True)
    consultant = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='as_consultant',
        null=True,
        blank=True)

    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('jobs:detail',
                       args=[str(self.job_id)])

    @property
    def job_view_href(self):
        return reverse(
            'jobs:detail',
            args=[str(self.job_id)])

    @property
    def edit_href(self):
        return reverse(
            'jobs:candidates_edit',
            args=[str(self.job_id),
                  str(self.pk)])

    @property
    def view_href(self):
        return reverse(
            'jobs:candidates_detail',
            args=[str(self.job_id),
                  str(self.pk)])


class Interview(models.Model):
    STATUS_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('A', 'Assessment'),
        ('F', 'Final'))

    job_candidate = models.ForeignKey(
        JobCandidate, on_delete=models.PROTECT, related_name='interviews')
    mode = models.ForeignKey(InterviewMode, on_delete=models.PROTECT)
    date_time = models.DateTimeField(default=timezone.localtime)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    done_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='interviews',
        null=True,
        blank=True)

    class Meta:
        ordering = ['-date_time', 'job_candidate']
        permissions = [
            (
                'view_all_interviews',
                'Can view all Interviews'
            ),
        ]
