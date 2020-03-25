from uuid import uuid4

from django.db import models

from django.conf import settings
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

backup_storage_path = str(settings.BACKUPS_STORAGE_ROOT)


class Backup(TimeStampedModel):
    class Meta:
        permissions = [
            (
                'download_backups',
                'Can download backups'
            ),
        ]
        get_latest_by = '-modified'
        ordering = ('-modified', '-created',)

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True)
    backup = models.FilePathField(
        path=backup_storage_path,
        editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        editable=False)

    def __str_(self):
        return self.name

    @property
    def edit_href(self):
        return reverse('backups:edit', args=[str(self.pk), ])

    @property
    def view_href(self):
        return reverse('backups:detail', args=[str(self.pk), ])

    @property
    def list_href(self):
        return reverse('backups:list')

    def get_absolute_url(self):
        return self.list_href
