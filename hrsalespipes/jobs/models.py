from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel

from contacts.models import Candidate, Client
from system.models import User, InterviewMode


class Status(models.Model):
    name = models.CharField(max_length=100)
    probability = models.DecimalField(
        max_digits=2, decimal_places=2, blank=True, null=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Job(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    reference_number = models.CharField(
        max_length=100,
        verbose_name=settings.JOB_REFERENCE_NUMBER_ALIAS,
        unique=True)
    date = models.DateField(verbose_name=settings.JOB_DATE_ALIAS)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    position = models.CharField(max_length=100)
    consultant = models.ForeignKey(User, on_delete=models.PROTECT)
    location = models.CharField(max_length=64, blank=True)
    potential_income = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=settings.JOB_POTENTIAL_INCOME_ALIAS)

    def __str__(self):
        return self.reference_number

    def get_absolute_url(self):
        return reverse('jobs:edit', args=[str(self.pk), ])


class JobCandidate(TimeStampedModel):
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
    actual_income = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
        verbose_name=settings.JOB_CANDIDATE_ACTUAL_INCOME_ALIAS)

    def get_absolute_url(self):
        return reverse('jobs:detail',
                       args=[str(self.job_id)])


class Interview(models.Model):
    STATUS_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('A', 'Assessment'),
        ('F', 'Final'))

    job_candidate = models.ForeignKey(
        JobCandidate, on_delete=models.PROTECT, related_name='interviews')
    mode = models.ForeignKey(InterviewMode, on_delete=models.PROTECT)
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
