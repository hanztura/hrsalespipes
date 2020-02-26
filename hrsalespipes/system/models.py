import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .helpers import SingletonModel


class User(AbstractUser):
    pass


class Setting(SingletonModel):
    initial_data_runned = models.BooleanField(default=False, blank=True)


class VisaStatus(models.Model):

    class Meta:
        verbose_name_plural = 'Visa Status'

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class InterviewMode(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
