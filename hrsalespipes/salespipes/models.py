from uuid import uuid4

from django.conf import settings
from django.db import models

from django_extensions.db.models import TimeStampedModel

from jobs.models import JobCandidate


class Status(models.Model):
    name = models.CharField(max_length=100)
    probability = models.DecimalField(max_digits=2, decimal_places=2)

    def __str__(self):
        return self.name


class Pipeline(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateField(verbose_name=settings.PIPELINE_DATE_ALIAS)
    job_candidate = models.ForeignKey(JobCandidate, on_delete=models.PROTECT)
    invoice_date = models.DateField(blank=True)
    recruitment_term = models.CharField(max_length=100, blank=True)
    recruitment_rate = models.DecimalField(
        max_digits=2, decimal_places=2, blank=True)
    base_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True)
    potential_income = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, blank=True)
    invoice_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True)
    vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
