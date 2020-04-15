from enum import Enum
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.urls import reverse

from simple_history.models import HistoricalRecords

from .db import UnpaidCommissionManager
from contacts.models import Employee
from salespipes.models import Pipeline
from system.db import IsDeletedAbstractModel


class Rate(models.Model):

    class ROLE_TYPE(Enum):
        # one is the lowest level compared to two and three
        # others is a commission created with 0 amount by default
        one = ('one', settings.COMMISSION_RATE_ROLE_TYPE_ONE_ALIAS)
        two = ('two', settings.COMMISSION_RATE_ROLE_TYPE_TWO_ALIAS)
        three = ('three', settings.COMMISSION_RATE_ROLE_TYPE_THREE_ALIAS)
        others = ('others', settings.COMMISSION_RATE_ROLE_TYPE_OTHERS_ALIAS)

    name = models.CharField(max_length=100)
    straight_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0)
    role_type = models.CharField(
        max_length=100,
        choices=[x.value for x in ROLE_TYPE],
        unique=True,
        null=True)

    def __str__(self):
        return self.name

    @property
    def use_table(self):
        details = self.details.count()
        if details:
            return True

        return False


class RateDetail(models.Model):

    class RATE_VALUE_TYPE(Enum):
        amount = ('amount', 'Amount')
        percentage = ('percentage', 'Percentage')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    class Meta:
        ordering = ('base_minimum', 'base_maximum')

    rate_record = models.ForeignKey(
        Rate,
        on_delete=models.PROTECT,
        related_name='details')
    base_minimum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='minimum')
    base_maximum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='maximum')
    rate_value_type = models.CharField(
        max_length=50,
        choices=[x.value for x in RATE_VALUE_TYPE])
    rate_value = models.DecimalField(max_digits=10, decimal_places=2)


class Commission(IsDeletedAbstractModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    date = models.DateField()
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.PROTECT,
        related_name='commissions')
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='employee_commissions',
        null=True)
    rate_role_type = models.CharField(
        max_length=100,
        null=True)
    rate_used = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    history = HistoricalRecords()

    objects = models.Manager()
    unpaid = UnpaidCommissionManager()

    class Meta:
        ordering = (
            '-date',
            '-pipeline__job_candidate__job__reference_number',
            'rate_role_type')
        permissions = [
            (
                'view_report_commissions_earned_summary',
                'Can view report Commissions Earned Summary'
            ),
            (
                'view_all_commissions',
                'Can view all commission records'
            ),
        ]

    @property
    def edit_href(self):
        return reverse('commissions:edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('commissions:detail', args=[str(self.pk), ])

    @property
    def delete_href(self):
        return reverse('commissions:delete', args=[str(self.pk), ])

    def get_absolute_url(self):
        return self.view_href
