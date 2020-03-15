from django.db import models
from django.urls import reverse

from .utils import ContactModel

from system.models import User, VisaStatus


class Client(ContactModel):
    industry = models.CharField(max_length=64)
    location = models.CharField(max_length=64, blank=False)
    initial_approach = models.TextField(blank=True)
    meeting_arranged = models.TextField(blank=True)
    agreement_terms = models.CharField(max_length=200, blank=True)
    agreement_fee = models.DecimalField(
        max_digits=2, decimal_places=2, blank=True, null=True)
    refund_scheme = models.TextField(blank=True)
    validity = models.DateField(null=True, blank=True)

    @property
    def edit_href(self):
        return reverse('contacts:clients_edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('contacts:clients_detail', args=[str(self.pk), ])

    def get_absolute_url(self):
        return self.edit_href


class Supplier(ContactModel):

    class Meta:
        abstract = False

    @property
    def edit_href(self):
        return reverse('contacts:suppliers_edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('contacts:suppliers_detail', args=[str(self.pk), ])

    def get_absolute_url(self):
        return self.edit_href


class Employee(ContactModel):

    class Meta:
        abstract = False

    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name='as_employee',
        null=True,
        blank=True)

    def __str__(self):
        return self.name


class Candidate(ContactModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'))
    CIVIL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('D', 'Divorced'),
        ('Se', 'Separated'))

    # work history
    current_previous_position = models.CharField(max_length=200, blank=True, verbose_name='position')
    current_previous_company = models.CharField(max_length=200, blank=True, verbose_name='company')
    current_previous_salary_and_benefits = models.TextField(blank=True, verbose_name='salary and benefits')
    motivation_for_leaving = models.TextField(blank=True)

    # personal details
    nationality = models.CharField(max_length=64, blank=True)
    languages = models.TextField(max_length=200, blank=True)
    preferred_location = models.CharField(max_length=200, blank=True)
    civil_status = models.CharField(max_length=16, blank=True, choices=CIVIL_STATUS_CHOICES)
    dependents = models.TextField(blank=True)
    gender = models.CharField(max_length=8, blank=True, choices=GENDER_CHOICES)
    highest_educational_qualification = models.CharField(
        max_length=200, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # others
    visa_status = models.ForeignKey(
        VisaStatus, on_delete=models.SET_NULL, null=True, blank=True)
    expected_salary_and_benefits = models.TextField(blank=True)
    availability_for_interview = models.CharField(max_length=200, blank=True)
    notice_period = models.CharField(max_length=100, blank=True)
    candidate_owner = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @property
    def edit_href(self):
        return reverse('contacts:candidates_edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('contacts:candidates_detail', args=[str(self.pk), ])

    def get_absolute_url(self):
        return self.edit_href
