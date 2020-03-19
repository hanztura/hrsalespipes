from django.db import models

from .utils import custom_permissions


class Dashboard(models.Model):

    class Meta:
        permissions = custom_permissions
