from django.db import models


class SuccessfulJobsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status__probability__gte=1)
