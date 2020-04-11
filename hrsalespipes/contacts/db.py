from django.db import models
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from system.models import Setting


class NewlySignedManager(models.Manager):
    def get_queryset(self):
        today = timezone.localdate()
        setting = Setting.load()
        date_from = today - relativedelta(
            days=setting.newly_signed_clients_number_of_days)

        return super().get_queryset().filter(
            signed_on__gte=date_from)
