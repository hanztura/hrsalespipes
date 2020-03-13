from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class SingletonModel(Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class User(AbstractUser):
    pass


class Setting(SingletonModel):
    initial_data_runned = models.BooleanField(default=False, blank=True)
    runned_locations_initial_data = models.BooleanField(
        default=False,
        blank=True)
    runned_nationalities_initial_data = models.BooleanField(
        default=False,
        blank=True)


class VisaStatus(models.Model):

    class Meta:
        verbose_name_plural = 'Visa Status'

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class InterviewMode(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
