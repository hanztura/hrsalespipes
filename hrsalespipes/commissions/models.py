from enum import Enum

from django.db import models

from contacts.models import Employee
from salespipes.models import Pipeline


class Rate(models.Model):
    name = models.CharField(max_length=100)
    straight_rate = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0)

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


class Role(models.Model):
    name = models.CharField(max_length=100)
    rate = models.ForeignKey(
        Rate,
        on_delete=models.PROTECT,
        related_name='roles')
    is_commission_individual = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class EmployeeRole(models.Model):
    employee = models.OneToOneField(
        Employee,
        on_delete=models.PROTECT,
        related_name='roles')
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='employees')


class Commission(models.Model):
    date = models.DateField()
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.PROTECT,
        related_name='commissions')
    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name='role_commissions')
    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name='employee_commissions')
