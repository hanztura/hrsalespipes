from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from .helpers import SuccessfulJobsManager
from jobs.models import Job, JobCandidate, Status as JobStatus


class Status(models.Model):
    class Meta:
        verbose_name_plural = 'Status'
    name = models.CharField(max_length=100)
    probability = models.DecimalField(max_digits=3, decimal_places=2)
    job_status = models.OneToOneField(
        JobStatus,
        on_delete=models.PROTECT,
        related_name='related_pipeline_status',
        verbose_name='equivalent job status',
        null=True)
    should_have_invoice = models.BooleanField(default=False, blank=True)
    is_closed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class Pipeline(TimeStampedModel):

    class Meta:
        permissions = [
            (
                'view_report_pipeline_summary',
                'Can view report Pipeline Summary'
            ),
            (
                'view_report_pipeline_details',
                'Can view report Pipeline Details'
            ),
            (
                'view_report_monthly_invoices_summary',
                'Can view report Monthly Invoices Summary'
            ),
            (
                'view_report_successful_jobs',
                'Can view report on Successful Jobs'
            ),
            (
                'view_all_pipelines',
                'Can view all Pipeline records'
            ),
        ]
        ordering = ['-date', '-job']

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateField(
        verbose_name=settings.PIPELINE_DATE_ALIAS,
        default=timezone.localdate)

    # successful date DEPRECIATED!!!
    # successful_date = models.DateField(null=True, blank=True)
    job = models.OneToOneField(  # DEPRECIATED!!!
        Job,
        on_delete=models.PROTECT,
        related_name='pipeline',
        null=True,
        blank=True)
    job_candidate = models.OneToOneField(
        JobCandidate,
        on_delete=models.PROTECT,
        related_name='pipeline',
        null=True)
    recruitment_term = models.DecimalField(
        max_digits=15, decimal_places=5, default=1.0, blank=True)
    recruitment_rate = models.DecimalField(
        max_digits=11, decimal_places=10, default=0.0, blank=True)
    base_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, blank=True)
    potential_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_number = models.CharField(
        max_length=50,
        blank=True)
    invoice_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0)
    vat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True)

    history = HistoricalRecords()

    objects = models.Manager()
    successful_jobs = SuccessfulJobsManager()

    @property
    def candidate(self):
        candidates = self.job.candidates.all()
        candidates = candidates.filter(status__probability__gte=1)
        if candidates.exists():
            candidate = candidates.first()
        else:
            candidate = None

        return candidate

    @property
    def edit_href(self):
        return reverse('salespipes:edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('salespipes:detail', args=[str(self.pk), ])

    @property
    def computed_potential_income(self):
        term = self.recruitment_term
        rate = self.recruitment_rate
        base_amount = self.base_amount
        return term * rate * base_amount

    def get_absolute_url(self):
        return self.edit_href


class Target(TimeStampedModel):
    date = models.DateField()
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return '{} - {}'.format(self.date, self.amount)
