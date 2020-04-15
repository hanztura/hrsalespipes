from django.db import models
from django.utils import timezone


class CVSentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            cv_date_shared__isnull=False)


class TentativeJoiningManager(models.Manager):
    def get_queryset(self):
        q = super().get_queryset().select_related('status').filter(
            status__should_create_pipeline=True)

        today = timezone.localdate()
        q = q.exclude(tentative_date_of_joining__lt=today)
        return q
