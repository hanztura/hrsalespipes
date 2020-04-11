from django.db import models


class CVSentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            cv_date_shared__isnull=False)
