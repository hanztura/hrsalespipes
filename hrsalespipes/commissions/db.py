from django.db import models


class UnpaidCommissionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_paid=False)
