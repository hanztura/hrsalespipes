from uuid import uuid4

from django.db import models

from django.conf import settings
from django_extensions.db.models import TimeStampedModel


class Backup(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True)
    backup = models.FileField(
        upload_to='backups/',
        editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False)

    def __str_(self):
        return self.name
