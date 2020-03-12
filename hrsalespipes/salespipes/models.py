import datetime
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel

from jobs.models import Job, Status as JobStatus


class Status(models.Model):
    name = models.CharField(max_length=100)
    probability = models.DecimalField(max_digits=3, decimal_places=2)
    job_status = models.OneToOneField(
        JobStatus,
        on_delete=models.PROTECT,
        related_name='related_pipeline_status',
        verbose_name='equivalent job status',
        null=True)

    def __str__(self):
        return self.name


class Pipeline(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateField(
        verbose_name=settings.PIPELINE_DATE_ALIAS,
        default=datetime.date.today)
    job = models.OneToOneField(
        Job,
        on_delete=models.PROTECT,
        related_name='pipeline')
    invoice_date = models.DateField(null=True, blank=True)
    recruitment_term = models.CharField(max_length=100, blank=True)
    recruitment_rate = models.DecimalField(
        max_digits=2, decimal_places=2, default=0, blank=True)
    base_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True)
    potential_income = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
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

    def get_absolute_url(self):
        return reverse('salespipes:edit', args=[str(self.pk), ])
