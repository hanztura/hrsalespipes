from django.db import models
from django.urls import reverse

from simple_history.models import HistoricalRecords

from .db import NewlySignedManager
from .utils import ContactModel
from system.models import User, VisaStatus


class Client(ContactModel):
    name = models.CharField(
        max_length=100, unique=True, db_index=True)
    industry = models.CharField(max_length=64)
    location = models.CharField(max_length=64, blank=False)
    initial_approach = models.TextField(blank=True)
    meeting_arranged = models.TextField(blank=True)
    agreement_term = models.DecimalField(
        max_digits=15, decimal_places=5, default=1.0, blank=True)
    agreement_fee = models.DecimalField(
        max_digits=11, decimal_places=10, default=0.0, blank=True)
    refund_scheme = models.TextField(blank=True)
    validity = models.DateField(null=True, blank=True)
    point_of_contacts = models.TextField(blank=True)
    business_development_person = models.ForeignKey(
        'Employee', on_delete=models.SET_NULL, null=True, blank=True)
    signed_on = models.DateField(null=True, blank=True)

    history = HistoricalRecords()

    objects = models.Manager()
    newly_signed = NewlySignedManager()

    class Meta:
        permissions = (
            (
                'edit_client_agreement_fields',
                'Can edit client agreement fields'
            ),
        )
        ordering = 'name',

    @property
    def edit_href(self):
        return reverse('contacts:clients_edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('contacts:clients_detail', args=[str(self.pk), ])

    def get_absolute_url(self):
        return self.edit_href


class Supplier(ContactModel):
    point_of_contacts = models.TextField(blank=True)

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


class CVTemplate(models.Model):
    name = models.CharField(max_length=100)
    template = models.FileField(upload_to='CV_TEMPLATES')
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = 'name', 'id'

    def __str_(self):
        return self.name


class Candidate(ContactModel):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'))
    CIVIL_STATUS_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Widowed', 'Widowed'),
        ('Divorced', 'Divorced'),
        ('Separated', 'Separated'))

    CV_FIELDS = (
        'code',
        'name',
        'contact_number',
        'alternate_contact_number',
        'whatsapp_link',
        'email_address',
        'skype_id',
        'ms_teams_id',
        'location',

        'current_previous_position',
        'current_previous_company',
        'current_previous_benefits',
        'current_previous_salary',
        'motivation_for_leaving',
        'expected_benefits',
        'expected_salary',

        'nationality',
        'languages',
        'preferred_location',
        'civil_status',
        'dependents',
        'gender',
        'highest_educational_qualification',
        'date_of_birth',

        'is_medical',
        'medical_experience_in_years',
        'specialization',
        'other_certifications',
        'bls_validity',
        'acls_validity',
        'haad_dha_license_validity',
        'haad_dha_license_type',
        'job_title_on_dha_haad',
        'dataflow_last_update',

        'visa_status',
        'driving_license',
        'availability_for_interview',
        'notice_period',
        'candidate_owner',
        'cv_template',
        'notes',
    )
    name = models.CharField(
        max_length=100, unique=True, db_index=True)

    # work history
    current_previous_position = models.TextField(
        blank=True, verbose_name='position')
    current_previous_company = models.CharField(
        max_length=200, blank=True, verbose_name='company')
    current_previous_benefits = models.TextField(
        blank=True, verbose_name='salary and benefits')
    current_previous_salary = models.CharField(
        max_length=250, null=True, blank=True)
    motivation_for_leaving = models.TextField(blank=True)
    expected_benefits = models.TextField(blank=True)
    expected_salary = models.CharField(max_length=250, null=True, blank=True)

    # personal details
    nationality = models.CharField(max_length=64, blank=True)
    languages = models.TextField(max_length=1000, blank=True)
    preferred_location = models.CharField(max_length=200, blank=True)
    civil_status = models.CharField(
        max_length=16, blank=True, choices=CIVIL_STATUS_CHOICES)
    dependents = models.TextField(blank=True)
    gender = models.CharField(max_length=8, blank=True, choices=GENDER_CHOICES)
    highest_educational_qualification = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    # medical
    is_medical = models.BooleanField(default=False, blank=True)
    medical_experience_in_years = models.SmallIntegerField(
        default=0,
        blank=True)
    specialization = models.TextField(
        blank=True,
        verbose_name='Field of specialization')
    other_certifications = models.TextField(blank=True)
    bls_validity = models.DateField(null=True, blank=True)
    acls_validity = models.DateField(null=True, blank=True)
    haad_dha_license_validity = models.DateField(null=True, blank=True)
    haad_dha_license_type = models.CharField(
        max_length=5,
        blank=True,
        choices=(
        ('HAAD', 'HAAD'),
        ('DHA', 'DHA')))
    job_title_on_dha_haad = models.CharField(max_length=250, blank=True)
    dataflow_last_update = models.DateField(null=True, blank=True)

    # others
    visa_status = models.ForeignKey(
        VisaStatus, on_delete=models.SET_NULL, null=True, blank=True)
    driving_license = models.CharField(max_length=100, blank=True)
    availability_for_interview = models.CharField(max_length=200, blank=True)
    notice_period = models.TextField(blank=True)
    candidate_owner = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        null=True)
    cv_template = models.ForeignKey(
        CVTemplate,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    notes = models.TextField(blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def current_previous_salary_and_benefits(self):
        value = ''
        if self.current_previous_salary:
            if self.current_previous_benefits:
                value = '{}; {}'.format(
                    self.current_previous_salary,
                    self.current_previous_benefits)
            else:
                value = self.current_previous_salary
        else:  # if salary is null or 0
            if self.current_previous_benefits:
                value = self.current_previous_benefits
            else:  # if both salary and benefits are 0 or None
                pass

        return value

    @property
    def expected_salary_and_benefits(self):
        value = ''
        if self.expected_salary:
            if self.expected_benefits:  # both are with value
                value = '{}; {}'.format(
                    self.expected_salary,
                    self.expected_benefits)
            else:
                value = self.expected_salary
        else:  # if salary is null or 0
            if self.expected_benefits:
                value = self.expected_benefits
            else:  # if both salary and benefits are 0 or None
                pass

        return value

    @property
    def edit_href(self):
        return reverse('contacts:candidates_edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('contacts:candidates_detail', args=[str(self.pk), ])

    def get_absolute_url(self):
        return self.edit_href
