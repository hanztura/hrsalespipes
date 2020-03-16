from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel

from contacts.models import Candidate, Client, Employee
from system.models import InterviewMode


class Status(models.Model):
    name = models.CharField(max_length=100)
    probability = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True)
    should_create_pipeline = models.BooleanField(
        default=False,
        verbose_name='should create pipeline if selected')

    def __str__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Job Board'

    def __str__(self):
        return self.name


class Job(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    board = models.ForeignKey(
        Board,
        on_delete=models.PROTECT,
        null=True,
        verbose_name='Job Board')
    reference_number = models.CharField(
        max_length=100,
        verbose_name=settings.JOB_REFERENCE_NUMBER_ALIAS,
        unique=True)
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

    class Meta:
        ordering = ['-date', '-reference_number']
        permissions = [
            (
                'view_report_jobs_summary',
                'Can view report Jobs Summary'
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

    def get_absolute_url(self):
        return self.edit_href


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
    associate = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='as_associate')

    class Meta:
        ordering = ['-registration_date', 'job', 'candidate__name']

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

    class Meta:
        ordering = ['-date', 'job_candidate']
